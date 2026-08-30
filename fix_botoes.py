import os
import re

base = os.path.dirname(os.path.abspath(__file__))
tpl_dir = os.path.join(base, 'templates')

# 1. LIMPAR dashboard.html - remover link/script fora do lugar
fpath = os.path.join(tpl_dir, 'dashboard.html')
with open(fpath, 'r', encoding='utf-8') as f:
    content = f.read()

# Remover link e script soltos fora dos blocks
content = content.replace('<link rel="stylesheet" href="/static/css/mobile-fix.css">\n', '')
content = content.replace('<script src="/static/js/mobile-fix.js"></script>\n', '')

# Adicionar class="btn" no botao Abrir
content = content.replace('class="btn-primary"', 'class="btn btn-primary"')

with open(fpath, 'w', encoding='utf-8') as f:
    f.write(content)
print("OK: dashboard.html corrigido")

# 2. Limpar outros templates que tambem tem link/script antes do extends
for fname in sorted(os.listdir(tpl_dir)):
    if not fname.endswith('.html') or fname == 'base.html':
        continue
    fp = os.path.join(tpl_dir, fname)
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()
    
    original = c
    # Remove link solto antes de extends
    c = re.sub(r'<link[^>]*mobile-fix\.css[^>]*>\s*(?=\{%\s*extends)', '', c)
    # Remove script solto depois de endblock
    c = re.sub(r'(?<=\{%\s*endblock\s*%\})\s*<script[^>]*mobile-fix\.js[^>]*></script>', '', c)
    
    # Adicionar class="btn" onde so tem btn-primary ou btn-danger
    c = re.sub(r'class="btn-primary"', 'class="btn btn-primary"', c)
    c = re.sub(r'class="btn-danger"', 'class="btn btn-danger"', c)
    c = re.sub(r'class="btn-secondary"', 'class="btn btn-secondary"', c)
    
    if c != original:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"OK: {fname}")

# 3. Atualizar mobile-fix.css com regras para btn-primary sem .btn
css_path = os.path.join(base, 'static', 'css', 'mobile-fix.css')
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Adicionar regras para btn-primary/btn-danger sozinhos
extra = """
/* CORRIGIR BOTOES SEM CLASS btn */
.btn-primary,.btn-danger,.btn-secondary{
display:inline-flex!important;align-items:center!important;justify-content:center!important;
padding:0.6rem 1.2rem!important;border-radius:8px!important;font-weight:600!important;
cursor:pointer!important;border:1px solid transparent!important;transition:0.2s!important;gap:8px!important;
width:auto!important;text-decoration:none!important
}
"""

if 'BOTOES SEM CLASS btn' not in css:
    css = css + extra
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css)
    print("OK: mobile-fix.css atualizado com regras para btn-primary sozinho")

print("\nPronto! Reinicia o Flask e aperta Ctrl+Shift+R.")