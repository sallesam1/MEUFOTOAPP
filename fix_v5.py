import os

base = os.path.dirname(os.path.abspath(__file__))
tpl = os.path.join(base, 'templates')
app_path = os.path.join(base, 'app.py')
wm_path = os.path.join(base, 'watermark.py')

# ===== 1. FIX app.py: galeria_id -> gid =====
with open(app_path, 'r', encoding='utf-8') as f:
    code = f.read()
patches = 0

if "url_for('galeria', galeria_id=" in code:
    code = code.replace("url_for('galeria', galeria_id=", "url_for('galeria', gid=")
    patches += 1
    print('  OK: galeria_id -> gid')
else:
    print('  SKIP: no galeria_id found')

# Also check for share_token issue in nova_galeria
if 'def nova_galeria' in code and 'share_token' not in code.split('def nova_galeria')[1].split('def ')[0]:
    # Add share_token generation if missing
    code = code.replace(
        'db.session.add(g)\n        db.session.commit()',
        'g.share_token = secrets.token_urlsafe(16)\n        db.session.add(g)\n        db.session.commit()'
    )
    patches += 1
    print('  OK: share_token added')

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(code)
print(f'app.py: {patches} patches')

# ===== 2. FIX watermark.py: less pollution =====
wm_code = """from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import io

def get_watermarked_bytes(filepath, text='MeuFotoApp', color='#ffffff', opacity=30, position='diagonal', stroke=False, logo_path=None):
    img = Image.open(filepath).convert('RGBA')
    r = int(color[1:3], 16) if color.startswith('#') and len(color) >= 7 else 255
    g = int(color[3:5], 16) if color.startswith('#') and len(color) >= 7 else 255
    b = int(color[5:7], 16) if color.startswith('#') and len(color) >= 7 else 255
    alpha = int(opacity * 255 / 100)
    fs = max(16, img.width // 18)
    try:
        font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', fs)
    except:
        try:
            font = ImageFont.truetype('arial.ttf', fs)
        except:
            font = ImageFont.load_default()
    if position == 'diagonal':
        diag = Image.new('RGBA', (img.width * 3, img.height * 3), (0, 0, 0, 0))
        d = ImageDraw.Draw(diag)
        bb = d.textbbox((0, 0), text, font=font)
        tw = bb[2] - bb[0]
        # MUCH MORE SPACING - only 3-4 repetitions across
        sx = tw + max(300, img.width // 2)
        sy = max(120, fs + 80)
        for y in range(0, diag.height, sy):
            for x in range(0, diag.width, sx):
                if stroke:
                    d.text((x, y), text, font=font, fill=(r, g, b, alpha), stroke_width=2, stroke_fill=(0, 0, 0, alpha))
                else:
                    d.text((x, y), text, font=font, fill=(r, g, b, alpha))
        diag = diag.rotate(-45, resample=Image.BICUBIC)
        left = (diag.width - img.width) // 2
        top = (diag.height - img.height) // 2
        diag = diag.crop((left, top, left + img.width, top + img.height))
        result = Image.alpha_composite(img, diag)
    else:
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(overlay)
        bb = d.textbbox((0, 0), text, font=font)
        tw = bb[2] - bb[0]
        th = bb[3] - bb[1]
        x = (img.width - tw) / 2
        y = (img.height - th) / 2
        if stroke:
            d.text((x, y), text, font=font, fill=(r, g, b, alpha), stroke_width=2, stroke_fill=(0, 0, 0, alpha))
        else:
            d.text((x, y), text, font=font, fill=(r, g, b, alpha))
        result = Image.alpha_composite(img, overlay)
    output = result.convert('RGB')
    buf = io.BytesIO()
    output.save(buf, format='JPEG', quality=95)
    buf.seek(0)
    return buf

def apply_watermark(filepath, text='MeuFotoApp', color='#ffffff', opacity=30, position='diagonal', stroke=False, logo_path=None):
    buf = get_watermarked_bytes(filepath, text, color, opacity, position, stroke, logo_path)
    img = Image.open(buf)
    img.save(filepath, quality=95)

def enhance_image(filepath):
    img = Image.open(filepath)
    img = ImageEnhance.Contrast(img).enhance(1.2)
    img = ImageEnhance.Brightness(img).enhance(1.1)
    img = ImageEnhance.Sharpness(img).enhance(1.3)
    img.save(filepath, quality=95)
"""
with open(wm_path, 'w', encoding='utf-8') as f:
    f.write(wm_code.strip() + '\n')
print('OK: watermark.py (menos poluicao)')

# ===== 3. base.html (com JS para copiar link + lightbox) =====
base_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{% block title %}{{ site_settings.app_name if site_settings else 'MeuFotoApp' }}{% endblock %}</title>
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
{% if current_user.is_authenticated %}
<div class="sidebar">
<h2>{{ site_settings.app_name if site_settings else 'MeuFotoApp' }}</h2>
<a href="{{ url_for('dashboard') }}">Dashboard</a>
<a href="{{ url_for('list_galerias') }}">Galerias</a>
<a href="{{ url_for('nova_galeria') }}">+ Nova Galeria</a>
<a href="{{ url_for('selecoes') }}">Selecoes</a>
<a href="{{ url_for('portfolio') }}">Portfolio</a>
<a href="{{ url_for('catalogo_poses') }}">Catalogo de Poses</a>
<a href="{{ url_for('marca') }}">Marca d Agua</a>
<a href="{{ url_for('planos') }}">Planos</a>
<a href="{{ url_for('configuracoes') }}">Configuracoes</a>
{% if current_user.is_admin %}
<a href="{{ url_for('admin') }}" style="background:#353b48;color:#fff;">ADMIN</a>
{% endif %}
<a href="{{ url_for('logout') }}" class="logout">Sair</a>
</div>
<div class="main-content">
{% else %}
<div style="max-width:380px;margin:16px auto;">
{% endif %}
{% with messages = get_flashed_messages(with_categories=true) %}
{% if messages %}
{% for category, message in messages %}
<div class="flash {{ category }}">{{ message }}</div>
{% endfor %}
{% endif %}
{% endwith %}
{% block content %}{% endblock %}
{% if current_user.is_authenticated %}
</div>
{% else %}
</div>
{% endif %}

<div id="lightbox" style="display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.9);z-index:9999;justify-content:center;align-items:center;cursor:pointer;" onclick="closeLightbox()">
<img id="lightbox-img" src="" style="max-width:90%;max-height:90%;border-radius:8px;">
</div>

<script>
function copyLink(url,btn) {
    navigator.clipboard.writeText(url).then(function() {
        var orig = btn.textContent;
        btn.textContent = 'Copiado!';
        btn.style.background = '#27ae60';
        setTimeout(function() { btn.textContent = orig; btn.style.background = ''; }, 2000);
    });
}
function openLightbox(src) {
    var lb = document.getElementById('lightbox');
    document.getElementById('lightbox-img').src = src;
    lb.style.display = 'flex';
}
function closeLightbox() {
    document.getElementById('lightbox').style.display = 'none';
}
</script>
</body>
</html>"""
with open(os.path.join(tpl, 'base.html'), 'w', encoding='utf-8') as f:
    f.write(base_html.strip() + '\n')
print('OK: base.html (copy + lightbox)')

# ===== 4. portfolio.html (copy button + clickable photos) =====
portfolio_html = """{% extends 'base.html' %}
{% block title %}Portfolio{% endblock %}
{% block content %}
<div class="page-header">
<h1>Portfolio</h1>
<p>Antes e depois - com links de entrega para clientes</p>
</div>
{% if not public %}
<div class="card">
<h3>Adicionar Item</h3>
<form method="POST" enctype="multipart/form-data" action="{{ url_for('portfolio') }}">
<input type="text" name="title" placeholder="Titulo do trabalho" required>
<label>Foto Antes</label>
<input type="file" name="before" accept="image/*">
<label>Foto Depois</label>
<input type="file" name="after" accept="image/*">
<button type="submit" class="btn-primary">Adicionar</button>
</form>
</div>
{% endif %}
<div class="grid">
{% for item in items %}
<div class="card">
<h3>{{ item.title }}</h3>
{% if not public %}
<div style="background:#e8f5e9;padding:12px;border-radius:8px;margin-bottom:12px;border:1px solid #a5d6a7;">
<p style="font-size:13px;color:#2e7d32;margin:0 0 6px 0;"><strong>LINK DE ENTREGA:</strong></p>
<div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap;">
<a href="http://localhost:5000/p/{{ item.id }}" style="font-size:13px;color:#4a90d9;word-break:break-all;flex:1;">http://localhost:5000/p/{{ item.id }}</a>
<button onclick="copyLink('http://localhost:5000/p/{{ item.id }}',this)" class="btn-primary" style="padding:4px 10px;font-size:12px;flex-shrink:0;">Copiar</button>
</div>
</div>
{% endif %}
<div style="display:flex;gap:8px;flex-wrap:wrap;">
{% if item.before_path %}
<div>
<p style="font-size:12px;color:#888;margin-bottom:4px;">ANTES</p>
<img src="{{ url_for('serve_wm', filename=item.before_path) }}" style="width:200px;border-radius:8px;cursor:pointer;" onclick="openLightbox(this.src)">
</div>
{% endif %}
{% if item.after_path %}
<div>
<p style="font-size:12px;color:#888;margin-bottom:4px;">DEPOIS</p>
<img src="{{ url_for('serve_wm', filename=item.after_path) }}" style="width:200px;border-radius:8px;cursor:pointer;" onclick="openLightbox(this.src)">
</div>
{% endif %}
</div>
{% if not public %}
<form method="POST" action="{{ url_for('delete_portfolio', iid=item.id) }}" style="margin-top:8px;">
<button type="submit" class="btn-danger">Excluir</button>
</form>
{% endif %}
</div>
{% endfor %}
</div>
{% if not items %}
<p style="text-align:center;color:#888;margin-top:24px;">Nenhum item no portfolio.</p>
{% endif %}
{% endblock %}"""
with open(os.path.join(tpl, 'portfolio.html'), 'w', encoding='utf-8') as f:
    f.write(portfolio_html.strip() + '\n')
print('OK: portfolio.html (copy + lightbox)')

# ===== 5. galeria.html (copy button + clickable photos) =====
galeria_html = """{% extends 'base.html' %}
{% block title %}{{ galeria.title }}{% endblock %}
{% block content %}
<div class="page-header">
<h1>{{ galeria.title }}</h1>
<p>Cliente: {{ galeria.client_name or 'Nao definido' }} | {{ galeria.created_at.strftime('%d/%m/%Y') }}</p>
</div>
<div class="card" style="background:#e8f5e9;border:1px solid #a5d6a7;">
<h3 style="color:#2e7d32;">Sistema de Entrega Automatico</h3>
<p style="font-size:14px;color:#333;margin-bottom:8px;">
As fotos ficam <strong>sem marca</strong>. O cliente ve <strong>com marca dagua</strong>.
No ZIP e por e-mail voce recebe <strong>sem marca</strong>.
</p>
<div style="background:#fff;padding:10px;border-radius:8px;margin-top:8px;">
<p style="font-size:13px;margin:0 0 4px 0;"><strong>LINK DO CLIENTE:</strong></p>
<div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap;">
<a href="http://localhost:5000/g/{{ galeria.share_token }}" style="font-size:14px;color:#4a90d9;word-break:break-all;flex:1;">http://localhost:5000/g/{{ galeria.share_token }}</a>
<button onclick="copyLink('http://localhost:5000/g/{{ galeria.share_token }}',this)" class="btn-primary" style="padding:4px 10px;font-size:12px;flex-shrink:0;">Copiar</button>
</div>
</div>
</div>
<div class="card">
<h3>Enviar Fotos</h3>
<form method="POST" enctype="multipart/form-data">
<input type="file" name="photos" multiple accept="image/*" required>
<button type="submit" class="btn-primary">Enviar</button>
</form>
</div>
{% if selections %}
<div class="card">
<h3>Selecoes Recebidas ({{ selections|length }})</h3>
<table>
<tr><th>Data</th><th>Pacote</th><th>Status</th><th>Download</th></tr>
{% for s in selections %}
<tr>
<td>{{ s.created_at.strftime('%d/%m/%Y %H:%M') }}</td>
<td>{{ s.package_key or '-' }}</td>
<td>{{ s.status }}</td>
<td><a href="{{ url_for('download_selection', sid=s.id) }}" class="btn-primary" style="padding:4px 10px;font-size:12px;">Baixar ZIP</a></td>
</tr>
{% endfor %}
</table>
</div>
{% endif %}
<div class="card">
<h3>Fotos ({{ photos|length }})</h3>
{% if photos %}
<div class="grid">
{% for p in photos %}
<div style="border-radius:8px;overflow:hidden;">
<img src="{{ url_for('serve_upload', filename=p.filepath) }}" style="width:100%;border-radius:8px;cursor:pointer;" onclick="openLightbox(this.src)">
<div style="display:flex;gap:4px;margin-top:4px;flex-wrap:wrap;">
<a href="{{ url_for('resize_photo', gid=galeria.id, pid=p.id, platform='instagram_feed') }}" class="btn-primary" style="padding:3px 6px;font-size:11px;">IG</a>
<form method="POST" action="{{ url_for('enhance_photo', gid=galeria.id, pid=p.id) }}" style="display:inline;">
<button type="submit" class="btn-primary" style="padding:3px 6px;font-size:11px;">Melhorar</button>
</form>
<form method="POST" action="{{ url_for('rewatermark', gid=galeria.id, pid=p.id) }}" style="display:inline;">
<button type="submit" class="btn-primary" style="padding:3px 6px;font-size:11px;">Marca</button>
</form>
<form method="POST" action="{{ url_for('delete_photo', gid=galeria.id, pid=p.id) }}" style="display:inline;">
<button type="submit" class="btn-danger" style="padding:3px 6px;font-size:11px;">Excluir</button>
</form>
</div>
</div>
{% endfor %}
</div>
{% else %}
<p style="color:#888;text-align:center;">Nenhuma foto enviada.</p>
{% endif %}
</div>
{% endblock %}"""
with open(os.path.join(tpl, 'galeria.html'), 'w', encoding='utf-8') as f:
    f.write(galeria_html.strip() + '\n')
print('OK: galeria.html (copy + lightbox)')

# ===== 6. cliente.html (clickable photos) =====
cliente_path = os.path.join(tpl, 'cliente.html')
with open(cliente_path, 'r', encoding='utf-8') as f:
    content = f.read()
# Add onclick to images
content = content.replace(
    'style="width:100%;border-radius:8px;">',
    'style="width:100%;border-radius:8px;cursor:pointer;" onclick="openLightbox(this.src)">'
)
with open(cliente_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('OK: cliente.html (lightbox)')

# ===== 7. public_portfolio.html (clickable photos) =====
public_path = os.path.join(tpl, 'public_portfolio.html')
if os.path.exists(public_path):
    with open(public_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace(
        'style="width:350px;border-radius:8px;">',
        'style="width:350px;border-radius:8px;cursor:pointer;" onclick="openLightbox(this.src)">'
    )
    with open(public_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('OK: public_portfolio.html (lightbox)')

# ===== 8. catalogo_poses.html (clickable photos) =====
cat_path = os.path.join(tpl, 'catalogo_poses.html')
with open(cat_path, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace(
    'style="width:100%;border-radius:8px;">',
    'style="width:100%;border-radius:8px;cursor:pointer;" onclick="openLightbox(this.src)">'
)
with open(cat_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('OK: catalogo_poses.html (lightbox)')

print('\n=== CORRECOES APLICADAS! ===')