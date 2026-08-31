import os

base = os.path.dirname(os.path.abspath(__file__))

# ===== 1) CORRIGIR PORTFOLIO.HTML =====
tpl = os.path.join(base, 'templates', 'portfolio.html')
with open(tpl, 'r', encoding='utf-8') as f:
    conteudo = f.read()

novo_bloco = """<div style="display:flex;gap:8px;flex-wrap:wrap;">
{% if item.before_path %}
<div style="position:relative;display:inline-block;">
<p style="position:absolute;top:8px;left:8px;background:rgba(0,0,0,.75);color:#fff;padding:4px 10px;border-radius:4px;font-size:12px;font-weight:700;z-index:5;margin:0;">ANTES</p>
<img src="{{ url_for('serve_wm', filename=item.before_path) }}" style="width:200px;border-radius:8px;cursor:pointer;display:block;" onclick="openLightbox(this.src)">
</div>
{% endif %}
{% if item.after_path %}
<div style="position:relative;display:inline-block;">
<p style="position:absolute;top:8px;right:8px;background:rgba(0,0,0,.75);color:#fff;padding:4px 10px;border-radius:4px;font-size:12px;font-weight:700;z-index:5;margin:0;">DEPOIS</p>
<img src="{{ url_for('serve_wm', filename=item.after_path) }}" style="width:200px;border-radius:8px;cursor:pointer;display:block;" onclick="openLightbox(this.src)">
</div>
{% endif %}
</div>"""

import re
# Troca o bloco antigo (do display:flex até o </div> que fecha) pelo novo
padrao = re.compile(r'<div style="display:flex;gap:8px;flex-wrap:wrap;">.*?</div>\s*</div>\s*</div>', re.DOTALL)
if padrao.search(conteudo):
    conteudo = padrao.sub(novo_bloco, conteudo, count=1)
    with open(tpl, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    print('OK! Etiquetas ANTES/DEPOIS agora ficam por cima da foto.')
else:
    print('AVISO: nao encontrei o bloco de fotos no portfolio.html.')

# ===== 2) CRIAR A FUNCAO QUE AMPLIA A FOTO (LIGHTBOX) =====
base_tpl = os.path.join(base, 'templates', 'base.html')
with open(base_tpl, 'r', encoding='utf-8') as f:
    base_conteudo = f.read()

# CSS do lightbox
lightbox_css = """<style>
.lightbox{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.9);z-index:9999;justify-content:center;align-items:center;cursor:pointer}
.lightbox img{max-width:92%;max-height:92%;border-radius:8px;box-shadow:0 0 30px rgba(0,0,0,.6)}
.lightbox .close{position:absolute;top:20px;right:30px;color:#fff;font-size:40px;font-weight:700;cursor:pointer;line-height:1}
</style>"""

# HTML do lightbox
lightbox_html = """<div class="lightbox" id="lightbox" onclick="closeLightbox()">
<span class="close">&times;</span>
<img id="lightboxImg" src="" alt="">
</div>"""

# JS da funcao
lightbox_js = """<script>
function openLightbox(src){var lb=document.getElementById('lightbox');var img=document.getElementById('lightboxImg');img.src=src;lb.style.display='flex';}
function closeLightbox(){document.getElementById('lightbox').style.display='none';}
</script>"""

mudou = False
if 'lightbox' not in base_conteudo:
    base_conteudo = base_conteudo.replace('</head>', lightbox_css + '\n</head>')
    base_conteudo = base_conteudo.replace('</body>', lightbox_html + '\n' + lightbox_js + '\n</body>')
    mudou = True

if mudou:
    with open(base_tpl, 'w', encoding='utf-8') as f:
        f.write(base_conteudo)
    print('OK! Funcao de ampliar foto criada (lightbox).')
else:
    print('Lightbox ja existe no base.html.')