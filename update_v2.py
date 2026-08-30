import os

base = os.path.dirname(os.path.abspath(__file__))
tpl = os.path.join(base, 'templates')

# ===== 1. WATERMARK.PY (com marca d'agua em memoria) =====
wm_code = """from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import io

def get_watermarked_bytes(filepath, text='MeuFotoApp', color='#ffffff', opacity=30, position='diagonal', stroke=False, logo_path=None):
    img = Image.open(filepath).convert('RGBA')
    r = int(color[1:3], 16) if color.startswith('#') and len(color) >= 7 else 255
    g = int(color[3:5], 16) if color.startswith('#') and len(color) >= 7 else 255
    b = int(color[5:7], 16) if color.startswith('#') and len(color) >= 7 else 255
    alpha = int(opacity * 255 / 100)
    fs = max(20, img.width // 15)
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
        sx = tw + 80
        sy = max(40, fs + 20)
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
with open(os.path.join(base, 'watermark.py'), 'w', encoding='utf-8') as f:
    f.write(wm_code.strip() + '\n')
print('OK: watermark.py')

# ===== 2. APP.PY (patched) =====
app_path = os.path.join(base, 'app.py')
with open(app_path, 'r', encoding='utf-8') as f:
    code = f.read()

patches = 0

# 2a. Add smtplib import
if 'import os, secrets, io, zipfile\n' in code and 'smtplib' not in code:
    code = code.replace('import os, secrets, io, zipfile\n', 'import os, secrets, io, zipfile, smtplib\nfrom email.mime.text import MIMEText\n')
    patches += 1; print('  OK: smtplib import')
else:
    print('  SKIP: smtplib import')

# 2b. Add get_watermarked_bytes import
if 'get_watermarked_bytes' not in code:
    code = code.replace('from watermark import apply_watermark, enhance_image', 'from watermark import apply_watermark, enhance_image, get_watermarked_bytes')
    patches += 1; print('  OK: watermark import')
else:
    print('  SKIP: watermark import')

# 2c. Add send_notification_email function
if 'def send_notification_email' not in code:
    email_func = '''
def send_notification_email(user_email, client_name, gallery_title, package, photo_count):
    settings = AppSettings.query.first()
    if not settings or not settings.smtp_host or not settings.smtp_user:
        return
    try:
        body = "Nova selecao!\\n\\nCliente: " + str(client_name or "Nao informado") + "\\nGaleria: " + str(gallery_title) + "\\nPacote: " + str(package or "Nenhum") + "\\nFotos: " + str(photo_count) + "\\n\\nAcesse: http://localhost:5000/selecoes"
        msg = MIMEText(body)
        msg["Subject"] = "Nova selecao - " + str(gallery_title)
        msg["From"] = settings.smtp_user
        msg["To"] = user_email
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port or 587) as server:
            server.starttls()
            server.login(settings.smtp_user, settings.smtp_password or "")
            server.send_message(msg)
    except Exception as e:
        print("Email error: " + str(e))
'''
    code = code.replace('@login_manager.user_loader', email_func + '\n@login_manager.user_loader')
    patches += 1; print('  OK: send_notification_email')
else:
    print('  SKIP: send_notification_email')

# 2d. Remove apply_watermark on upload (store originals)
old_upload = """                if wm:
                    try: apply_watermark(os.path.join(UPLOAD_FOLDER, fn), wm.text or 'MeuFotoApp', wm.color, wm.opacity, wm.position, wm.stroke, wm.logo_path)
                    except: pass
                db.session.add(Photo(galeria_id=g.id, filepath=fn, filename=f.filename, has_watermark=bool(wm)))"""
new_upload = "                db.session.add(Photo(galeria_id=g.id, filepath=fn, filename=f.filename, has_watermark=False))"
if old_upload in code:
    code = code.replace(old_upload, new_upload)
    patches += 1; print('  OK: upload sem watermark')
else:
    print('  SKIP: upload patch')

# 2e. Add serve_wm route
if 'def serve_wm' not in code:
    wm_route = '''

@app.route('/wm/<filename>')
def serve_wm(filename):
    photo = Photo.query.filter_by(filepath=filename).first()
    if photo:
        galeria = Galeria.query.get(photo.galeria_id)
        if galeria:
            wm = Watermark.query.filter_by(user_id=galeria.user_id).first()
            if wm:
                fp = os.path.join(UPLOAD_FOLDER, filename)
                if os.path.exists(fp):
                    try:
                        img_bytes = get_watermarked_bytes(fp, wm.text or 'MeuFotoApp', wm.color or '#ffffff', wm.opacity or 30, wm.position or 'diagonal', wm.stroke, wm.logo_path)
                        return send_file(img_bytes, mimetype='image/jpeg')
                    except Exception as e:
                        print('WM error: ' + str(e))
    return send_file(os.path.join(UPLOAD_FOLDER, filename))'''
    # Insert after serve_upload route
    old_route = "@app.route('/uploads/<filename>')\ndef serve_upload(filename):\n    return send_file(os.path.join(UPLOAD_FOLDER, filename))"
    if old_route in code:
        code = code.replace(old_route, old_route + wm_route)
        patches += 1; print('  OK: serve_wm route')
    else:
        print('  SKIP: serve_wm (serve_upload not found)')
else:
    print('  SKIP: serve_wm already exists')

# 2f. Add email notification in cliente_view POST
old_client = """        db.session.add(sel); db.session.commit()
        flash('Selecao enviada! O fotografo recebera sua escolha.', 'success')"""
new_client = """        db.session.add(sel); db.session.commit()
        try:
            owner = User.query.get(g.user_id)
            if owner:
                send_notification_email(owner.email, g.client_name, g.title, request.form.get('package_key', ''), len(ids))
        except: pass
        flash('Selecao enviada! O fotografo recebera sua escolha.', 'success')"""
if old_client in code and 'send_notification_email(owner' not in code:
    code = code.replace(old_client, new_client)
    patches += 1; print('  OK: email notification')
else:
    print('  SKIP: email notification')

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(code)
print(f'app.py: {patches} patches applied')

# ===== 3. MARCA.HTML (preview com foto + diagonal real) =====
marca_html = """{% extends 'base.html' %}
{% block title %}Marca d Agua{% endblock %}
{% block content %}
<div class="page-header">
<h1>Marca d Agua</h1>
<p>Configure a marca dagua - o cliente ve as fotos com marca, voce recebe sem</p>
</div>
<div style="display:flex;gap:20px;flex-wrap:wrap;">
<div class="card" style="flex:1;min-width:280px;">
<form method="POST" enctype="multipart/form-data" action="{{ url_for('marca') }}" id="wm-form">
<label>Texto da marca dagua</label>
<input type="text" name="text" id="wm-text" value="{{ wm.text if wm else '' }}" placeholder="Seu nome ou estudio" oninput="updatePreview()">
<label>Cor</label>
<input type="color" name="color" id="wm-color" value="{{ wm.color if wm else '#ffffff' }}" oninput="updatePreview()">
<label>Opacidade: <span id="opacity-val">{{ wm.opacity if wm else 30 }}%</span></label>
<input type="range" name="opacity" id="wm-opacity" value="{{ wm.opacity if wm else 30 }}" min="0" max="100" oninput="updatePreview()">
<label>Posicao</label>
<select name="position" id="wm-position" onchange="updatePreview()">
<option value="diagonal" {{ 'selected' if wm and wm.position == 'diagonal' else '' }}>Diagonal (atravessada -45)</option>
<option value="center" {{ 'selected' if wm and wm.position == 'center' else '' }}>Centro</option>
</select>
<label>Contorno (borda escura)</label>
<input type="checkbox" name="stroke" id="wm-stroke" {{ 'checked' if wm and wm.stroke else '' }} onchange="updatePreview()">
<label>Logo (opcional)</label>
<input type="file" name="logo" accept="image/*">
<hr>
<label>Carregar foto de teste para pre-visualizacao</label>
<input type="file" id="preview-img" accept="image/*" onchange="loadPreviewImage(this)">
<button type="submit" class="btn-primary">Salvar Configuracoes</button>
</form>
</div>
<div class="card" style="flex:1;min-width:280px;">
<h3>Pre-visualizacao</h3>
<canvas id="preview-canvas" width="500" height="375" style="width:100%;border-radius:8px;background:#555;"></canvas>
<p style="color:#777;font-size:12px;margin-top:8px;">Carregue uma foto de teste para ver como ficara. A marca dagua e aplicada automaticamente quando o cliente visualiza as fotos.</p>
</div>
</div>
<script>
var previewImage = null;
function loadPreviewImage(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            var img = new Image();
            img.onload = function() {
                previewImage = img;
                updatePreview();
            };
            img.src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    }
}
function updatePreview() {
    var c = document.getElementById('preview-canvas');
    var x = c.getContext('2d');
    x.clearRect(0, 0, c.width, c.height);
    if (previewImage) {
        var r = Math.max(c.width / previewImage.width, c.height / previewImage.height);
        var w = previewImage.width * r;
        var h = previewImage.height * r;
        x.drawImage(previewImage, (c.width - w) / 2, (c.height - h) / 2, w, h);
    } else {
        var g = x.createLinearGradient(0, 0, c.width, c.height);
        g.addColorStop(0, '#666');
        g.addColorStop(0.5, '#888');
        g.addColorStop(1, '#555');
        x.fillStyle = g;
        x.fillRect(0, 0, c.width, c.height);
    }
    var text = document.getElementById('wm-text').value || 'MeuFotoApp';
    var color = document.getElementById('wm-color').value;
    var opacity = document.getElementById('wm-opacity').value / 100;
    var position = document.getElementById('wm-position').value;
    var stroke = document.getElementById('wm-stroke').checked;
    document.getElementById('opacity-val').textContent = document.getElementById('wm-opacity').value + '%';
    x.font = 'bold 24px Arial';
    x.globalAlpha = opacity;
    if (position === 'diagonal') {
        x.save();
        x.translate(c.width / 2, c.height / 2);
        x.rotate(-Math.PI / 4);
        var tw = x.measureText(text).width;
        var sp = tw + 80;
        for (var y = -c.height; y < c.height * 2; y += 60) {
            for (var xx = -c.width; xx < c.width * 2; xx += sp) {
                if (stroke) {
                    x.strokeStyle = 'rgba(0,0,0,' + opacity + ')';
                    x.lineWidth = 2;
                    x.strokeText(text, xx, y);
                }
                x.fillStyle = color;
                x.fillText(text, xx, y);
            }
        }
        x.restore();
    } else {
        var tw = x.measureText(text).width;
        var px = (c.width - tw) / 2;
        var py = c.height / 2;
        if (stroke) {
            x.strokeStyle = 'rgba(0,0,0,' + opacity + ')';
            x.lineWidth = 2;
            x.strokeText(text, px, py);
        }
        x.fillStyle = color;
        x.fillText(text, px, py);
    }
    x.globalAlpha = 1;
}
updatePreview();
</script>
{% endblock %}"""
with open(os.path.join(tpl, 'marca.html'), 'w', encoding='utf-8') as f:
    f.write(marca_html.strip() + '\n')
print('OK: marca.html')

# ===== 4. CLIENTE.HTML (usa serve_wm em vez de serve_upload) =====
cliente_path = os.path.join(tpl, 'cliente.html')
with open(cliente_path, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("url_for('serve_upload'", "url_for('serve_wm'")
with open(cliente_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('OK: cliente.html (watermarked view)')

# ===== 5. PORTFOLIO.HTML (com links de entrega) =====
portfolio_html = """{% extends 'base.html' %}
{% block title %}Portfolio{% endblock %}
{% block content %}
<div class="page-header">
<h1>Portfolio</h1>
<p>Antes e depois -Links de entrega para clientes</p>
</div>
{% if not public %}
<form method="POST" enctype="multipart/form-data" action="{{ url_for('portfolio') }}" class="card">
<h3>Adicionar Item</h3>
<input type="text" name="title" placeholder="Titulo do trabalho" required>
<label>Foto Antes</label>
<input type="file" name="before" accept="image/*">
<label>Foto Depois</label>
<input type="file" name="after" accept="image/*">
<button type="submit" class="btn-primary">Adicionar</button>
</form>
{% endif %}
<div class="grid">
{% for item in items %}
<div class="card">
<h3>{{ item.title }}</h3>
{% if not public %}
<div style="background:#e8f5e9;padding:10px;border-radius:8px;margin-bottom:10px;">
<p style="font-size:12px;color:#2e7d32;margin:0;"><strong>Link de entrega:</strong></p>
<p style="font-size:13px;word-break:break-all;margin:4px 0 0 0;">http://localhost:5000/p/{{ item.share_token }}</p>
</div>
{% endif %}
<div style="display:flex;gap:8px;flex-wrap:wrap;">
{% if item.before_path %}
<div><p style="font-size:12px;color:#888;">ANTES</p><img src="{{ url_for('serve_upload', filename=item.before_path) }}" style="width:200px;border-radius:8px;"></div>
{% endif %}
{% if item.after_path %}
<div><p style="font-size:12px;color:#888;">DEPOIS</p><img src="{{ url_for('serve_upload', filename=item.after_path) }}" style="width:200px;border-radius:8px;"></div>
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
print('OK: portfolio.html (com links de entrega)')

# ===== 6. GALERIA.HTML (adicionar nota de entrega) =====
galeria_path = os.path.join(tpl, 'galeria.html')
with open(galeria_path, 'r', encoding='utf-8') as f:
    content = f.read()
if 'Sistema de Entrega' not in content:
    delivery_note = """<div class="card" style="background:#e8f5e9;border:1px solid #a5d6a7;">
<h3>Sistema de Entrega Automatico</h3>
<p style="font-size:14px;color:#2e7d32;">As fotos sao armazenadas <strong>sem marca dagua</strong>. O cliente ve as fotos <strong>com marca dagua</strong> automaticamente. Quando o cliente seleciona e envia, voce recebe as fotos <strong>originais (sem marca)</strong> no download ZIP e por e-mail.</p>
</div>
"""
    content = content.replace('<div class="card">\n<h3>Enviar Fotos</h3>', delivery_note + '<div class="card">\n<h3>Enviar Fotos</h3>')
    with open(galeria_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('OK: galeria.html (nota de entrega)')
else:
    print('SKIP: galeria.html (ja tem nota)')

print('\n=== SISTEMA DE ENTREGAS ATUALIZADO! ===')