# Workshop Session Capture (Streamlit prototype)

Lightweight Streamlit app to capture product workshop sessions (Developer / Operator). Stores one JSON file per session under `data/sessions/`.

## Quick start

1. Create a Python venv and activate it
2. Install deps: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`

## Data storage

- Sessions are stored as `data/sessions/session-<uuid>.json`
- Index: `data/index.json`
- Attachments (if needed) store in `uploads/`

## Features

- Create session with sections matching the workshop agenda
- Maturity scoring (1-5)
- Verbatim quote capture
- List and view saved sessions
- Export single or all sessions to CSV / Markdown

## Next steps
- Add attachments upload support
- Improve attendees UI (structured inputs)
- Add simple UI filters and summary dashboard
