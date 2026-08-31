import os
import re

base = os.path.dirname(os.path.abspath(__file__))
tpl = os.path.join(base, 'templates', 'base.html')

with open(tpl, 'r', encoding='utf-8') as f:
    conteudo = f.read()

if 'lightbox' in conteudo:
    print('Lightbox ja existe no base.html.')
else:
    css = """<style>
.lightbox{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.9);z-index:9999;justify-content:center;align-items:center;cursor:pointer}
.lightbox img{max-width:92%;max-height:92%;border-radius:8px;box-shadow:0 0 30px rgba(0,0,0,.6)}
.lightbox .close{position:absolute;top:20px;right:30px;color:#fff;font-size:40px;font-weight:700;cursor:pointer;line-height:1}
</style>"""
    html = """<div class="lightbox" id="lightbox" onclick="closeLightbox()">
<span class="close">&times;</span>
<img id="lightboxImg" src="" alt="">
</div>"""
    js = """<script>
function openLightbox(src){var lb=document.getElementById('lightbox');var img=document.getElementById('lightboxImg');img.src=src;lb.style.display='flex';}
function closeLightbox(){document.getElementById('lightbox').style.display='none';}
</script>"""

    if re.search(r'</head>', conteudo, re.IGNORECASE):
        conteudo = re.sub(r'</head>', css + '\n</head>', conteudo, count=1, flags=re.IGNORECASE)
    else:
        conteudo = css + '\n' + conteudo

    if re.search(r'</body>', conteudo, re.IGNORECASE):
        conteudo = re.sub(r'</body>', html + '\n' + js + '\n</body>', conteudo, count=1, flags=re.IGNORECASE)
    else:
        conteudo = conteudo + '\n' + html + '\n' + js

    with open(tpl, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    print('OK! Funcao de ampliar foto adicionada com sucesso.')