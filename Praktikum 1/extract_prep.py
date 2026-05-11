import json

with open('code.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Show cells 0-16 (Data Preparation) with full source and output summary
for i in range(min(17, len(nb['cells']))):
    cell = nb['cells'][i]
    ct = cell['cell_type']
    src = ''.join(cell['source'])
    
    print(f"{'='*70}")
    print(f"CELL {i} [{ct}]")
    print(f"{'='*70}")
    print(src)
    
    # Show outputs summary
    if 'outputs' in cell and cell['outputs']:
        for out in cell['outputs']:
            if out.get('output_type') == 'stream':
                text = ''.join(out.get('text', []))
                print(f"\n--- OUTPUT ---")
                print(text[:2000])
            elif out.get('output_type') == 'execute_result':
                if 'text/plain' in out.get('data', {}):
                    text = ''.join(out['data']['text/plain'])
                    print(f"\n--- RESULT ---")
                    print(text[:1000])
    print()
