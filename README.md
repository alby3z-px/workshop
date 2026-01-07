# Workshop Product & Session Capture (Streamlit)

A lightweight Streamlit app to capture product information and workshop notes across Operators/Developers and Business Owners. Data is persisted in a single aggregated JSON file for simplicity and easy backup/restore.

## Quick Start

Pick the fastest path for your OS. The virtual environment (`.venv`) is not committed (by design), but the steps below create it automatically.

### macOS/Linux — copy/paste and go

```bash
python3 -m venv .venv \
	&& source .venv/bin/activate \
	&& python3 -m pip install -r requirements.txt \
	&& streamlit run app.py
```

### Windows (PowerShell)

```powershell
python -m venv .venv; 
. .\.venv\Scripts\Activate.ps1; 
python -m pip install -r requirements.txt; 
streamlit run app.py
```

On first run, the app creates the `data/` and `uploads/` folders and initializes the aggregated store.

### Manual steps (if you prefer)

1) Create and activate a virtual environment (macOS/Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows (PowerShell):

```powershell
. .\.venv\Scripts\Activate.ps1
```

2) Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

3) Run the app

```bash
streamlit run app.py
```

## Using the App

- Navigation lives in the left sidebar. Active pages are:
	- Products: list, add, edit, and delete products.
	- Business Owner Sessions: capture owner-level sessions covering their product portfolio.
	- Export Backup: download/restore the full data file.

### Import Products from CSV

- A starter catalog CSV ships with the app at uploads/Product Catalog 2c34aca9ecb38075ab7fcdbec29ce503.csv. Use it on first run to pre-populate products and owners.
- Click “Import from CSV” in the sidebar. The importer creates missing products and pre-fills Business Owners’ product lists.

### Products Page

- Shows a table with Product Name and Business Owner. Owner chips are color-coded.
- Edit opens the Operator/Developer session editor for the selected product.
- Delete removes the product from the aggregated store.
- Use ➕ Add Product to create a new product record.

### Add Product

- Provide basic metadata (workstream, owner, users, operator, developer). Saving initializes the product and opens its session editor.

### Product Operator/Developer Session

- Organized into expanders that mirror the workshop structure:
	- Part 1: Developer’s Product Overview
	- Part 2: Development Deep-Dive (technical stack, practices, challenges)
	- Part 3: Operation Deep-Dive (usage, pain points, gaps)
	- Part 4: Data & Integration (inputs, outputs, storage, integrations)
	- Part 5: Wrap-Up (maturity sliders, notes, quotes)
- Quotes field format: one per line as `Speaker | timestamp | quote`.
- Click “Save Technical session” to persist changes.

### Business Owner Sessions

- Select a Business Owner (grouped from the CSV import) and fill out the session form covering context, portfolio, cross-product processes, partner delivery, and future state.
- Click “Save Business Owner Session” to persist changes.

### Backup & Restore

- Export Backup lets you download the full data as JSON.
- Restore Backup accepts a JSON file containing `products` and `business_owners` keys and replaces the current store.

## Data & Conventions

- Single data file: data/aggregated.json (auto-created). Do not hand-edit while the app is running.
- Product IDs: derived via slugify(product_name) to ensure stable keys.
- Saves are deep-merged to preserve nested structures. No timestamp fields are stored.
- After saves, the UI refreshes automatically.

## Configuration Notes

- CSV path is defined as PRODUCT_CATALOG_FILE in app.py. Update it if your file name or location differs.
- Dependencies are listed in pyproject.toml and requirements.txt; Streamlit and Pandas are the only runtime libraries.

## Troubleshooting

- CSV not detected: ensure the file path and name match exactly under uploads/.
- Permission or write errors: verify the app has write access to the data/ directory.
- Virtual environment issues: re-create the venv and reinstall requirements.
- `python3` not found on macOS: install Python 3 (e.g., `brew install python@3.12`) and re-run the steps.
	- If `brew` is not installed: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
- Why `.venv` isn’t in the repo: virtualenvs are OS/architecture-specific and large; recreating from `requirements.txt` is reliable and quick.
