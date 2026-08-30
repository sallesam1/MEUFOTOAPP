import os
base = os.path.dirname(os.path.abspath(__file__))
tpl = os.path.join(base, 'templates')

# ===== 1. LOGIN dark premium =====
login_html = """{% extends 'base.html' %}
{% block title %}Login — {{ site_settings.app_name if site_settings else 'MeuFotoApp' }}{% endblock %}
{% block content %}
<div style="min-height:100vh;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#0a0a0a 0%,#1a1a2e 50%,#16213e 100%);">
<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:48px;width:420px;backdrop-filter:blur(20px);box-shadow:0 25px 60px rgba(0,0,0,0.5);">
<div style="text-align:center;margin-bottom:32px;">
<h1 style="color:#fff;font-size:28px;font-weight:700;letter-spacing:-0.02em;margin:0 0 6px 0;">{{ site_settings.app_name if site_settings else 'MeuFotoApp' }}</h1>
<p style="color:#888;font-size:13px;margin:0;">Acesse sua conta</p>
</div>
<form method="POST">
<div style="margin-bottom:16px;">
<label style="color:#999;font-size:12px;margin-bottom:6px;display:block;">E-MAIL</label>
<input type="email" name="email" placeholder="seu@email.com" required style="width:100%;padding:14px 16px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:10px;color:#fff;font-size:15px;outline:none;transition:all 0.3s;" onfocus="this.style.borderColor='#4a90d9'" onblur="this.style.borderColor='rgba(255,255,255,0.1)'">
</div>
<div style="margin-bottom:24px;">
<label style="color:#999;font-size:12px;margin-bottom:6px;display:block;">SENHA</label>
<input type="password" name="password" placeholder="********" required style="width:100%;padding:14px 16px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:10px;color:#fff;font-size:15px;outline:none;transition:all 0.3s;" onfocus="this.style.borderColor='#4a90d9'" onblur="this.style.borderColor='rgba(255,255,255,0.1)'">
</div>
<button type="submit" style="width:100%;padding:14px;background:linear-gradient(135deg,#4a90d9,#357abd);color:#fff;border:none;border-radius:10px;font-size:15px;font-weight:600;cursor:pointer;letter-spacing:0.5px;transition:all 0.3s;" onmouseover="this.style.transform='translateY(-1px)';this.style.boxShadow='0 8px 25px rgba(74,144,217,0.4)'" onmouseout="this.style.transform='none';this.style.boxShadow='none'">ENTRAR</button>
</form>
<div style="text-align:center;margin:20px 0 16px 0;position:relative;">
<hr style="border:none;border-top:1px solid rgba(255,255,255,0.1);margin:0;">
<span style="position:absolute;top:-8px;left:50%;transform:translateX(-50%);background:#0d1117;color:#666;font-size:11px;padding:0 12px;">OU</span>
</div>
<a href="{{ url_for('login_google') }}" style="display:block;text-align:center;padding:14px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:10px;text-decoration:none;color:#fff;font-size:14px;font-weight:500;transition:all 0.3s;" onmouseover="this.style.background='rgba(255,255,255,0.08)'" onmouseout="this.style.background='rgba(255,255,255,0.05)'">
<span style="display:inline-block;vertical-align:middle;margin-right:8px;font-size:18px;">G</span>Entrar com Google
</a>
<p style="text-align:center;margin-top:24px;font-size:14px;color:#666;">Nao tem conta? <a href="{{ url_for('registro') }}" style="color:#4a90d9;text-decoration:none;">Criar agora</a></p>
</div>
</div>
{% endblock %}"""
with open(os.path.join(tpl, 'login.html'), 'w', encoding='utf-8') as f:
    f.write(login_html.strip() + '\n')
print('OK: login.html (dark premium)')

# ===== 2. REGISTRO dark premium =====
registro_html = """{% extends 'base.html' %}
{% block title %}Criar conta — {{ site_settings.app_name if site_settings else 'MeuFotoApp' }}{% endblock %}
{% block content %}
<div style="min-height:100vh;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#0a0a0a 0%,#1a1a2e 50%,#16213e 100%);padding:20px;">
<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:48px;width:420px;backdrop-filter:blur(20px);box-shadow:0 25px 60px rgba(0,0,0,0.5);">
<div style="text-align:center;margin-bottom:32px;">
<h1 style="color:#fff;font-size:28px;font-weight:700;letter-spacing:-0.02em;margin:0 0 6px 0;">Criar Conta</h1>
<p style="color:#888;font-size:13px;margin:0;">Comece gratis agora</p>
</div>
<form method="POST">
<div style="margin-bottom:16px;">
<label style="color:#999;font-size:12px;margin-bottom:6px;display:block;">NOME DO ESTUDIO</label>
<input type="text" name="studio_name" placeholder="Seu estudio" style="width:100%;padding:14px 16px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:10px;color:#fff;font-size:15px;outline:none;" onfocus="this.style.borderColor='#4a90d9'" onblur="this.style.borderColor='rgba(255,255,255,0.1)'">
</div>
<div style="margin-bottom:16px;">
<label style="color:#999;font-size:12px;margin-bottom:6px;display:block;">SEU NOME</label>
<input type="text" name="name" placeholder="Como te chamam" style="width:100%;padding:14px 16px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:10px;color:#fff;font-size:15px;outline:none;" onfocus="this.style.borderColor='#4a90d9'" onblur="this.style.borderColor='rgba(255,255,255,0.1)'">
</div>
<div style="margin-bottom:16px;">
<label style="color:#999;font-size:12px;margin-bottom:6px;display:block;">E-MAIL</label>
<input type="email" name="email" placeholder="seu@email.com" required style="width:100%;padding:14px 16px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:10px;color:#fff;font-size:15px;outline:none;" onfocus="this.style.borderColor='#4a90d9'" onblur="this.style.borderColor='rgba(255,255,255,0.1)'">
</div>
<div style="margin-bottom:24px;">
<label style="color:#999;font-size:12px;margin-bottom:6px;display:block;">SENHA</label>
<input type="password" name="password" placeholder="********" required style="width:100%;padding:14px 16px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:10px;color:#fff;font-size:15px;outline:none;" onfocus="this.style.borderColor='#4a90d9'" onblur="this.style.borderColor='rgba(255,255,255,0.1)'">
</div>
<button type="submit" style="width:100%;padding:14px;background:linear-gradient(135deg,#4a90d9,#357abd);color:#fff;border:none;border-radius:10px;font-size:15px;font-weight:600;cursor:pointer;letter-spacing:0.5px;transition:all 0.3s;" onmouseover="this.style.transform='translateY(-1px)';this.style.boxShadow='0 8px 25px rgba(74,144,217,0.4)'" onmouseout="this.style.transform='none';this.style.boxShadow='none'">CRIAR CONTA</button>
</form>
<p style="text-align:center;margin-top:24px;font-size:14px;color:#666;">Ja tem conta? <a href="{{ url_for('login') }}" style="color:#4a90d9;text-decoration:none;">Entrar</a></p>
</div>
</div>
{% endblock %}"""
with open(os.path.join(tpl, 'registro.html'), 'w', encoding='utf-8') as f:
    f.write(registro_html.strip() + '\n')
print('OK: registro.html (dark premium)')

# ===== 3. WATERMARK - muito menos poluicao =====
wm_code = """from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import io

def get_watermarked_bytes(filepath, text='MeuFotoApp', color='#ffffff', opacity=30, position='diagonal', stroke=False, logo_path=None):
    img = Image.open(filepath).convert('RGBA')
    r = int(color[1:3], 16) if color.startswith('#') and len(color) >= 7 else 255
    g = int(color[3:5], 16) if color.startswith('#') and len(color) >= 7 else 255
    b = int(color[5:7], 16) if color.startswith('#') and len(color) >= 7 else 255
    alpha = int(opacity * 255 / 100)

    if position == 'diagonal':
        # UM UNICO TEXTO GRANDE DIAGONAL - sem repeticao
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(overlay)
        fs = max(40, img.width // 5)
        try:
            font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', fs)
        except:
            try:
                font = ImageFont.truetype('arial.ttf', fs)
            except:
                font = ImageFont.load_default()
        bb = d.textbbox((0, 0), text, font=font)
        tw = bb[2] - bb[0]
        th = bb[3] - bb[1]
        # Centralizar e rotacionar
        temp = Image.new('RGBA', (tw + fs * 2, th + fs), (0, 0, 0, 0))
        td = ImageDraw.Draw(temp)
        tx = fs
        ty = 0
        if stroke:
            td.text((tx, ty), text, font=font, fill=(r, g, b, alpha), stroke_width=max(2, fs // 15), stroke_fill=(0, 0, 0, alpha))
        else:
            td.text((tx, ty), text, font=font, fill=(r, g, b, alpha))
        temp = temp.rotate(-45, resample=Image.BICUBIC, expand=True)
        px = (img.width - temp.width) // 2
        py = (img.height - temp.height) // 2
        overlay.paste(temp, (px, py), temp)
        result = Image.alpha_composite(img, overlay)
    else:
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(overlay)
        fs = max(30, img.width // 8)
        try:
            font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', fs)
        except:
            try:
                font = ImageFont.truetype('arial.ttf', fs)
            except:
                font = ImageFont.load_default()
        bb = d.textbbox((0, 0), text, font=font)
        tw = bb[2] - bb[0]
        th = bb[3] - bb[1]
        x = (img.width - tw) / 2
        y = (img.height - th) / 2
        if stroke:
            d.text((x, y), text, font=font, fill=(r, g, b, alpha), stroke_width=max(2, fs // 15), stroke_fill=(0, 0, 0, alpha))
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
print('OK: watermark.py (1 texto grande, sem repeticao)')

# ===== 4. MARCA.HTML (preview atualizado) =====
marca_html = """{% extends 'base.html' %}
{% block title %}Marca d'Agua{% endblock %}
{% block content %}
<div class="page-header">
<h1>Marca d'Agua</h1>
<p>Configure a marca dagua - o cliente ve com marca, voce recebe sem</p>
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
<option value="diagonal" {{ 'selected' if wm and wm.position == 'diagonal' else '' }}>Diagonal (1 texto grande)</option>
<option value="center" {{ 'selected' if wm and wm.position == 'center' else '' }}>Centro</option>
</select>
<label>Contorno (borda escura)</label>
<input type="checkbox" name="stroke" id="wm-stroke" {{ 'checked' if wm and wm.stroke else '' }} onchange="updatePreview()">
<label>Logo (opcional)</label>
<input type="file" name="logo" accept="image/*">
<hr>
<label>Carregar foto de teste</label>
<input type="file" id="preview-img" accept="image/*" onchange="loadPreviewImage(this)">
<button type="submit" class="btn-primary">Salvar Configuracoes</button>
</form>
</div>
<div class="card" style="flex:1;min-width:280px;">
<h3>Pre-visualizacao</h3>
<canvas id="preview-canvas" width="500" height="375" style="width:100%;border-radius:8px;background:#555;"></canvas>
<p style="color:#777;font-size:12px;margin-top:8px;">A marca dagua e aplicada automaticamente quando o cliente visualiza. Um unico texto grande, sem poluir.</p>
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
var fs=40;x.font='bold '+fs+'px Arial';x.globalAlpha=opacity;
if(position==='diagonal'){x.save();x.translate(c.width/2,c.height/2);x.rotate(-Math.PI/4);var tw=x.measureText(text).width;x.fillText(text,-tw/2,0);if(stroke){x.strokeStyle='rgba(0,0,0,'+opacity+')';x.lineWidth=2;x.strokeText(text,-tw/2,0)}x.restore()}
else{var tw=x.measureText(text).width;x.fillText(text,(c.width-tw)/2,c.height/2);if(stroke){x.strokeStyle='rgba(0,0,0,'+opacity+')';x.lineWidth=2;x.strokeText(text,(c.width-tw)/2,c.height/2)}}
x.globalAlpha=1
}
updatePreview();
</script>
{% endblock %}"""
with open(os.path.join(tpl, 'marca.html'), 'w', encoding='utf-8') as f:
    f.write(marca_html.strip() + '\n')
print('OK: marca.html (preview 1 texto)')

print('\n=== LOGIN DARK + WATERMARK LIMPO! ===')