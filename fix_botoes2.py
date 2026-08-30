import os
import re

base = os.path.dirname(os.path.abspath(__file__))
tpl_dir = os.path.join(base, 'templates')

# 1. Limpar outros templates (versao sem lookbehind)
for fname in sorted(os.listdir(tpl_dir)):
    if not fname.endswith('.html') or fname == 'base.html' or fname == 'dashboard.html':
        continue
    fp = os.path.join(tpl_dir, fname)
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()
    
    original = c
    # Remove link solto antes de extends
    c = re.sub(r'<link[^>]*mobile-fix\.css[^>]*>\s*(?=\{%\s*extends)', '', c)
    # Remove script solto depois de endblock (sem lookbehind)
    c = re.sub(r'(\{%\s*endblock\s*%\})\s*<script[^>]*mobile-fix\.js[^>]*></script>', r'\1', c)
    
    # Adicionar class="btn" onde so tem btn-primary ou btn-danger
    c = re.sub(r'class="btn-primary"', 'class="btn btn-primary"', c)
    c = re.sub(r'class="btn-danger"', 'class="btn btn-danger"', c)
    c = re.sub(r'class="btn-secondary"', 'class="btn btn-secondary"', c)
    
    if c != original:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"OK: {fname}")

# 2. Atualizar mobile-fix.css
css_path = os.path.join(base, 'static', 'css', 'mobile-fix.css')
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

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
    print("OK: mobile-fix.css atualizado")

print("\nPronto! Reinicia o Flask e aperta Ctrl+Shift+R.")