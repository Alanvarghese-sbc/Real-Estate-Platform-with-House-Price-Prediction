Project snapshot

- Mono-repo Django project with a single central app `house` that contains the database models (auto-generated from a legacy DB). Don't split schema across the smaller UI apps.

Architecture & intent

- `house/` is the primary Django app and contains the legacy DB schema (`house/models.py`) exported with `managed = False` (inspectdb). The rest of the folders (`administrator/`, `broker/`, `user/`) are lightweight UI/URL modules that import `house.models` for database access.
- Routing: root URLconf is `house/urls.py` and it includes `administrator.urls`, `broker.urls`, and `user.urls`. See `house/view.py` for the top-level flows (login, register, session keys `semail` and `seuser_id`).

Key files to reference

- `house/settings.py` — DB, static/media, templates. Note: DATABASES is configured for MySQL (legacy). There is also a `db.sqlite3` file at repo root (likely leftover). Verify which DB you intend to use before running migrations.
- `house/models.py` — central, auto-generated models (many classes use `managed = False`). Prefer reading this file rather than creating new models for the same tables.
- `house/view.py` — top-level views and auth flow; uses `models.Register` and `models.Login` (example: `register_user()` creates a `Register` + `Login` record).
- `administrator/urls.py`, `broker/urls.py`, `user/urls.py` — examples of app-level routing and naming conventions for view functions.
- `templates/` and `static/` — templates live in `templates/` (configured via `TEMPLATES['DIRS']`) and static assets under `static/`; uploaded media stored under `media/` (see `MEDIA_ROOT`). Property images are placed in `media/property_images/`.

Project-specific conventions (concrete rules for agents)

- Data model is centralized in `house/models.py`. Calls in view modules import it with `from house import models` — follow that pattern instead of importing models from small app folders.
- Do not enable migrations for tables in `house/models.py` unless you intentionally convert `managed = False` models to managed. Changing those models without DB migration coordination will cause confusion.
- The smaller app folders (`administrator`, `broker`, `user`) are used primarily for URL/view organization. They do not register their models with the DB schema — prefer to check `house/models.py` when in doubt.
- Session keys used in auth flows: `semail`, `seuser_id`. Use these keys when adding or verifying session-based logic.

Developer workflows & quick commands

- Start dev server (default settings expect MySQL; if you want sqlite for quick dev, update `DATABASES` in `house/settings.py`):

```bash
python manage.py migrate
python manage.py runserver
```

- If using MySQL, ensure an appropriate DB driver is installed (`mysqlclient` or `PyMySQL`) and the DB named in `house/settings.py` exists.
- Create a superuser (if using Django admin tables from the legacy DB, verify `auth_user` usage):

```bash
python manage.py createsuperuser
```

- Static & media

```bash
# development: static files served from `static/` and uploaded files in `media/`
python manage.py collectstatic  # for production deploys
```

Patterns to follow when editing

- When adding new database-backed features, prefer creating new tables through a new app and including it in `INSTALLED_APPS` (in `house/settings.py`) instead of modifying the legacy `house/models.py` directly.
- Keep template paths consistent: templates are referenced as `home/index.html`, `login/login.html`, etc. Check `templates/` structure when adding views.
- Views in the `administrator`, `broker`, and `user` directories use function-based views with explicit redirects (see `administrator/urls.py` examples). Keep route naming consistent (e.g., `dashboardAdmin`, `dashboardBroker`, `userDashboard`).

Testing and debugging notes

- There are no top-level test configurations beyond Django defaults. Run `python manage.py test` to run tests if any exist.
- Because models were generated from an existing DB, tests that depend on migrations may require a live MySQL test DB or conversion of those models to managed models.

Integration points & gotchas

- Legacy DB: `house/models.py` contains `managed = False` classes — this is the single source-of-truth for database fields. Inspect that file before adding/modifying code that relies on table columns (e.g., `Register.email`, `Login.password`).
- Settings mismatch: repo contains `db.sqlite3` but `house/settings.py` points to MySQL. Confirm which DB to use before running `migrate` or `inspectdb`.
- URL includes are relative (e.g., `path('administrator/', include('administrator.urls'))`); many redirect targets in views use relative paths (e.g., `redirect('../administrator/dashboardAdmin')`). Prefer using `reverse()` or named routes when adding new redirects.

If anything here is unclear or you'd like me to add more examples (e.g., common model fields, example request bodies, or sample SQL), tell me which area to expand. 
