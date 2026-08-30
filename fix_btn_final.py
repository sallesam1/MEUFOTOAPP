import os

base = os.path.dirname(os.path.abspath(__file__))
css_path = os.path.join(base, 'static', 'css', 'style.css')

with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Trocar a regra .btn para incluir btn-primary, btn-danger, btn-secondary
css = css.replace(
    '.btn{display:inline-flex;align-items:center;justify-content:center;padding:.6rem 1.2rem;border-radius:8px;font-weight:600;cursor:pointer;border:1px solid transparent;transition:.2s;gap:8px;width:auto;text-decoration:none}',
    '.btn,.btn-primary,.btn-danger,.btn-secondary{display:inline-flex;align-items:center;justify-content:center;padding:.6rem 1.2rem;border-radius:8px;font-weight:600;cursor:pointer;border:1px solid transparent;transition:.2s;gap:8px;width:auto;text-decoration:none}'
)

# Tambem garantir que a regra duplicada antiga seja corrigida
css = css.replace(
    '.btn { display: inline-flex; align-items: center; justify-content: center; padding: 0.6rem 1.2rem; border-radius: 8px; font-weight: 600; cursor: pointer; border: 1px solid transparent; transition: 0.2s; gap: 8px; width: auto; }',
    '.btn, .btn-primary, .btn-danger, .btn-secondary { display: inline-flex; align-items: center; justify-content: center; padding: 0.6rem 1.2rem; border-radius: 8px; font-weight: 600; cursor: pointer; border: 1px solid transparent; transition: 0.2s; gap: 8px; width: auto; }'
)

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

print("OK! Botoes corrigidos no style.css")
print("Reinicia o Flask e aperta Ctrl+Shift+R")