import os
import re

base = os.path.dirname(os.path.abspath(__file__))
tpl_dir = os.path.join(base, 'templates')

MOBILE_CSS = """<style>
.hamburger{display:none;flex-direction:column;gap:5px;cursor:pointer;padding:10px;position:fixed;top:15px;left:15px;z-index:1001;background:#161b22;border-radius:6px;border:1px solid #30363d}
.hamburger span{width:25px;height:3px;background:#e6edf3;border-radius:2px;transition:0.3s}
.hamburger.active span:nth-child(1){transform:rotate(45deg) translate(6px,6px)}
.hamburger.active span:nth-child(2){opacity:0}
.hamburger.active span:nth-child(3){transform:rotate(-45deg) translate(6px,-6px)}
.sidebar-overlay{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.7);z-index:999}
.sidebar-overlay.active{display:block}
@media(max-width:768px){
.hamburger{display:flex!important}
.sidebar{transform:translateX(-100%)!important;width:280px!important;position:fixed!important;z-index:1000;transition:transform 0.3s ease}
.sidebar.active{transform:translateX(0)!important}
.sidebar-overlay.active{display:block}
.main-content,.content,.content-area,.main,.wrapper{margin-left:0!important;padding:1rem!important;padding-top:4rem!important}
.photo-grid,.grid-fotos,.galeria-grid,.cards-grid{grid-template-columns:repeat(2,1fr)!important;gap:0.8rem!important}
.btn{width:100%}
.stats-grid{grid-template-columns:1fr!important}
}
@media(max-width:480px){
.photo-grid,.grid-fotos,.galeria-grid,.cards-grid{grid-template-columns:1fr!important}
.sidebar{width:100%!important}
}
</style>"""

HAMBURGER_HTML = '\n<div class="hamburger" id="hamburger"><span></span><span></span><span></span></div>\n<div class="sidebar-overlay" id="sidebarOverlay"></div>\n'

JS = "\n<script>\n(function(){var h=document.getElementById('hamburger');var s=document.querySelector('.sidebar');var o=document.getElementById('sidebarOverlay');if(h&&s){h.addEventListener('click',function(){h.classList.toggle('active');s.classList.toggle('active');if(o)o.classList.toggle('active')})}if(o){o.addEventListener('click',function(){if(h)h.classList.remove('active');if(s)s.classList.remove('active');o.classList.remove('active')})}})();\nfunction togglePassword(btn){var i=btn.previousElementSibling;if(i.type==='password'){i.type='text';btn.textContent='\uD83D\uDE48'}else{i.type='password';btn.textContent='\uD83D\uDC41'}}\n</script>\n"

SIDEBAR_TPLS = ['admin.html','catalogo_categoria.html','catalogo_poses.html','galeria.html','planos.html','selecoes_poses.html']
PW_TPLS = ['login.html','registro.html']

for fname in sorted(os.listdir(tpl_dir)):
    if not fname.endswith('.html'):
        continue
    fpath = os.path.join(tpl_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    if fname in SIDEBAR_TPLS:
        if 'hamburger' not in content.lower():
            if '</head>' in content:
                content = content.replace('</head>', MOBILE_CSS + '\n</head>')
            elif '<head>' in content:
                content = content.replace('<head>', '<head>\n' + MOBILE_CSS)
            content = re.sub(r'(<body[^>]*>)', r'\1' + HAMBURGER_HTML, content)
            if '</body>' in content:
                content = content.replace('</body>', JS + '</body>')
            elif '</html>' in content:
                content = content.replace('</html>', JS + '\n</html>')

    if fname in PW_TPLS:
        if 'function togglePassword' not in content:
            pw_js = "\n<script>\nfunction togglePassword(btn){var i=btn.previousElementSibling;if(i.type==='password'){i.type='text';btn.textContent='\uD83D\uDE48'}else{i.type='password';btn.textContent='\uD83D\uDC41'}}\n</script>\n"
            if '</body>' in content:
                content = content.replace('</body>', pw_js + '</body>')
            elif '</html>' in content:
                content = content.replace('</html>', pw_js + '\n</html>')

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"OK: {fname}")
    else:
        print(f"SKIP: {fname}")

print("\nPronto! Reinicia o Flask e testa no celular.")