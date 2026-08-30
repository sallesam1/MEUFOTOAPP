import os
import re

base = os.path.dirname(os.path.abspath(__file__))

# 1. Mostrar dashboard.html
tpl = os.path.join(base, 'templates', 'dashboard.html')
if os.path.exists(tpl):
    with open(tpl, 'r', encoding='utf-8') as f:
        content = f.read()
    print("=== DASHBOARD.HTML ===")
    print(content)
else:
    print("dashboard.html NAO ENCONTRADO")

# 2. Mostrar regras .btn do style.css
css_path = os.path.join(base, 'static', 'css', 'style.css')
if os.path.exists(css_path):
    with open(css_path, 'r', encoding='utf-8') as f:
        css = f.read()
    print("\n=== REGRAS .btn NO style.css ===")
    matches = re.findall(r'\.btn[^{]*\{[^}]*\}', css)
    for m in matches:
        print(m)
        print("---")

# 3. Mostrar regras .btn do mobile-fix.css
fix_path = os.path.join(base, 'static', 'css', 'mobile-fix.css')
if os.path.exists(fix_path):
    with open(fix_path, 'r', encoding='utf-8') as f:
        fix_css = f.read()
    print("\n=== REGRAS .btn NO mobile-fix.css ===")
    matches = re.findall(r'\.btn[^{]*\{[^}]*\}', fix_css)
    for m in matches:
        print(m)
        print("---")

# 4. Mostrar regras .stats no style.css
print("\n=== REGRAS .stats NO style.css ===")
matches = re.findall(r'\.stats[^{]*\{[^}]*\}', css)
for m in matches:
    print(m)
    print("---")