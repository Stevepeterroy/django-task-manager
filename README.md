# Django Task Manager

A Django task app with account registration, sign-in, user-scoped task lists, create/edit/delete forms, completion controls, due dates and priority fields.

## Run locally

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
export DJANGO_SECRET_KEY="$(.venv/bin/python -c 'import secrets; print(secrets.token_urlsafe(48))')"
export DJANGO_DEBUG=true
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

Open http://127.0.0.1:8000 and register an account. The publication copy uses SQLite for a simple local setup. Database files are ignored. `.env.example` documents the environment variables; export them in your shell because this app does not automatically load that file.

## Security and verification

Task queries are scoped to the authenticated owner. Completion toggles require CSRF-protected POST requests. The original embedded Django key and MySQL credentials were removed; a locally generated environment key is required. Debugging is off by default.

```sh
.venv/bin/python manage.py check
.venv/bin/python manage.py test
```

Tests cover sign-in requirements, cross-user read/mutation isolation, private task lists and the POST requirement. This repository contains no real accounts or task database. A production deployment still needs HTTPS, secure cookie settings, static-file serving and an appropriate host configuration.

## Interface and ordering update

Daybook now uses an updated responsive interface, clear edit/delete controls, and high → medium → low priority ordering for the task list, with completed items last. Regression tests also cover priority order, create/edit/delete and invalid input.
