# Copilot Instructions for This Repo

These project-specific notes help AI coding agents work productively in this codebase. Keep guidance concrete and tied to current code.

## Overview
- Stack: Python (>=3.9), Streamlit, Pandas. Primary entry: [app.py](app.py). Minimal [main.py](main.py).
- Run locally: `streamlit run app.py` from repo root. Dependencies defined in [pyproject.toml](pyproject.toml) and [requirements.txt](requirements.txt).
- Persistence: Single aggregated JSON at [data/aggregated.json](data/aggregated.json). Folders auto-created by `ensure_dirs()`.

## Architecture & Data Flow
- All logic lives in [app.py](app.py): helpers + Streamlit pages.
- Key helpers:
  - `ensure_dirs()`: creates `uploads/` and `data/`, initializes aggregated.json.
  - `load_aggregated_data()` / `save_aggregated_data(data)`: read/write the single JSON store.
  - `get_empty_product_template()` / `get_empty_business_owner_template()`: canonical schemas for persisted objects.
  - `save_product_data(product_id, product_data)`: deep-merges fields into `products[product_id]` and stamps `last_updated`.
  - `save_business_owner_data(owner_name, owner_data)`: writes owner session and stamps `last_updated`.
  - `import_products_from_csv()`: populates products and pre-fills owners from the product catalog CSV.
- Data model in aggregated.json:
  - `products: { <product_id>: <product_obj> }` with nested `technical_session.part*` sections and `simple_edit`.
  - `business_owners: { <owner_name>: <owner_obj> }` with nested parts (context, portfolio, cross-product, delivery, future state, wrap-up).

## UI & Navigation (Streamlit)
- Navigation via `st.session_state['page']` set from sidebar buttons.
- Active pages:
  - "Products": list, edit, and delete products; color-coded by business owner (`get_owner_color()`).
  - "Add Product": creates a product and jumps to its session editor.
  - "Product Operator/Developer Session": comprehensive nested form that saves under `technical_session`.
  - "Business Owner Sessions": groups products by owner (from CSV) and saves owner-level session data.
  - "Export Backup": download/restore the full aggregated JSON.
- Note: There is a second "Products" block later in [app.py](app.py) that appears vestigial; the first "Products" implementation is the active one.

## CSV Import
- Catalog file path is fixed: [uploads/Product Catalog 2c34aca9ecb38075ab7fcdbec29ce503.csv](uploads/Product%20Catalog%202c34aca9ecb38075ab7fcdbec29ce503.csv).
- `load_products_from_csv()` expectations:
  - Skips header and empty rows; ignores platform rows where name contains "Platform" and column 2 is "N/A".
  - Uses specific indices: 0 `product_name`, 1 `workstream`, 3 `business_owner`, 4 `existing_users`, 6 `primary_operator`, 10 `primary_developer`.
- `import_products_from_csv()`:
  - Creates products missing in aggregated.json using the full product template, then overlays CSV fields and `product_id = slugify(product_name)`.
  - Keeps `business_owners[owner].products_covered` in sync with products.

## Conventions & Patterns
- IDs: `product_id` is `slugify(product_name)`; persist it on save.
- Writes: Always use `save_product_data()` / `save_business_owner_data()` so timestamps and deep-merge semantics are preserved.
- UI state: After saves, call `st.rerun()` to refresh the page.
- Quotes input: one quote per line using `Speaker | timestamp | quote`; parsed into list objects at save time.
- Colors: business owner chips use `get_owner_color(owner_name)` for consistent color mapping.

## Common Tasks (How-To)
- Add a new product field:
  1) Add default in `get_empty_product_template()`.
  2) Add form control in the "Product Operator/Developer Session" UI and include it in the `product_data` payload before `save_product_data()`.
- Extend business owner schema:
  1) Add default in `get_empty_business_owner_template()`.
  2) Add form control in "Business Owner Sessions" and include in `owner_data` before `save_business_owner_data()`.
- Map an additional CSV column:
  1) Update `load_products_from_csv()` to read the new index/column.
  2) If it belongs in products, ensure `import_products_from_csv()` copies it into the product object.
- Add a new page:
  1) Add a sidebar button and route by setting `st.session_state['page']`.
  2) Implement the page block in the main `if/elif` routing and use forms + `st.rerun()` like existing pages.

## Running & Debugging
- Install and run:
  - `pip install -r requirements.txt`
  - `streamlit run app.py`
- Data folders are created on first run; if the CSV path differs, update `PRODUCT_CATALOG_FILE` in [app.py](app.py).
- README is outdated for storage layout (mentions per-session files); source of truth is aggregated.json and the helpers above.
