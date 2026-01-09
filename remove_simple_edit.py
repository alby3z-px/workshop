#!/usr/bin/env python3
"""Remove simple_edit sections from aggregated.json"""

import json
from pathlib import Path

DATA_DIR = Path("data")
AGGREGATED_FILE = DATA_DIR / "aggregated.json"

with open(AGGREGATED_FILE, 'r') as f:
    data = json.load(f)

# Remove simple_edit from all products
removed_count = 0
for product_id, product in data.get('products', {}).items():
    if 'simple_edit' in product:
        del product['simple_edit']
        removed_count += 1

with open(AGGREGATED_FILE, 'w') as f:
    json.dump(data, f, indent=2)

print(f'✅ Removed simple_edit from {removed_count} products')
