# Phase 1 Parity Audit


## Status Legend

| Status | Meaning |
| --- | --- |
| Implemented | Python equivalent exists and is wired for runtime use. |
| Partial | Python equivalent exists but behavior, contract, or coverage is incomplete. |
| Missing | No meaningful Python equivalent exists yet. |
| Not wired | Python equivalent exists but application composition does not expose it. |

## Route Matrix

| TypeScript route | Python equivalent | Status | Notes |
| --- | --- | --- | --- |
| `POST /api/signup` | `main/config/app.py` registers `/api/signup` | Partial | Route exists, but app composition uses `InMemoryAddAccountRepository`; factory wiring has Mongo repository available but is not used here. |
| `POST /api/login` | `main/config/app.py` registers `/api/login` | Partial | Route exists, but shares the in-memory account repository issue. |
| `POST /api/surveys` | `presentation/controllers/add_survey_controller.py`, `main/factories/controllers.py` | Not wired | Controller/use case/repository factory exist, but Flask app does not register the route or admin auth middleware. |
| `GET /api/surveys` | `presentation/controllers/load_surveys_controller.py`, `main/factories/controllers.py` | Not wired | Controller/use case/repository factory exist, but Flask app does not register the route or user auth middleware. |
| `PUT /api/surveys/:surveyId/results` | `presentation/controllers/save_survey_result_controller.py`, `main/factories/controllers.py` | Not wired | Controller/use case/repository factory exist, but Flask app does not register the route or pass route params. |
| `GET /api/surveys/:surveyId/results` | `presentation/controllers/load_survey_result_controller.py`, `main/factories/controllers.py` | Not wired | Controller/use case/repository factory exist, but Flask app does not register the route or pass route params. |
| Static files | None | Missing | TypeScript has `main/config/static-files.ts`; Flask app does not serve the TypeScript `public` equivalent. |
| Swagger/OpenAPI docs | None | Missing | TypeScript has `main/docs/**` and `config-swagger.ts`; no Flask/RESTX docs are wired. |
| Health | `/health` | Implemented | Python-only health endpoint. |
| Legacy signup | `/signup` | Implemented | Kept for backward compatibility; not part of TypeScript parity. |

## Controller Matrix

| TypeScript controller | Python equivalent | Status | Notes |
| --- | --- | --- | --- |
| `signup-controller.ts` | `presentation/controllers/signup/signup.py` | Partial | Exists with validation and authentication flow; public contract still needs Phase 4 verification. |
| `login-controller.ts` | `presentation/controllers/login_controller.py` | Partial | Exists with validation and auth flow; public contract still needs Phase 4 verification. |
| `add-survey-controller.ts` | `presentation/controllers/add_survey_controller.py` | Not wired | Exists, not exposed through Flask route. |
| `load-surveys-controller.ts` | `presentation/controllers/load_surveys_controller.py` | Not wired | Exists, not exposed through Flask route. |
| `save-survey-result-controller.ts` | `presentation/controllers/save_survey_result_controller.py` | Not wired | Exists, not exposed through Flask route. |
| `load-survey-result-controller.ts` | `presentation/controllers/load_survey_result_controller.py` | Not wired | Exists, not exposed through Flask route. |
| `log-controller-decorator.ts` | None | Missing | No Python controller error logging decorator/repository wiring. |

## Use Case Matrix

| TypeScript use case | Python equivalent | Status | Notes |
| --- | --- | --- | --- |
| `DbAddAccount` | `data/usecases/add_account/db_add_account.py` | Partial | Exists; runtime app currently wires in-memory repository. |
| `DbAuthentication` | `data/usecases/authentication/db_authentication.py` | Partial | Exists; runtime app currently wires in-memory repository. |
| `DbLoadAccountByToken` | `data/usecases/load_account_by_token.py` | Partial | Exists; middleware wiring needs route integration. |
| `DbAddSurvey` | `data/usecases/survey.py` | Not wired | Exists and factory exists. |
| `DbLoadSurveys` | `data/usecases/survey.py` | Not wired | Exists and factory exists. |
| `DbCheckSurveyById` / `DbLoadSurveyById` | `data/usecases/survey.py` | Not wired | Exists under Python naming. |
| `DbLoadAnswersBySurvey` | `data/usecases/survey.py` | Not wired | Exists and factory exists. |
| `DbSaveSurveyResult` | `data/usecases/save_survey_result/db_save_survey_result.py` | Not wired | Exists and has focused tests. |
| `DbLoadSurveyResult` | `data/usecases/load_survey_result.py` | Not wired | Exists and factory exists. |

## Repository Matrix

| TypeScript repository/protocol | Python equivalent | Status | Notes |
| --- | --- | --- | --- |
| `AccountMongoRepository.add` | `infra/db/mongodb/account_repository.py` | Partial | Exists with integration test coverage. |
| `loadByEmail` | `infra/db/mongodb/account_repository.py` | Partial | Exists; parity tests still thin. |
| `loadByToken` | `infra/db/mongodb/account_repository.py` | Partial | Exists; role-aware admin behavior needs route tests. |
| `updateAccessToken` | `infra/db/mongodb/account_repository.py` | Partial | Exists; runtime app not using Mongo account repository. |
| `SurveyMongoRepository.add` | `infra/db/mongodb/survey_repository.py` | Partial | Exists; route-level behavior unverified. |
| `loadAll` | `infra/db/mongodb/survey_repository.py` | Partial | Exists; answer-state aggregation/sorting parity needs verification. |
| `loadById` | `infra/db/mongodb/survey_repository.py` | Partial | Exists; ObjectId edge cases need parity tests. |
| `loadAnswersBySurvey` | `infra/db/mongodb/survey_repository.py` | Partial | Exists. |
| `SurveyResultMongoRepository.save` | `infra/db/mongodb/survey_result_repository.py` | Partial | Exists; aggregation parity still needs broader tests. |
| `loadBySurveyId` | `infra/db/mongodb/survey_result_repository.py` | Partial | Exists; zero-result behavior needs parity verification. |
| `LogMongoRepository` | None | Missing | Needed for controller error logging parity. |
| `MongoHelper` | `infra/db/mongodb/helpers/mongo_helper.py` | Partial | Exists; query builder equivalent is missing. |

## Middleware And Adapter Matrix

| TypeScript component | Python equivalent | Status | Notes |
| --- | --- | --- | --- |
| `body-parser.ts` | Flask JSON request parsing, `main/middlewares/body_parser.py` | Partial | Test exists; Flask app does not explicitly install body parser middleware. |
| `content-type.ts` | None | Missing | Needs JSON response header middleware. |
| `cors.ts` | `main/config/middlewares.py` | Partial | Needs parity headers/preflight verification in Phase 3. |
| `no-cache.ts` | None | Missing | Needs response headers. |
| `auth.ts` | `main/factories/middlewares.py`, `presentation/middlewares/auth_middleware.py` | Not wired | Middleware and adapter exist but protected routes are not registered. |
| `admin-auth.ts` | `main/factories/middlewares.py` | Not wired | Role-aware factory exists but is not attached to survey creation. |
| `express-route-adapter.ts` | `main/adapters/flask_route_adapter.py` | Partial | Exists; route params need Phase 2 verification. |
| `express-middleware-adapter.ts` | `main/adapters/flask_middleware_adapter.py` | Not wired | Exists but unused by current app routes. |

## Test Matrix

| TypeScript test area | Python equivalent | Status | Notes |
| --- | --- | --- | --- |
| Validation validators | None | Missing | Python validators exist, but no focused validator parity tests. |
| Signup controller | `tests/presentation/controllers/signup/test_signup.py` | Partial | Exists. |
| Login controller | None | Missing | Needs controller tests. |
| Add survey controller | None | Missing | Needs controller tests. |
| Load surveys controller | None | Missing | Needs controller tests. |
| Save survey result controller | None | Missing | Needs controller tests. |
| Load survey result controller | None | Missing | Needs controller tests. |
| Auth middleware | None | Missing | Needs middleware tests. |
| Main middlewares | `tests/main/middlewares/test_body_parser.py` | Partial | Only body parser covered. |
| Route integration tests | None | Missing | Needed for all six `/api` routes. |
| Account Mongo repository | `tests/infra/db/mongodb/account-repository/test_account.py` | Partial | One integration test. |
| Survey Mongo repository | None | Missing | Needed. |
| Survey result Mongo repository | None | Missing | Needed. |
| Mongo helper | `tests/infra/db/mongodb/helpers/test_mongo_helper.py` | Partial | Exists. |
| Bcrypt adapter | `tests/infra/cryptography/test_bcrypt_adapter.py` | Partial | Exists. |
| JWT adapter | None | Missing | Needed. |
| Email validator adapter | `tests/utils/test_email_validator_adapter.py` | Implemented | Exists. |
| Data use cases | `tests/data/usecases/**` | Partial | Add account and save survey result covered; other use cases need tests. |
| Log controller decorator/repository | None | Missing | Needed. |

## Cleanup Decisions

- `__pycache__` directories are generated artifacts and are not feature work. They were removed from the project tree, excluding virtual environment contents.
- `presentation/controllers/.DS_Store` is a macOS generated file and should not be kept. It was removed.
- `.gitignore` already excludes `__pycache__/`, `*.py[cod]`, `.DS_Store`, and virtual environments.

## Mongo Test Setup Decision

- Pytest now defaults `MONGO_DB_NAME` to `flask_tdd_test` unless explicitly overridden.
- `conftest.py` builds an authenticated `MONGO_URL` from `.env` values when `MONGO_PASSWORD` is present and `MONGO_URL` is absent.
- The account repository integration fixture no longer falls back to unauthenticated `mongodb://localhost:27017`; it skips with setup guidance if `MONGO_URL` is unavailable.
- `make test-integration` now uses the isolated `flask_tdd_test` database name by default and keeps `authSource=admin`.
