import os

base = os.path.dirname(os.path.abspath(__file__))

# 1. CSS UNIVERSAL (override com !important)
css_fix = """/* MOBILE FIX UNIVERSAL - OVERRIDE TUDO */
.hamburger{display:none!important;flex-direction:column;gap:5px;cursor:pointer;padding:10px;position:fixed;top:15px;left:15px;z-index:99999;background:#161b22;border-radius:6px;border:1px solid #30363d}
.hamburger span{width:25px;height:3px;background:#e6edf3;border-radius:2px;transition:0.3s}
.hamburger.active span:nth-child(1){transform:rotate(45deg) translate(6px,6px)}
.hamburger.active span:nth-child(2){opacity:0}
.hamburger.active span:nth-child(3){transform:rotate(-45deg) translate(6px,-6px)}
.sb-overlay{display:none!important;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.7);z-index:99998}
.sb-overlay.active{display:block!important}
.pw-wrapper{position:relative!important;width:100%!important}
.pw-toggle{position:absolute!important;right:12px!important;top:50%!important;transform:translateY(-50%)!important;cursor:pointer!important;background:none!important;border:none!important;color:#8b949e!important;font-size:18px!important;z-index:10!important;padding:0!important}
.pw-toggle:hover{color:#e6edf3!important}

@media(max-width:768px){
.hamburger{display:flex!important}
.sidebar{transform:translateX(-100%)!important;position:fixed!important;z-index:99999!important;width:280px!important;max-width:85vw!important;transition:transform 0.3s ease!important}
.sidebar.active{transform:translateX(0)!important}
.sb-overlay.active{display:block!important}
.main-content,.content,.content-area,.main,.wrapper,.container{
margin-left:0!important;padding:1rem!important;padding-top:4.5rem!important;width:100%!important;max-width:100%!important}
.photo-grid,.grid-fotos,.galeria-grid,.cards-grid,.grid{
grid-template-columns:repeat(2,1fr)!important;gap:0.8rem!important}
.btn{width:auto!important;min-width:120px!important}
.stats-grid,.stats{grid-template-columns:repeat(2,1fr)!important}
table{font-size:0.85rem!important}
h1,h2,.page-title{font-size:1.3rem!important}
}

@media(max-width:480px){
.photo-grid,.grid-fotos,.galeria-grid,.cards-grid,.grid{
grid-template-columns:1fr!important}
.stats-grid,.stats{grid-template-columns:1fr!important}
.sidebar{width:100%!important}
}
"""

css_dir = os.path.join(base, 'static', 'css')
os.makedirs(css_dir, exist_ok=True)
with open(os.path.join(css_dir, 'mobile-fix.css'), 'w', encoding='utf-8') as f:
    f.write(css_fix)
print("OK: mobile-fix.css criado")

# 2. JS UNIVERSAL (faz tudo via JavaScript)
js_fix = """// MOBILE FIX UNIVERSAL
(function(){
    // Cria hamburger e overlay
    var body = document.body || document.documentElement;
    if(!document.getElementById('fixHamburger')){
        var h = document.createElement('div');
        h.id = 'fixHamburger';
        h.className = 'hamburger';
        h.innerHTML = '<span></span><span></span><span></span>';
        h.onclick = function(){
            h.classList.toggle('active');
            var sb = document.querySelector('.sidebar');
            if(sb) sb.classList.toggle('active');
            var ov = document.getElementById('fixOverlay');
            if(ov) ov.classList.toggle('active');
        };
        body.insertBefore(h, body.firstChild);
        
        var ov = document.createElement('div');
        ov.id = 'fixOverlay';
        ov.className = 'sb-overlay';
        ov.onclick = function(){
            h.classList.remove('active');
            var sb = document.querySelector('.sidebar');
            if(sb) sb.classList.remove('active');
            ov.classList.remove('active');
        };
        body.insertBefore(ov, body.firstChild);
    }
    
    // Password toggle - encontra todos os inputs password
    var pwInputs = document.querySelectorAll('input[type="password"]');
    pwInputs.forEach(function(input){
        if(input.getAttribute('data-pw-fixed')) return;
        input.setAttribute('data-pw-fixed', '1');
        
        // Se ja tem wrapper, pula
        if(input.parentNode && input.parentNode.className === 'pw-wrapper') return;
        
        var wrapper = document.createElement('div');
        wrapper.className = 'pw-wrapper';
        
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'pw-toggle';
        btn.innerHTML = '&#128065;';
        btn.onclick = function(e){
            e.preventDefault();
            if(input.type === 'password'){
                input.type = 'text';
                btn.innerHTML = '&#128584;';
            } else {
                input.type = 'password';
                btn.innerHTML = '&#128065;';
            }
        };
        
        input.parentNode.insertBefore(wrapper, input);
        wrapper.appendChild(input);
        wrapper.appendChild(btn);
    });
})();
"""

js_dir = os.path.join(base, 'static', 'js')
os.makedirs(js_dir, exist_ok=True)
with open(os.path.join(js_dir, 'mobile-fix.js'), 'w', encoding='utf-8') as f:
    f.write(js_fix)
print("OK: mobile-fix.js criado")

# 3. INJETAR em TODOS os templates
import re
tpl_dir = os.path.join(base, 'templates')
css_link = '<link rel="stylesheet" href="/static/css/mobile-fix.css">'
js_link = '<script src="/static/js/mobile-fix.js"></script>'

for fname in sorted(os.listdir(tpl_dir)):
    if not fname.endswith('.html') or fname == 'base.html':
        continue
    
    fpath = os.path.join(tpl_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    
    # Adicionar CSS
    if 'mobile-fix.css' not in content:
        if '</head>' in content:
            content = content.replace('</head>', css_link + '\n</head>')
        elif '<head>' in content:
            content = content.replace('<head>', '<head>\n' + css_link)
        elif '<html' in content:
            content = content.replace('<html', '<head>' + css_link + '</head>\n<html')
        else:
            content = css_link + '\n' + content
    
    # Adicionar JS
    if 'mobile-fix.js' not in content:
        if '</body>' in content:
            content = content.replace('</body>', js_link + '\n</body>')
        elif '</html>' in content:
            content = content.replace('</html>', js_link + '\n</html>')
        else:
            content = content + '\n' + js_link
    
    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"OK: {fname}")
    else:
        print(f"SKIP: {fname}")

# 4. Tambem adicionar no base.html
base_path_tpl = os.path.join(tpl_dir, 'base.html')
with open(base_path_tpl, 'r', encoding='utf-8') as f:
    content = f.read()

if 'mobile-fix.css' not in content:
    if '</head>' in content:
        content = content.replace('</head>', css_link + '\n</head>')
    with open(base_path_tpl, 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK: base.html")

if 'mobile-fix.js' not in content:
    if '</body>' in content:
        content = content.replace('</body>', js_link + '\n</body>')
    with open(base_path_tpl, 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK: base.html (JS)")

print("\nTudo pronto! Reinicia o Flask e testa.")