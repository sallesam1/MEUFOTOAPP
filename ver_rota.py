import os

base_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base_dir, 'app.py'), 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Encontrar a rota catalogo_poses
printing = False
for j, line in enumerate(lines):
    if 'catalogo' in line.lower() and 'def ' in line.lower():
        printing = True
    if printing:
        print('L' + str(j+1) + ': ' + line.rstrip())
        if j > 0 and printing and line.strip().startswith('def ') and 'catalogo' not in line.lower():
            break
        if printing and j > 0 and (line.strip().startswith('@app.route') and 'catalogo' not in line.lower()):
            break