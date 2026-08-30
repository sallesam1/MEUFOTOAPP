import os
import re

base = os.path.dirname(os.path.abspath(__file__))
tpl_dir = os.path.join(base, 'templates')

# 1. REMOVER OS OLHINHOS DUPLICADOS (injetados pelo update_mobile.py)
for fname in sorted(os.listdir(tpl_dir)):
    if not fname.endswith('.html'):
        continue
    fpath = os.path.join(tpl_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # Remove wrappers HTML injetados pelo update_mobile.py
    # Padrão: <div class="password-wrapper"><input ... class="password-input ..."><button ...>👁</button></div>
    content = re.sub(
        r'<div class="password-wrapper">\s*(<input[^>]*>)\s*<button[^>]*class="password-toggle"[^>]*>.*?</button>\s*</div>',
        r'\1',
        content,
        flags=re.DOTALL
    )

    # Remove a classe password-input dos inputs (o JS do fix_final cuida disso)
    content = content.replace('password-input ', '')
    content = content.replace(' password-input', '')
    content = content.replace('class="password-input"', '')

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Olhinho duplicado removido: {fname}")

# 2. ATUALIZAR mobile-fix.css com correcao de botoes
css_fix = """/* MOBILE FIX UNIVERSAL */
.hamburger{display:none!important;flex-direction:column;gap:5px;cursor:pointer;padding:10px;position:fixed;top:15px;left:15px;z-index:99999;background:#161b22;border-radius:6px;border:1px solid #30363d}
.hamburger span{width:25px;height:3px;background:#e6edf3;border-radius:2px;transition:0.3s}
.hamburger.active span:nth-child(1){transform:rotate(45deg) translate(6px,6px)}
.hamburger.active span:nth-child(2){opacity:0}
.hamburger.active span:nth-child(3){transform:rotate(-45deg) translate(6px,-6px)}
.sb-overlay{display:none!important;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.7);z-index:99998}
.sb-overlay.active{display:block!important}
.pw-wrapper{position:relative!important;width:100%!important}
.pw-toggle{position:absolute!important;right:12px!important;top:50%!important;transform:translateY(-50%)!important;cursor:pointer!important;background:none!important;border:none!important;color:#8b949e!important;font-size:18px!important;z-index:10!important;padding:0!important;width:auto!important}
.pw-toggle:hover{color:#e6edf3!important}

/* CORRIGIR BOTOES NO DESKTOP */
.btn{width:auto!important;display:inline-flex!important}
.btn-block{width:100%!important}

@media(max-width:768px){
.hamburger{display:flex!important}
.sidebar{transform:translateX(-100%)!important;position:fixed!important;z-index:99999!important;width:280px!important;max-width:85vw!important;transition:transform 0.3s ease!important}
.sidebar.active{transform:translateX(0)!important}
.sb-overlay.active{display:block!important}
.main-content,.content,.content-area,.main,.wrapper,.container{
margin-left:0!important;padding:1rem!important;padding-top:4.5rem!important;width:100%!important;max-width:100%!important}
.photo-grid,.grid-fotos,.galeria-grid,.cards-grid,.grid{
grid-template-columns:repeat(2,1fr)!important;gap:0.8rem!important}
.btn{width:auto!important;min-width:100px!important}
.btn-block{width:100%!important}
.stats-grid,.stats{grid-template-columns:repeat(2,1fr)!important}
table{font-size:0.85rem!important}
h1,h2,.page-title{font-size:1.3rem!important}
}

@media(max-width:480px){
.photo-grid,.grid-fotos,.galeria-grid,.cards-grid,.grid{
grid-template-columns:1fr!important}
.stats-grid,.stats{grid-template-columns:1fr!important}
.sidebar{width:100%!important}
.btn{width:100%!important}
}
"""

css_dir = os.path.join(base, 'static', 'css')
with open(os.path.join(css_dir, 'mobile-fix.css'), 'w', encoding='utf-8') as f:
    f.write(css_fix)
print("mobile-fix.css atualizado com correcao de botoes")

# 3. CORRIGIR style.css - remover width:100% dos botoes no desktop
style_path = os.path.join(css_dir, 'style.css')
if os.path.exists(style_path):
    with open(style_path, 'r', encoding='utf-8') as f:
        css = f.read()
    
    # Remover .btn { width: 100% } que esta fora de media query (se existir)
    css = re.sub(r'\.btn\s*\{[^}]*width:\s*100%[^}]*\}', '.btn { display: inline-flex; align-items: center; justify-content: center; padding: 0.6rem 1.2rem; border-radius: 8px; font-weight: 600; cursor: pointer; border: 1px solid transparent; transition: 0.2s; gap: 8px; width: auto; }', css)
    
    with open(style_path, 'w', encoding='utf-8') as f:
        f.write(css)
    print("style.css corrigido (botoes width:auto no desktop)")

print("\nPronto! Reinicia o Flask (Ctrl+C depois python app.py) e aperta Ctrl+Shift+R.")