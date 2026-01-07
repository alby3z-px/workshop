# Workshop Product & Session Capture (Streamlit)

A lightweight Streamlit app to capture product information and workshop notes across Operators/Developers and Business Owners. Data is persisted in a single aggregated JSON file for simplicity and easy backup/restore.

## Quick Start

Pick the fastest path for your setup. The app auto-creates `data/` and `uploads/` on first run.

### Option A — uv (fastest, no manual venv)

If you don't have `uv` yet:

macOS/Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows (PowerShell):

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

Run the app (reads dependencies from pyproject.toml):

```bash
uv sync
uv run streamlit run app.py
```

Notes:
- `uv sync` creates/updates a local environment from `pyproject.toml`.
- `uv run` executes in that environment; no activation needed.

### Option B — Conda

Create and activate an environment, then use pip inside it:

```bash
conda create -n workshop python=3.12 -y
conda activate workshop
python -m pip install -r requirements.txt
streamlit run app.py
```

Tip: Using mamba? Replace `conda create` with `mamba create`.

### Option C — Python venv (manual)

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
streamlit run app.py
```

Windows (PowerShell):

```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
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
- `uv` not found: install via the commands above.
- `conda` not found: install Miniconda/Anaconda, or use Mambaforge.
- `python3` not found on macOS: install Python 3 (e.g., `brew install python@3.12`). If Homebrew is missing: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
- Why `.venv` isn’t in the repo: virtualenvs are OS/architecture-specific and large; recreating from `pyproject.toml`/`requirements.txt` is reliable and quick.
