import json

with open('code.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f"Total cells: {len(nb['cells'])}")
for i, cell in enumerate(nb['cells']):
    ct = cell['cell_type']
    src = ''.join(cell['source'])[:100].replace('\n', ' | ')
    print(f"Cell {i}: [{ct}] {src}")
