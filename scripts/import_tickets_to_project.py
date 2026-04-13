#!/usr/bin/env python3
"""Import markdown tickets into GitHub Issues and a GitHub Project board.

Usage example:
    python scripts/import_tickets_to_project.py \
      --file IMPLEMENTATION_TICKETS.md \
      --repo owner/repo \
      --owner owner \
      --project 2 \
      --dry-run
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Ticket:
    number: int
    title: str
    story_points: str
    priority: str
    description: str
    acceptance_criteria: str
    implementation_notes: str

    @property
    def issue_title(self) -> str:
        return f"Ticket {self.number}: {self.title}"

    @property
    def issue_body(self) -> str:
        return (
            "Imported from `IMPLEMENTATION_TICKETS.md`.\n\n"
            "## Description\n"
            f"{self.description or '_No description provided._'}\n\n"
            "## Acceptance Criteria\n"
            f"{self.acceptance_criteria or '_No acceptance criteria provided._'}\n\n"
            "## Implementation Notes\n"
            f"{self.implementation_notes or '_No implementation notes provided._'}\n\n"
            "## Metadata\n"
            f"- Story Points: {self.story_points or 'N/A'}\n"
            f"- Priority: {self.priority or 'N/A'}\n"
        )


def run_command(command: list[str]) -> str:
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
    except FileNotFoundError as error:
        raise RuntimeError("Required command is missing. Is `gh` installed and on PATH?") from error
    except subprocess.CalledProcessError as error:
        stderr = error.stderr.strip()
        stdout = error.stdout.strip()
        message = stderr or stdout or "Unknown command error."
        if "Failed to log in" in message or "invalid" in message.lower() or "forbidden" in message.lower():
            message = (
                f"{message}\n\n"
                "Authentication issue detected. Re-run:\n"
                "  gh auth login -h github.com\n"
                "  gh auth refresh -s repo -s project"
            )
        raise RuntimeError(f"Command failed: {' '.join(command)}\n{message}") from error
    return result.stdout.strip()


def clean_section_content(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    # Normalize markdown checkboxes to plain bullets to keep issues clean.
    value = re.sub(r"^\s*-\s*✅\s*", "- ", value, flags=re.MULTILINE)
    return value


def parse_tickets(markdown_content: str) -> list[Ticket]:
    ticket_pattern = re.compile(
        r"^## Ticket (?P<number>\d+): (?P<title>.+?)\n"
        r"\*\*Story Points:\*\*\s*(?P<story_points>.+?)\s*\n"
        r"\*\*Priority:\*\*\s*(?P<priority>.+?)\s*\n"
        r"\n### Description\n(?P<description>.*?)"
        r"\n### Acceptance Criteria\n(?P<acceptance_criteria>.*?)"
        r"(?:\n### Implementation Notes\n(?P<implementation_notes>.*?))?"
        r"(?=\n---\n|\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )

    tickets: list[Ticket] = []
    for match in ticket_pattern.finditer(markdown_content):
        ticket = Ticket(
            number=int(match.group("number")),
            title=match.group("title").strip(),
            story_points=match.group("story_points").strip(),
            priority=match.group("priority").strip(),
            description=clean_section_content(match.group("description")),
            acceptance_criteria=clean_section_content(match.group("acceptance_criteria")),
            implementation_notes=clean_section_content(match.group("implementation_notes") or ""),
        )
        tickets.append(ticket)

    return tickets


def list_existing_issue_titles(repo: str) -> set[str]:
    # Use REST API here (instead of `gh issue list --json`) to avoid GraphQL permission edge cases.
    output = run_command(
        [
            "gh",
            "api",
            f"repos/{repo}/issues?state=all&per_page=100",
            "--jq",
            ".[] | select(.pull_request|not) | .title",
        ]
    )
    return {line.strip() for line in output.splitlines() if line.strip()}


def create_issue(repo: str, ticket: Ticket, labels: list[str]) -> str:
    command = [
        "gh",
        "issue",
        "create",
        "--repo",
        repo,
        "--title",
        ticket.issue_title,
        "--body",
        ticket.issue_body,
    ]

    for label in labels:
        command.extend(["--label", label])

    try:
        return run_command(command)
    except RuntimeError as error:
        error_text = str(error).lower()
        # Some repositories don't have the provided labels yet.
        # Retry creation without labels so import can continue.
        if labels and "could not add label" in error_text and "not found" in error_text:
            fallback_command = [
                "gh",
                "issue",
                "create",
                "--repo",
                repo,
                "--title",
                ticket.issue_title,
                "--body",
                ticket.issue_body,
            ]
            print(
                "WARN label not found for issue creation. "
                f"Retrying without labels: {ticket.issue_title}"
            )
            return run_command(fallback_command)
        raise


def add_issue_to_project(project_number: int, project_owner: str, issue_url: str) -> None:
    try:
        run_command(
            [
                "gh",
                "project",
                "item-add",
                str(project_number),
                "--owner",
                project_owner,
                "--url",
                issue_url,
            ]
        )
    except RuntimeError as error:
        error_text = str(error).lower()
        if "content already exists in this project" in error_text:
            print(f"WARN already in project, skipping add: {issue_url}")
            return
        raise


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create GitHub issues from markdown tickets and add them to a GitHub Project board."
    )
    parser.add_argument("--file", default="IMPLEMENTATION_TICKETS.md", help="Path to markdown ticket file.")
    parser.add_argument("--repo", required=True, help="GitHub repository in owner/repo format.")
    parser.add_argument("--owner", required=True, help="GitHub project owner (user or org).")
    parser.add_argument("--project", required=True, type=int, help="GitHub project number.")
    parser.add_argument(
        "--label",
        action="append",
        default=["user-story"],
        help="Issue label to apply. Repeat for multiple labels.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print actions without creating issues.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    ticket_file = Path(args.file)
    if not ticket_file.exists():
        print(f"Ticket file does not exist: {ticket_file}", file=sys.stderr)
        return 1

    markdown_content = ticket_file.read_text(encoding="utf-8")
    tickets = parse_tickets(markdown_content)
    if not tickets:
        print("No tickets found. Verify the markdown format and headings.", file=sys.stderr)
        return 1

    print(f"Parsed {len(tickets)} tickets from {ticket_file}.")
    existing_titles = list_existing_issue_titles(args.repo)
    print(f"Found {len(existing_titles)} existing issues in {args.repo}.")

    created = 0
    skipped = 0
    labels = list(dict.fromkeys(args.label))

    failures: list[str] = []

    for ticket in tickets:
        if ticket.issue_title in existing_titles:
            print(f"SKIP already exists: {ticket.issue_title}")
            skipped += 1
            continue

        if args.dry_run:
            print(f"DRY-RUN create issue + add to project: {ticket.issue_title}")
            continue

        try:
            issue_url = create_issue(args.repo, ticket, labels)
            add_issue_to_project(args.project, args.owner, issue_url)
            print(f"CREATED {ticket.issue_title} -> {issue_url}")
            created += 1
        except RuntimeError as error:
            message = f"FAILED {ticket.issue_title}: {error}"
            print(message, file=sys.stderr)
            failures.append(message)

    print(
        f"Done. Created={created}, Skipped={skipped}, Failed={len(failures)}, DryRun={args.dry_run}"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
