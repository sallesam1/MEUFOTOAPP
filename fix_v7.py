import os
base = os.path.dirname(os.path.abspath(__file__))
tpl = os.path.join(base, 'templates')

# ===== 1. LOGIN total dark premium =====
login_html = """{% extends 'base.html' %}
{% block title %}Login{% endblock %}
{% block content %}
<div style="min-height:100vh;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#0a0a0a 0%,#1a1a2e 50%,#16213e 100%);">
<div style="background:#161b22;border:1px solid #30363d;border-radius:16px;padding:40px;width:380px;box-shadow:0 20px 50px rgba(0,0,0,0.6);">
<div style="text-align:center;margin-bottom:28px;">
<h1 style="color:#fff;font-size:26px;font-weight:700;margin:0 0 4px 0;">{{ site_settings.app_name if site_settings else 'MeuFotoApp' }}</h1>
<p style="color:#8b949e;font-size:13px;margin:0;">Acesse sua conta</p>
</div>
<form method="POST">
<div style="margin-bottom:14px;">
<label style="color:#8b949e;font-size:12px;margin-bottom:6px;display:block;">E-MAIL</label>
<input type="email" name="email" placeholder="seu@email.com" required style="width:100%;padding:12px 14px;background:#0d1117;border:1px solid #30363d;border-radius:8px;color:#fff;font-size:14px;outline:none;" onfocus="this.style.borderColor='#4a90d9'" onblur="this.style.borderColor='#30363d'">
</div>
<div style="margin-bottom:20px;">
<label style="color:#8b949e;font-size:12px;margin-bottom:6px;display:block;">SENHA</label>
<input type="password" name="password" placeholder="********" required style="width:100%;padding:12px 14px;background:#0d1117;border:1px solid #30363d;border-radius:8px;color:#fff;font-size:14px;outline:none;" onfocus="this.style.borderColor='#4a90d9'" onblur="this.style.borderColor='#30363d'">
</div>
<button type="submit" style="width:100%;padding:12px;background:#4a90d9;color:#fff;border:none;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer;">ENTRAR</button>
</form>
<div style="text-align:center;margin:16px 0 12px 0;position:relative;">
<hr style="border:none;border-top:1px solid #30363d;margin:0;">
<span style="position:absolute;top:-8px;left:50%;transform:translateX(-50%);background:#161b22;color:#8b949e;font-size:11px;padding:0 12px;">OU</span>
</div>
<a href="{{ url_for('login_google') }}" style="display:block;text-align:center;padding:12px;background:#0d1117;border:1px solid #30363d;border-radius:8px;text-decoration:none;color:#fff;font-size:14px;">Entrar com Google</a>
<p style="text-align:center;margin-top:20px;font-size:13px;color:#8b949e;">Nao tem conta? <a href="{{ url_for('registro') }}" style="color:#4a90d9;text-decoration:none;">Criar agora</a></p>
</div>
</div>
{% endblock %}"""
with open(os.path.join(tpl, 'login.html'), 'w', encoding='utf-8') as f:
    f.write(login_html.strip() + '\n')
print('OK: login.html (dark total)')

# ===== 2. REGISTRO total dark premium =====
registro_html = """{% extends 'base.html' %}
{% block title %}Criar conta{% endblock %}
{% block content %}
<div style="min-height:100vh;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#0a0a0a 0%,#1a1a2e 50%,#16213e 100%);padding:20px;">
<div style="background:#161b22;border:1px solid #30363d;border-radius:16px;padding:40px;width:380px;box-shadow:0 20px 50px rgba(0,0,0,0.6);">
<div style="text-align:center;margin-bottom:28px;">
<h1 style="color:#fff;font-size:26px;font-weight:700;margin:0 0 4px 0;">Criar Conta</h1>
<p style="color:#8b949e;font-size:13px;margin:0;">Comece agora</p>
</div>
<form method="POST">
<div style="margin-bottom:14px;">
<label style="color:#8b949e;font-size:12px;margin-bottom:6px;display:block;">ESTUDIO</label>
<input type="text" name="studio_name" placeholder="Nome do estudio" style="width:100%;padding:12px 14px;background:#0d1117;border:1px solid #30363d;border-radius:8px;color:#fff;font-size:14px;outline:none;" onfocus="this.style.borderColor='#4a90d9'" onblur="this.style.borderColor='#30363d'">
</div>
<div style="margin-bottom:14px;">
<label style="color:#8b949e;font-size:12px;margin-bottom:6px;display:block;">NOME</label>
<input type="text" name="name" placeholder="Seu nome" style="width:100%;padding:12px 14px;background:#0d1117;border:1px solid #30363d;border-radius:8px;color:#fff;font-size:14px;outline:none;" onfocus="this.style.borderColor='#4a90d9'" onblur="this.style.borderColor='#30363d'">
</div>
<div style="margin-bottom:14px;">
<label style="color:#8b949e;font-size:12px;margin-bottom:6px;display:block;">E-MAIL</label>
<input type="email" name="email" placeholder="seu@email.com" required style="width:100%;padding:12px 14px;background:#0d1117;border:1px solid #30363d;border-radius:8px;color:#fff;font-size:14px;outline:none;" onfocus="this.style.borderColor='#4a90d9'" onblur="this.style.borderColor='#30363d'">
</div>
<div style="margin-bottom:20px;">
<label style="color:#8b949e;font-size:12px;margin-bottom:6px;display:block;">SENHA</label>
<input type="password" name="password" placeholder="********" required style="width:100%;padding:12px 14px;background:#0d1117;border:1px solid #30363d;border-radius:8px;color:#fff;font-size:14px;outline:none;" onfocus="this.style.borderColor='#4a90d9'" onblur="this.style.borderColor='#30363d'">
</div>
<button type="submit" style="width:100%;padding:12px;background:#4a90d9;color:#fff;border:none;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer;">CRIAR CONTA</button>
</form>
<p style="text-align:center;margin-top:20px;font-size:13px;color:#8b949e;">Ja tem conta? <a href="{{ url_for('login') }}" style="color:#4a90d9;text-decoration:none;">Entrar</a></p>
</div>
</div>
{% endblock %}"""
with open(os.path.join(tpl, 'registro.html'), 'w', encoding='utf-8') as f:
    f.write(registro_html.strip() + '\n')
print('OK: registro.html (dark total)')

# ===== 3. WATERMARK estilo Upfotos (repetido diagonal, bem espaçado) =====
wm_code = """from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import io

def get_watermarked_bytes(filepath, text='MeuFotoApp', color='#ffffff', opacity=30, position='diagonal', stroke=False, logo_path=None):
    img = Image.open(filepath).convert('RGBA')
    r = int(color[1:3], 16) if color.startswith('#') and len(color) >= 7 else 255
    g = int(color[3:5], 16) if color.startswith('#') and len(color) >= 7 else 255
    b = int(color[5:7], 16) if color.startswith('#') and len(color) >= 7 else 255
    alpha = int(opacity * 255 / 100)
    fs = max(14, img.width // 25)
    try:
        font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', fs)
    except:
        try:
            font = ImageFont.truetype('arial.ttf', fs)
        except:
            font = ImageFont.load_default()

    if position == 'diagonal':
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(overlay)
        bb = d.textbbox((0, 0), text, font=font)
        tw = bb[2] - bb[0]
        th = bb[3] - bb[1]
        sp_x = tw + max(150, img.width // 3)
        sp_y = max(50, fs + 30)
        for y in range(-th, img.height + th, sp_y):
            for x in range(-tw, img.width + tw, sp_x):
                if stroke:
                    d.text((x, y), text, font=font, fill=(r, g, b, alpha), stroke_width=1, stroke_fill=(0, 0, 0, alpha))
                else:
                    d.text((x, y), text, font=font, fill=(r, g, b, alpha))
        result = Image.alpha_composite(img, overlay)
    else:
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(overlay)
        fs2 = max(20, img.width // 10)
        try:
            font2 = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', fs2)
        except:
            try:
                font2 = ImageFont.truetype('arial.ttf', fs2)
            except:
                font2 = ImageFont.load_default()
        bb = d.textbbox((0, 0), text, font=font2)
        tw = bb[2] - bb[0]
        th = bb[3] - bb[1]
        x = (img.width - tw) / 2
        y = (img.height - th) / 2
        if stroke:
            d.text((x, y), text, font=font2, fill=(r, g, b, alpha), stroke_width=2, stroke_fill=(0, 0, 0, alpha))
        else:
            d.text((x, y), text, font=font2, fill=(r, g, b, alpha))
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
print('OK: watermark.py (estilo Upfotos - repetido e espaçado)')

# ===== 4. MARCA.HTML (preview estilo Upfotos) =====
marca_html = """{% extends 'base.html' %}
{% block title %}Marca d Agua{% endblock %}
{% block content %}
<div class="page-header">
<h1>Marca d Agua</h1>
<p>Estilo Upfotos - repetido na diagonal, bem espaçado, sem poluir</p>
</div>
<div style="display:flex;gap:20px;flex-wrap:wrap;">
<div class="card" style="flex:1;min-width:280px;">
<form method="POST" enctype="multipart/form-data" action="{{ url_for('marca') }}" id="wm-form">
<label>Texto da marca dagua</label>
<input type="text" name="text" id="wm-text" value="{{ wm.text if wm else '' }}" placeholder="Seu nome ou estudio" oninput="updatePreview()">
<label>Cor</label>
<input type="color" name="color" id="wm-color" value="{{ wm.color if wm else '#ffffff' }}" oninput="updatePreview()">
<label>Opacidade: <span id="opacity-val">{{ wm.opacity if wm else 30 }}%</span></label>
<input type="range" name="opacity" id="wm-opacity" value="{{ wm.opacity if wm else 30 }}" min="5" max="80" oninput="updatePreview()">
<label>Posicao</label>
<select name="position" id="wm-position" onchange="updatePreview()">
<option value="diagonal" {{ 'selected' if wm and wm.position == 'diagonal' else '' }}>Diagonal (repetido)</option>
<option value="center" {{ 'selected' if wm and wm.position == 'center' else '' }}>Centro</option>
</select>
<label>Contorno</label>
<input type="checkbox" name="stroke" id="wm-stroke" {{ 'checked' if wm and wm.stroke else '' }} onchange="updatePreview()">
<label>Logo (opcional)</label>
<input type="file" name="logo" accept="image/*">
<hr>
<label>Carregar foto de teste</label>
<input type="file" id="preview-img" accept="image/*" onchange="loadPreviewImage(this)">
<button type="submit" class="btn-primary">Salvar</button>
</form>
</div>
<div class="card" style="flex:1;min-width:280px;">
<h3>Pre-visualizacao</h3>
<canvas id="preview-canvas" width="500" height="375" style="width:100%;border-radius:8px;background:#555;"></canvas>
<p style="color:#777;font-size:12px;margin-top:8px;">Texto menor e bem espaçado - protege sem poluir a foto.</p>
</div>
</div>
<script>
var previewImage=null;
function loadPreviewImage(input){if(input.files&&input.files[0]){var r=new FileReader();r.onload=function(e){var i=new Image();i.onload=function(){previewImage=i;updatePreview()};i.src=e.target.result};r.readAsDataURL(input.files[0])}}
function updatePreview(){
var c=document.getElementById('preview-canvas');var x=c.getContext('2d');x.clearRect(0,0,c.width,c.height);
if(previewImage){var r=Math.max(c.width/previewImage.width,c.height/previewImage.height);var w=previewImage.width*r;var h=previewImage.height*r;x.drawImage(previewImage,(c.width-w)/2,(c.height-h)/2,w,h)}
else{var g=x.createLinearGradient(0,0,c.width,c.height);g.addColorStop(0,'#666');g.addColorStop(1,'#555');x.fillStyle=g;x.fillRect(0,0,c.width,c.height)}
var text=document.getElementById('wm-text').value||'MeuFotoApp';var color=document.getElementById('wm-color').value;var opacity=document.getElementById('wm-opacity').value/100;var position=document.getElementById('wm-position').value;var stroke=document.getElementById('wm-stroke').checked;
document.getElementById('opacity-val').textContent=document.getElementById('wm-opacity').value+'%';
var fs=14;x.font=fs+'px Arial';x.globalAlpha=opacity;
if(position==='diagonal'){
x.save();x.translate(c.width/2,c.height/2);x.rotate(-Math.PI/4);
var tw=x.measureText(text).width;var spx=tw+150;var spy=fs+30;
for(var y=-c.height;y<c.height*2;y+=spy){for(var xx=-c.width;xx<c.width*2;xx+=spx){
if(stroke){x.strokeStyle='rgba(0,0,0,'+opacity+')';x.lineWidth=1;x.strokeText(text,xx,y)}
x.fillStyle=color;x.fillText(text,xx,y)}}
x.restore()}else{
var fs2=30;x.font='bold '+fs2+'px Arial';var tw=x.measureText(text).width;
if(stroke){x.strokeStyle='rgba(0,0,0,'+opacity+')';x.lineWidth=2;x.strokeText(text,(c.width-tw)/2,c.height/2)}
x.fillStyle=color;x.fillText(text,(c.width-tw)/2,c.height/2)}
x.globalAlpha=1}
updatePreview();
</script>
{% endblock %}"""
with open(os.path.join(tpl, 'marca.html'), 'w', encoding='utf-8') as f:
    f.write(marca_html.strip() + '\n')
print('OK: marca.html (preview estilo Upfotos)')

print('\n=== LOGIN DARK TOTAL + WATERMARK UPFOTOS! ===')