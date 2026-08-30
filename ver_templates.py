import os

base_dir = os.path.dirname(os.path.abspath(__file__))

for fname in ['templates/base.html', 'templates/catalogo_poses.html']:
    filepath = os.path.join(base_dir, fname)
    print('=' * 60)
    print('ARQUIVO: ' + fname)
    print('=' * 60)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        lines = content.split('\n')
        for j, line in enumerate(lines):
            print('L' + str(j+1) + ': ' + line[:120])
        print('\n')
    else:
        print('NAO ENCONTRADO\n')