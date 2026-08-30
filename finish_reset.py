import os
import re

base = os.path.dirname(os.path.abspath(__file__))
tpl_dir = os.path.join(base, 'templates')
css_dir = os.path.join(base, 'static', 'css')
js_dir = os.path.join(base, 'static', 'js')

# 1. CRIAR mobile-fix.js (usando HTML entities no lugar de emojis diretos)
js_content = """(function(){
// Hamburger
var h=document.getElementById('hamburger');
var s=document.querySelector('.sidebar');
var o=document.getElementById('sidebarOverlay');
if(h&&s){
h.addEventListener('click',function(){
h.classList.toggle('active');
s.classList.toggle('active');
if(o)o.classList.toggle('active');
});
}
if(o){
o.addEventListener('click',function(){
h.classList.remove('active');
s.classList.remove('active');
o.classList.remove('active');
});
}
// Password toggle
document.querySelectorAll('input[type="password"]').forEach(function(input){
if(input.getAttribute('data-pw'))return;
input.setAttribute('data-pw','1');
input.classList.add('pw-input');
var wrap=document.createElement('div');
wrap.className='pw-wrap';
input.parentNode.insertBefore(wrap,input);
wrap.appendChild(input);
var btn=document.createElement('button');
btn.type='button';
btn.className='pw-toggle';
btn.innerHTML='&#128065;';
btn.onclick=function(e){
e.preventDefault();
if(input.type==='password'){
input.type='text';
btn.innerHTML='&#128584;';
}else{
input.type='password';
btn.innerHTML='&#128065;';
}
};
wrap.appendChild(btn);
});
})();
"""

os.makedirs(js_dir, exist_ok=True)
with open(os.path.join(js_dir, 'mobile-fix.js'), 'w', encoding='utf-8') as f:
    f.write(js_content)
print("OK: mobile-fix.js criado")

# 2. INJETAR no base.html
base_tpl = os.path.join(tpl_dir, 'base.html')
with open(base_tpl, 'r', encoding='utf-8') as f:
    c = f.read()

if 'style.css' not in c and '</head>' in c:
    c = c.replace('</head>', '<link rel="stylesheet" href="/static/css/style.css">\n</head>')

if 'hamburger' not in c:
    ham = '\n<div class="hamburger" id="hamburger"><span></span><span></span><span></span></div>\n<div class="sidebar-overlay" id="sidebarOverlay"></div>\n'
    c = re.sub(r'(<body[^>]*>)', r'\1' + ham, c)

if 'mobile-fix.js' not in c:
    js_tag = '\n<script src="/static/js/mobile-fix.js"></script>\n'
    if '</body>' in c:
        c = c.replace('</body>', js_tag + '</body>')
    else:
        c = c + js_tag

with open(base_tpl, 'w', encoding='utf-8') as f:
    f.write(c)
print("OK: base.html")

# 3. Injetar em templates standalone
standalone = ['admin.html','catalogo_categoria.html','catalogo_poses.html','galeria.html',
              'login.html','planos.html','portfolio_public.html','public_catalog.html',
              'registro.html','selecoes_poses.html','cliente.html','add_pose.html']

for fname in standalone:
    fpath = os.path.join(tpl_dir, fname)
    if not os.path.exists(fpath):
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # CSS
    if 'style.css' not in c:
        if '</head>' in c:
            c = c.replace('</head>', '<link rel="stylesheet" href="/static/css/style.css">\n</head>')
        elif '<html' in c:
            c = re.sub(r'(<html[^>]*>)', r'\1\n<head><link rel="stylesheet" href="/static/css/style.css"></head>', c)
        else:
            c = '<link rel="stylesheet" href="/static/css/style.css">\n' + c
    
    # Hamburger (so se tem sidebar)
    if 'sidebar' in c.lower() and 'hamburger' not in c.lower():
        ham = '\n<div class="hamburger" id="hamburger"><span></span><span></span><span></span></div>\n<div class="sidebar-overlay" id="sidebarOverlay"></div>\n'
        if '<body' in c:
            c = re.sub(r'(<body[^>]*>)', r'\1' + ham, c)
        else:
            c = ham + c
    
    # JS
    if 'mobile-fix.js' not in c:
        js_tag = '\n<script src="/static/js/mobile-fix.js"></script>\n'
        if '</body>' in c:
            c = c.replace('</body>', js_tag + '</body>')
        elif '</html>' in c:
            c = c.replace('</html>', js_tag + '</html>')
        else:
            c = c + js_tag
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"OK: {fname}")

print("\nPronto! Reinicia o Flask e aperta Ctrl+Shift+R.")