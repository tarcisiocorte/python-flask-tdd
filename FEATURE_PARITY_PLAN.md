# Feature Parity Plan: Python Flask API vs clean-ts-api

This plan describes how to implement, in this Python Flask project, the same feature and functionality available in `/Users/tarcisiocorte/dev/clean-ts-api`.

## Target Feature Parity

The TypeScript project has six main API features:

1. `POST /api/signup`
2. `POST /api/login`
3. `POST /api/surveys`
4. `GET /api/surveys`
5. `PUT /api/surveys/:surveyId/results`
6. `GET /api/surveys/:surveyId/results`

Supporting features include:

- JWT authentication via `x-access-token`
- Admin-only authorization
- MongoDB persistence
- bcrypt password hashing
- Validation composite
- Middleware adapters
- Route adapters
- Swagger/OpenAPI docs
- Static file serving
- CORS, content-type, and no-cache middleware
- Controller error logging
- Route/integration tests
- Repository, use-case, controller, middleware, and validation tests

## Phase 1: Baseline Audit And Cleanup

1. Create a parity checklist document or extend this file.
2. List every TypeScript route, controller, use case, repository, middleware, and test.
3. Map each one to the Python equivalent:
   - already implemented
   - partially implemented
   - missing
   - implemented but not wired
4. Remove accidental generated files from feature consideration, such as `__pycache__`.
5. Decide whether `.DS_Store` under `presentation/controllers/` should be removed.
6. Fix the current Mongo test setup issue:
   - Current test run gives `Command delete requires authentication`.
   - Ensure tests use the correct `MONGO_URL`, `MONGO_DB_NAME`, and auth source.
   - Prefer isolated test database names.

Deliverable: a written matrix showing Python vs TypeScript parity.

## Phase 2: Application Composition And Route Registration

Current issue: the Python project has survey factories, but `main/config/app.py` only wires signup, login, legacy signup, and health.

1. Refactor `main/config/app.py` to use factory functions from `main/factories/controllers.py`.
2. Add route registration modules similar to the TypeScript project:
   - `main/routes/login_routes.py`
   - `main/routes/survey_routes.py`
   - `main/routes/survey_result_routes.py`
   - optional `main/config/routes.py`
3. Register all routes under `/api`:
   - `POST /api/signup`
   - `POST /api/login`
   - `POST /api/surveys`
   - `GET /api/surveys`
   - `PUT /api/surveys/<survey_id>/results`
   - `GET /api/surveys/<survey_id>/results`
4. Keep `/health`.
5. Decide whether to keep legacy `/signup`; likely keep it for backward compatibility, but mark it as legacy.
6. Ensure Flask route params are passed into `HttpRequest.params`.

Deliverable: all TypeScript API routes exist in Flask.

## Phase 3: Middleware Parity

Implement Python equivalents for TypeScript middlewares.

1. `body_parser`
   - Mostly already covered by Flask.
   - Keep tests verifying JSON parsing.

2. `content_type`
   - Add `Content-Type: application/json` on JSON responses.
   - Avoid breaking empty `204` responses.

3. `cors`
   - Add headers:
     - `Access-Control-Allow-Origin: *`
     - `Access-Control-Allow-Methods`
     - `Access-Control-Allow-Headers`
   - Handle `OPTIONS` preflight.

4. `no_cache`
   - Add:
     - `Cache-Control: no-store, no-cache, must-revalidate, proxy-revalidate`
     - `Pragma: no-cache`
     - `Expires: 0`

5. `auth`
   - Use existing `presentation/middlewares/auth_middleware.py`.
   - Adapt it through `main/adapters/flask_middleware_adapter.py`.

6. `admin_auth`
   - Use the same middleware, but with role `"admin"`.

7. Route middleware wiring:
   - `POST /api/surveys`: admin auth.
   - `GET /api/surveys`: user auth.
   - Survey result routes: user auth.

Deliverable: route-level anonymous, user, and admin behavior matches the TypeScript project.

## Phase 4: Account And Authentication Feature Parity

Signup and login exist, but need production wiring and parity checks.

1. Ensure signup uses Mongo repository, not only an in-memory repository.
2. Confirm signup flow:
   - required fields
   - password confirmation
   - email validation
   - duplicate email returns `403`
   - password is bcrypt-hashed
   - account is inserted
   - JWT token is generated from account id
   - access token is stored
   - response returns `accessToken` and `name`
3. Confirm login flow:
   - required fields
   - email validation
   - invalid credentials return `401`
   - valid credentials generate and store token
   - response returns `accessToken` and `name`
4. Align JSON field names with the TypeScript public contract:
   - `accessToken`
   - `passwordConfirmation`
5. Ensure `JWT_SECRET` is required in non-local contexts, but still usable in tests.

Deliverable: signup and login behavior and contracts match the TypeScript project.

## Phase 5: Survey Creation

1. Verify `domain/usecases/add_survey.py`.
2. Verify survey data use cases, or split them into TypeScript-like modules if helpful:
   - `DbAddSurvey`
   - `DbLoadSurveys`
   - `DbCheckSurveyById`
   - `DbLoadAnswersBySurvey`
3. Ensure `AddSurveyController`:
   - validates `question`
   - validates `answers`
   - calls add survey use case
   - returns `204`
   - returns `400` on missing params
   - returns `500` on unexpected errors
4. Ensure Mongo survey repository inserts:
   - `question`
   - `answers`
   - `date`
5. Add admin-auth route tests:
   - no token returns `403`
   - user token returns `403`
   - admin token returns `204`

Deliverable: `POST /api/surveys` matches the TypeScript project.

## Phase 6: List Surveys

1. Wire `GET /api/surveys`.
2. Require user auth.
3. Implement repository behavior equivalent to the TypeScript aggregation:
   - load all surveys
   - include whether the current account has answered each survey
   - sort by date descending if the TypeScript implementation does so
4. Response behavior:
   - no surveys returns `204`
   - surveys exist returns `200` with an array
5. Add tests:
   - no token returns `403`
   - valid token and no surveys returns `204`
   - valid token and surveys returns `200`
   - repository error returns `500`

Deliverable: `GET /api/surveys` matches the TypeScript project.

## Phase 7: Save Survey Result

1. Wire `PUT /api/surveys/<survey_id>/results`.
2. Require user auth.
3. Controller must:
   - get `survey_id` from route params
   - get `answer` from body
   - get `account_id` from auth middleware
4. Validate:
   - invalid or missing token returns `403`
   - invalid survey id returns `403`
   - invalid answer returns `403`
5. Use cases:
   - load valid answers by survey id
   - save survey result
   - if no previous result exists, create one
   - if previous result exists, update it
6. Repository:
   - use Mongo upsert keyed by `surveyId` and `accountId`
   - store `answer` and `date`
7. Return `200` with full survey result aggregation.

Deliverable: `PUT /api/surveys/<survey_id>/results` matches the TypeScript project.

## Phase 8: Load Survey Result

1. Wire `GET /api/surveys/<survey_id>/results`.
2. Require user auth.
3. Validate:
   - invalid or missing token returns `403`
   - repository or use-case errors return `500`
4. Use `DbCheckSurveyById`.
5. Use `DbLoadSurveyResult`.
6. Repository aggregation should return:
   - survey id
   - question
   - answers
   - answer count
   - percent
   - whether each answer is the current user's answer
   - date
7. If no result exists, return survey answers with zero counts and percents.

Deliverable: `GET /api/surveys/<survey_id>/results` matches the TypeScript project.

## Phase 9: MongoDB Repository Parity

Implement or verify these repository methods.

1. Account repository:
   - `add`
   - `load_by_email`
   - `load_by_token`
   - `update_access_token`
   - role-aware token loading where admin can access admin routes

2. Survey repository:
   - `add`
   - `load_all(account_id)`
   - `load_by_id`
   - `load_answers_by_survey`

3. Survey result repository:
   - `save`
   - `load_by_survey_id(survey_id, account_id)`
   - aggregation matching TypeScript behavior

4. Log repository:
   - `log_error`
   - stores stack/message/date in Mongo

5. Mongo helper:
   - connect and reconnect
   - get collection
   - map `_id` to `id`
   - safe ObjectId conversion
   - test database isolation

Deliverable: Mongo adapters match TypeScript behavior.

## Phase 10: Error Logging Decorator

1. Add `main/decorators/log_controller_decorator.py`.
2. Behavior:
   - call wrapped controller
   - if response status is `500`, call `log_error_repository.log_error`
   - return original response
3. Add factory:
   - `main/factories/decorators.py`
4. Wrap production controllers with the decorator, matching TypeScript factory behavior.
5. Add tests:
   - calls controller
   - returns same response
   - logs only on `500`
   - handles log repository errors according to TypeScript behavior

Deliverable: controller error logging parity.

## Phase 11: Swagger/OpenAPI Docs

1. Add a docs package:
   - `main/docs/schemas.py`
   - `main/docs/paths.py`
   - or split like the TypeScript project if preferred
2. Generate OpenAPI definitions for:
   - signup
   - login
   - surveys
   - survey results
   - errors
   - auth header
3. Add `/api-docs` route.
4. Use `flasgger`, `swagger-ui-bundle`, or a simple static Swagger JSON plus UI.
5. Add a test that `/api-docs` or `/api-docs.json` loads.

Deliverable: Swagger docs equivalent to the TypeScript project.

## Phase 12: Static Files

1. Add Flask static serving equivalent to TypeScript `setupStaticFiles`.
2. Decide static folder:
   - `static/`
   - or `public/`
3. Add route `/static/...`.
4. Copy or recreate public assets only if needed.
5. Add a simple smoke test.

Deliverable: static file serving parity.

## Phase 13: Tests To Add

Minimum test set for parity.

1. Validation tests:
   - required field
   - email validation
   - compare fields
   - validation composite

2. Presentation controller tests:
   - login
   - signup
   - add survey
   - load surveys
   - save survey result
   - load survey result

3. Middleware tests:
   - auth middleware
   - admin auth
   - body parser
   - cors
   - content type
   - no cache

4. Main route tests:
   - login routes
   - survey routes
   - survey result routes

5. Data use case tests:
   - add account
   - authentication
   - load account by token
   - add survey
   - load surveys
   - check/load survey by id
   - save survey result
   - load survey result

6. Infra tests:
   - bcrypt adapter
   - JWT adapter
   - account Mongo repository
   - survey Mongo repository
   - survey result Mongo repository
   - log Mongo repository
   - Mongo helper

Deliverable: Python test coverage comparable to the TypeScript Jest suite.

## Phase 14: Tooling And Commands

1. Update `Makefile`:
   - `make test-unit`
   - `make test-integration`
   - `make test-routes`
   - `make test-coverage`
   - `make start`
   - `make lint`
2. Update `pytest.ini` markers:
   - `unit`
   - `integration`
   - `route`
   - `slow`
3. Update `requirements-dev.txt` if needed:
   - `pytest`
   - `pytest-cov`
   - `pytest-asyncio`
   - `faker`
   - `mongomock` or testcontainers, if chosen
   - Swagger dependency if chosen
4. Ensure Docker Compose supports Mongo test and dev flows.

Deliverable: reliable local and CI commands.

## Phase 15: README And API Documentation

1. Update `README.md` to list the full API surface.
2. Add curl examples for all six routes.
3. Document auth header:
   - `x-access-token: <token>`
4. Document admin setup:
   - how to create or seed an admin account
5. Document environment variables.
6. Document test commands.
7. Document Docker/Mongo setup.

Deliverable: README matches the actual implemented API.

## Recommended Implementation Order

1. Fix Mongo test configuration.
2. Wire existing survey routes into Flask.
3. Add auth and admin middleware route support.
4. Convert app factory from in-memory account repository to Mongo-backed factories.
5. Add route tests for all six API endpoints.
6. Fill use case and repository gaps revealed by tests.
7. Add error logging decorator.
8. Add CORS, content-type, and no-cache parity.
9. Add Swagger docs.
10. Add static files.
11. Update README and parity checklist.
12. Run the full unit and integration suite.

This order gives the fastest visible parity first: once routes and auth are wired, tests will expose the real behavior gaps cleanly. Then the remaining work becomes a sequence of precise fixes rather than a broad rewrite.
