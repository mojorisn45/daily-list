# Daily List

Phone-only, single-user daily to-do app. Streamlit + Supabase.

## Local dev

```
python -m venv .venv
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
streamlit run app.py
```

Secrets live in `.streamlit/secrets.toml` (gitignored). On Streamlit Community Cloud, set them in the app settings UI.

## Structure

- `app.py` — entry point, auth gate, rollover trigger, tabs
- `db.py` — Supabase client + CRUD
- `auth.py` — password gate
- `rollover.py` — pure rollover logic + apply function
- `views/` — Today, Archive, Recurring tab renderers
- `tests/` — unit tests (rollover)
