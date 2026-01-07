# Workshop Product & Session Capture (Streamlit)

A lightweight Streamlit app to capture product information and workshop notes across Operators/Developers and Business Owners. Data is persisted in a single aggregated JSON file for simplicity and easy backup/restore.

## Quick Start

1) Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# On Windows (PowerShell): .venv\Scripts\Activate.ps1
```

2) Install dependencies

```bash
pip install -r requirements.txt
```

3) Run the app

```bash
streamlit run app.py
```

On first run, the app creates the `data/` and `uploads/` folders and initializes the aggregated store.

## Using the App

- Navigation lives in the left sidebar. Active pages are:
	- Products: list, add, edit, and delete products.
	- Business Owner Sessions: capture owner-level sessions covering their product portfolio.
	- Export Backup: download/restore the full data file.

### Import Products from CSV

- Place the catalog at uploads/Product Catalog 2c34aca9ecb38075ab7fcdbec29ce503.csv, then click “Import from CSV” in the sidebar.
- The importer creates missing products and pre-fills Business Owners’ product lists.

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
- Saves are deep-merged to preserve nested structures; each save updates `last_updated`.
- After saves, the UI refreshes automatically.

## Configuration Notes

- CSV path is defined as PRODUCT_CATALOG_FILE in app.py. Update it if your file name or location differs.
- Dependencies are listed in pyproject.toml and requirements.txt; Streamlit and Pandas are the only runtime libraries.

## Troubleshooting

- CSV not detected: ensure the file path and name match exactly under uploads/.
- Permission or write errors: verify the app has write access to the data/ directory.
- Virtual environment issues: re-create the venv and reinstall requirements.
