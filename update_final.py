import os, shutil
base = os.path.dirname(os.path.abspath(__file__))
tpl = os.path.join(base, 'templates')
css_dir = os.path.join(base, 'static', 'css')

# APAGA tudo e recria do zero
if os.path.exists(tpl):
    shutil.rmtree(tpl)
os.makedirs(tpl)
os.makedirs(css_dir, exist_ok=True)

f = {}

f['style.css'] = """*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',Tahoma,sans-serif;background:#f5f6fa;color:#333}
.sidebar{position:fixed;left:0;top:0;width:240px;height:100vh;background:#1e272e;padding:20px;overflow-y:auto}
.sidebar h2{color:#fff;font-size:18px;margin-bottom:20px;padding-bottom:14px;border-bottom:1px solid #353b48}
.sidebar a{display:block;color:#a4b0be;text-decoration:none;padding:10px 14px;border-radius:8px;margin-bottom:3px;font-size:14px}
.sidebar a:hover{background:#353b48;color:#fff}
.sidebar a.active{background:#4a90d9;color:#fff}
.sidebar a.logout{color:#ff6b6b;margin-top:16px}
.main-content{margin-left:240px;padding:28px}
.auth-wrapper{min-height:100vh;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#1e272e,#2d3436)}
.card{background:#fff;border-radius:12px;padding:22px;margin-bottom:18px;box-shadow:0 2px 8px rgba(0,0,0,0.06)}
.card h3{margin-bottom:14px;font-size:17px}
.btn-primary{background:#4a90d9;color:#fff;border:none;padding:10px 18px;border-radius:8px;cursor:pointer;font-size:14px;text-decoration:none;display:inline-block}
.btn-primary:hover{background:#3a7bc8}
.btn-danger{background:#ff6b6b;color:#fff;border:none;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:13px}
.btn-danger:hover{background:#e85555}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:18px}
.page-header{margin-bottom:22px}
.page-header h1{font-size:22px;margin-bottom:4px}
.page-header p{color:#777;font-size:14px}
.flash{padding:10px 18px;border-radius:8px;margin-bottom:14px;font-size:14px}
.flash.success{background:#d4edda;color:#155724}
.flash.error{background:#f8d7da;color:#721c24}
input,select,textarea{width:100%;padding:9px;margin-bottom:10px;border:1px solid #ddd;border-radius:8px;font-size:14px}
input[type=checkbox]{width:auto}
input[type=color]{width:55px;height:38px;padding:0}
input[type=file]{padding:6px}
input[type=range]{padding:0}
label{display:block;font-size:13px;color:#555;margin-bottom:4px}
table{width:100%;border-collapse:collapse;margin-bottom:16px}
th,td{padding:10px;text-align:left;border-bottom:1px solid #eee;font-size:14px}
th{background:#f8f9fa;font-weight:600}
.stats-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:22px}
.stat-card{background:#fff;border-radius:12px;padding:18px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.06)}
.stat-card h3{font-size:28px;color:#4a90d9}
.stat-card p{color:#777;font-size:13px}
.auth-box{background:#fff;border-radius:16px;padding:36px;width:380px;box-shadow:0 10px 40px rgba(0,0,0,0.2)}
.auth-box h1{text-align:center;margin-bottom:22px;font-size:22px}
.auth-box a{color:#4a90d9;text-decoration:none}
hr{margin:18px 0;border:none;border-top:1px solid #eee}
img{max-width:100%}"""

f['base.html'] = """<!DOCTYPE html>
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
{% with messages = get_flashed_messages(with_categories=true) %}
{% if messages %}
{% for category, message in messages %}
<div class="flash {{ category }}">{{ message }}</div>
{% endfor %}
{% endif %}
{% endwith %}
{% block content %}{% endblock %}
</div>
{% else %}
{% with messages = get_flashed_messages(with_categories=true) %}
{% if messages %}
<div style="max-width:380px;margin:16px auto;">
{% for category, message in messages %}
<div class="flash {{ category }}">{{ message }}</div>
{% endfor %}
</div>
{% endif %}
{% endwith %}
{% block content %}{% endblock %}
{% endif %}
</body>
</html>"""

f['login.html'] = """{% extends 'base.html' %}
{% block title %}Login{% endblock %}
{% block content %}
<div class="auth-wrapper">
<div class="auth-box">
<h1>MeuFotoApp</h1>
<form method="POST">
<input type="email" name="email" placeholder="E-mail" required>
<input type="password" name="password" placeholder="Senha" required>
<button type="submit" class="btn-primary" style="width:100%;text-align:center;">Entrar</button>
</form>
<hr>
<a href="{{ url_for('login_google') }}" style="display:block;text-align:center;padding:10px;border:1px solid #ddd;border-radius:8px;text-decoration:none;color:#333;">Entrar com Google</a>
<p style="text-align:center;margin-top:14px;font-size:14px;">Nao tem conta? <a href="{{ url_for('registro') }}">Criar conta</a></p>
</div>
</div>
{% endblock %}"""

f['registro.html'] = """{% extends 'base.html' %}
{% block title %}Criar conta{% endblock %}
{% block content %}
<div class="auth-wrapper">
<div class="auth-box">
<h1>Criar Conta</h1>
<form method="POST">
<input type="text" name="studio_name" placeholder="Nome do Estudio">
<input type="text" name="name" placeholder="Seu nome">
<input type="email" name="email" placeholder="E-mail" required>
<input type="password" name="password" placeholder="Senha" required>
<button type="submit" class="btn-primary" style="width:100%;text-align:center;">Criar conta</button>
</form>
<p style="text-align:center;margin-top:14px;font-size:14px;">Ja tem conta? <a href="{{ url_for('login') }}">Entrar</a></p>
</div>
</div>
{% endblock %}"""

f['dashboard.html'] = """{% extends 'base.html' %}
{% block title %}Dashboard{% endblock %}
{% block content %}
<div class="page-header">
<h1>Dashboard</h1>
<p>Bem-vindo, {{ current_user.name or current_user.studio_name or current_user.email }}!</p>
</div>
{% if trial_days_left is defined and trial_days_left is not none and trial_days_left > 0 and not current_user.is_admin %}
<div class="card" style="background:#fff3cd;border:1px solid #ffeaa7;">
<p>Trial: <strong>{{ trial_days_left }} dia(s)</strong> restante(s). <a href="{{ url_for('planos') }}">Fazer upgrade</a></p>
</div>
{% endif %}
<div class="stats-grid">
<div class="stat-card"><h3>{{ galerias|length }}</h3><p>Galerias</p></div>
<div class="stat-card"><h3>{{ total_fotos }}</h3><p>Fotos</p></div>
<div class="stat-card"><h3>{{ total_selecoes }}</h3><p>Selecoes</p></div>
<div class="stat-card"><h3>{{ current_user.plan|upper }}</h3><p>Plano</p></div>
</div>
<div class="card">
<h3>Galerias Recentes</h3>
{% if galerias %}
<table>
<tr><th>Titulo</th><th>Cliente</th><th>Criada</th><th>Acao</th></tr>
{% for g in galerias %}
<tr>
<td>{{ g.title }}</td>
<td>{{ g.client_name or '-' }}</td>
<td>{{ g.created_at.strftime('%d/%m/%Y') }}</td>
<td><a href="{{ url_for('galeria', gid=g.id) }}" class="btn-primary" style="padding:4px 10px;font-size:12px;">Abrir</a></td>
</tr>
{% endfor %}
</table>
{% else %}
<p style="color:#888;">Nenhuma galeria. <a href="{{ url_for('nova_galeria') }}">Criar agora</a></p>
{% endif %}
</div>
{% endblock %}"""

f['list_galerias.html'] = """{% extends 'base.html' %}
{% block title %}Galerias{% endblock %}
{% block content %}
<div class="page-header">
<h1>Galerias</h1>
<p>Todas as suas galerias</p>
</div>
<div class="card">
{% if galerias %}
<table>
<tr><th>Titulo</th><th>Cliente</th><th>Categoria</th><th>Criada</th><th>Acoes</th></tr>
{% for g in galerias %}
<tr>
<td>{{ g.title }}</td>
<td>{{ g.client_name or '-' }}</td>
<td>{{ g.category or '-' }}</td>
<td>{{ g.created_at.strftime('%d/%m/%Y') }}</td>
<td>
<a href="{{ url_for('galeria', gid=g.id) }}" class="btn-primary" style="padding:4px 10px;font-size:12px;">Abrir</a>
<form method="POST" action="{{ url_for('delete_galeria', gid=g.id) }}" style="display:inline;">
<button type="submit" class="btn-danger" onclick="return confirm('Excluir?')">Excluir</button>
</form>
</td>
</tr>
{% endfor %}
</table>
{% else %}
<p style="color:#888;text-align:center;">Nenhuma galeria. <a href="{{ url_for('nova_galeria') }}">Criar agora</a></p>
{% endif %}
</div>
{% endblock %}"""

f['nova_galeria.html'] = """{% extends 'base.html' %}
{% block title %}Nova Galeria{% endblock %}
{% block content %}
<div class="page-header">
<h1>Nova Galeria</h1>
<p>Crie uma galeria para seu cliente</p>
</div>
<div class="card">
<form method="POST">
<label>Titulo</label>
<input type="text" name="title" placeholder="Ex: Casamento Joao e Maria" required>
<label>Cliente</label>
<input type="text" name="client_name" placeholder="Nome do cliente">
<label>E-mail do cliente</label>
<input type="email" name="client_email" placeholder="cliente@email.com">
<label>Categoria</label>
<select name="category">
<option value="">Selecione</option>
{% for c in categories %}
<option value="{{ c.slug }}">{{ c.label }}</option>
{% endfor %}
</select>
<label>Data do evento</label>
<input type="date" name="event_date">
<label>Mensagem</label>
<textarea name="client_message" rows="3" placeholder="Opcional"></textarea>
<button type="submit" class="btn-primary">Criar Galeria</button>
</form>
</div>
{% endblock %}"""

f['galeria.html'] = """{% extends 'base.html' %}
{% block title %}{{ galeria.title }}{% endblock %}
{% block content %}
<div class="page-header">
<h1>{{ galeria.title }}</h1>
<p>Cliente: {{ galeria.client_name or 'Nao definido' }} | {{ galeria.created_at.strftime('%d/%m/%Y') }}</p>
</div>
<div class="card">
<h3>Enviar Fotos</h3>
<form method="POST" enctype="multipart/form-data">
<input type="file" name="photos" multiple accept="image/*" required>
<button type="submit" class="btn-primary">Enviar</button>
</form>
</div>
<div class="card">
<h3>Link do Cliente</h3>
<p style="word-break:break-all;background:#f8f9fa;padding:10px;border-radius:8px;">
http://localhost:5000/g/{{ galeria.share_token }}
</p>
</div>
{% if selections %}
<div class="card">
<h3>Selecoes ({{ selections|length }})</h3>
<table>
<tr><th>Data</th><th>Pacote</th><th>Status</th><th>Download</th></tr>
{% for s in selections %}
<tr>
<td>{{ s.created_at.strftime('%d/%m/%Y %H:%M') }}</td>
<td>{{ s.package_key or '-' }}</td>
<td>{{ s.status }}</td>
<td><a href="{{ url_for('download_selection', sid=s.id) }}" class="btn-primary" style="padding:4px 10px;font-size:12px;">ZIP</a></td>
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
<img src="{{ url_for('serve_upload', filename=p.filepath) }}" style="width:100%;border-radius:8px;">
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

f['cliente.html'] = """{% extends 'base.html' %}
{% block title %}{{ galeria.title }} - Selecao{% endblock %}
{% block content %}
<div class="auth-wrapper" style="min-height:100vh;padding:20px;">
<div style="max-width:900px;margin:0 auto;">
<div class="page-header" style="color:#fff;">
<h1>{{ galeria.title }}</h1>
<p>Selecione suas fotos favoritas.</p>
</div>
{% if submitted %}
<div class="card" style="text-align:center;padding:40px;">
<h2>Selecao enviada!</h2>
<p>Obrigado! O fotografo recebera sua escolha.</p>
</div>
{% else %}
<form method="POST">
{% if packages %}
<div class="card" style="margin-bottom:16px;">
<label><strong>Pacote:</strong></label>
<select name="package_key" style="padding:8px;">
{% for p in packages %}
<option value="{{ p.key }}">{{ p.label }} - {{ p.limit }} fotos - {{ p.price }}</option>
{% endfor %}
</select>
</div>
{% endif %}
<div class="grid">
{% for p in photos %}
<div style="border-radius:8px;overflow:hidden;background:#fff;">
<label style="display:block;cursor:pointer;position:relative;">
<img src="{{ url_for('serve_upload', filename=p.filepath) }}" style="width:100%;border-radius:8px;">
<input type="checkbox" name="selected_photos" value="{{ p.id }}" style="position:absolute;top:8px;right:8px;width:24px;height:24px;">
</label>
</div>
{% endfor %}
</div>
{% if photos %}
<div style="text-align:center;margin-top:20px;">
<button type="submit" class="btn-primary" style="padding:14px 40px;font-size:16px;">Enviar Selecao</button>
</div>
{% else %}
<div class="card" style="text-align:center;">
<p style="color:#888;">Nenhuma foto disponivel.</p>
</div>
{% endif %}
</form>
{% endif %}
</div>
</div>
{% endblock %}"""

f['selecoes.html'] = """{% extends 'base.html' %}
{% block title %}Selecoes{% endblock %}
{% block content %}
<div class="page-header">
<h1>Selecoes</h1>
<p>Selecoes recebidas dos clientes</p>
</div>
{% if selections %}
<div class="card">
<table>
<tr><th>Data</th><th>Pacote</th><th>Status</th><th>Download</th></tr>
{% for s in selections %}
<tr>
<td>{{ s.created_at.strftime('%d/%m/%Y %H:%M') }}</td>
<td>{{ s.package_key or '-' }}</td>
<td>{{ s.status }}</td>
<td><a href="{{ url_for('download_selection', sid=s.id) }}" class="btn-primary" style="padding:4px 10px;font-size:12px;">ZIP</a></td>
</tr>
{% endfor %}
</table>
</div>
{% else %}
<div class="card" style="text-align:center;">
<p style="color:#888;">Nenhuma selecao recebida.</p>
</div>
{% endif %}
{% endblock %}"""

f['portfolio.html'] = """{% extends 'base.html' %}
{% block title %}Portfolio{% endblock %}
{% block content %}
<div class="page-header">
<h1>Portfolio</h1>
<p>Antes e depois</p>
</div>
{% if not public %}
<form method="POST" enctype="multipart/form-data" action="{{ url_for('portfolio') }}" class="card">
<h3>Adicionar Item</h3>
<input type="text" name="title" placeholder="Titulo" required>
<label>Antes</label>
<input type="file" name="before" accept="image/*">
<label>Depois</label>
<input type="file" name="after" accept="image/*">
<button type="submit" class="btn-primary">Adicionar</button>
</form>
{% endif %}
<div class="grid">
{% for item in items %}
<div class="card">
<h3>{{ item.title }}</h3>
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
<p style="text-align:center;color:#888;margin-top:24px;">Nenhum item.</p>
{% endif %}
{% endblock %}"""

f['catalogo_poses.html'] = """{% extends 'base.html' %}
{% block title %}Catalogo de Poses{% endblock %}
{% block content %}
<div class="page-header">
<h1>Catalogo de Poses</h1>
<p>Inspiracoes para clientes</p>
</div>
{% if not public %}
<form method="POST" enctype="multipart/form-data" action="{{ url_for('catalogo_poses') }}" class="card">
<h3>Adicionar Pose</h3>
<input type="file" name="photo" accept="image/*" required>
{% if categories is defined %}
<select name="category">
<option value="">Sem categoria</option>
{% for c in categories %}
<option value="{{ c.slug }}">{{ c.label }}</option>
{% endfor %}
</select>
{% endif %}
<input type="text" name="group_name" placeholder="Grupo">
<textarea name="prompt_text" placeholder="Descricao" rows="3"></textarea>
<button type="submit" class="btn-primary">Adicionar</button>
</form>
{% endif %}
<div class="grid">
{% for pose in poses %}
<div class="card">
<img src="{{ url_for('serve_upload', filename=pose.filepath) }}" style="width:100%;border-radius:8px;">
{% if pose.group_name %}<p><strong>{{ pose.group_name }}</strong></p>{% endif %}
{% if pose.prompt_text %}<p style="font-size:14px;color:#666;">{{ pose.prompt_text }}</p>{% endif %}
{% if not public %}
<form method="POST" action="{{ url_for('delete_pose', pid=pose.id) }}" style="margin-top:8px;">
<button type="submit" class="btn-danger">Excluir</button>
</form>
{% endif %}
</div>
{% endfor %}
</div>
{% if not poses %}
<p style="text-align:center;color:#888;margin-top:24px;">Nenhuma pose.</p>
{% endif %}
{% endblock %}"""

f['marca.html'] = """{% extends 'base.html' %}
{% block title %}Marca d Agua{% endblock %}
{% block content %}
<div class="page-header">
<h1>Marca d Agua</h1>
<p>Configure a marca dagua</p>
</div>
<div style="display:flex;gap:20px;flex-wrap:wrap;">
<div class="card" style="flex:1;min-width:280px;">
<form method="POST" enctype="multipart/form-data" action="{{ url_for('marca') }}" id="wm-form">
<label>Texto</label>
<input type="text" name="text" id="wm-text" value="{{ wm.text if wm else '' }}" placeholder="Seu nome" oninput="updatePreview()">
<label>Cor</label>
<input type="color" name="color" id="wm-color" value="{{ wm.color if wm else '#ffffff' }}" oninput="updatePreview()">
<label>Opacidade: <span id="opacity-val">{{ wm.opacity if wm else 30 }}%</span></label>
<input type="range" name="opacity" id="wm-opacity" value="{{ wm.opacity if wm else 30 }}" min="0" max="100" oninput="updatePreview()">
<label>Posicao</label>
<select name="position" id="wm-position" onchange="updatePreview()">
<option value="diagonal" {{ 'selected' if wm and wm.position == 'diagonal' else '' }}>Diagonal</option>
<option value="center" {{ 'selected' if wm and wm.position == 'center' else '' }}>Centro</option>
</select>
<label>Contorno</label>
<input type="checkbox" name="stroke" id="wm-stroke" {{ 'checked' if wm and wm.stroke else '' }} onchange="updatePreview()">
<label>Logo (opcional)</label>
<input type="file" name="logo" accept="image/*">
<button type="submit" class="btn-primary">Salvar</button>
</form>
</div>
<div class="card" style="flex:1;min-width:280px;">
<h3>Pre-visualizacao</h3>
<canvas id="preview-canvas" width="400" height="300" style="width:100%;border-radius:8px;background:#555;"></canvas>
</div>
</div>
<script>
function updatePreview(){var c=document.getElementById('preview-canvas');var x=c.getContext('2d');var g=x.createLinearGradient(0,0,c.width,c.height);g.addColorStop(0,'#666');g.addColorStop(1,'#555');x.fillStyle=g;x.fillRect(0,0,c.width,c.height);var t=document.getElementById('wm-text').value||'MeuFotoApp';var cl=document.getElementById('wm-color').value;var op=document.getElementById('wm-opacity').value/100;var pos=document.getElementById('wm-position').value;var st=document.getElementById('wm-stroke').checked;document.getElementById('opacity-val').textContent=document.getElementById('wm-opacity').value+'%';x.font='bold 20px Arial';x.globalAlpha=op;if(pos==='diagonal'){for(var y=-20;y<c.height+20;y+=80){for(var xx=-100;xx<c.width+100;xx+=200){if(st){x.strokeStyle='rgba(0,0,0,'+op+')';x.lineWidth=2;x.strokeText(t,xx,y)}x.fillStyle=cl;x.fillText(t,xx,y)}}}else{var m=x.measureText(t);var px=(c.width-m.width)/2;var py=c.height/2;if(st){x.strokeStyle='rgba(0,0,0,'+op+')';x.lineWidth=2;x.strokeText(t,px,py)}x.fillStyle=cl;x.fillText(t,px,py)}x.globalAlpha=1}
updatePreview();
</script>
{% endblock %}"""

f['planos.html'] = """{% extends 'base.html' %}
{% block title %}Planos{% endblock %}
{% block content %}
<div class="page-header">
<h1>Planos</h1>
<p>Escolha seu plano</p>
</div>
<div class="grid">
<div class="card" style="text-align:center;">
<h3 style="color:#4a90d9;">Gratuito</h3>
<p style="font-size:22px;font-weight:bold;">R$ 0<span style="font-size:13px;color:#999;">/mes</span></p>
<ul style="list-style:none;padding:0;font-size:14px;line-height:1.8;text-align:left;">
<li>3 galerias</li><li>50 fotos/galeria</li><li>Selecao pelo cliente</li><li>Marca dagua</li>
</ul>
</div>
<div class="card" style="text-align:center;">
<h3 style="color:#27ae60;">Pro</h3>
<p style="font-size:22px;font-weight:bold;">R$ 49<span style="font-size:13px;color:#999;">/mes</span></p>
<ul style="list-style:none;padding:0;font-size:14px;line-height:1.8;text-align:left;">
<li>Galerias ilimitadas</li><li>Fotos ilimitadas</li><li>Portfolio</li><li>Catalogo de poses</li><li>Redimensionamento</li>
</ul>
</div>
<div class="card" style="text-align:center;">
<h3 style="color:#e67e22;">Premium</h3>
<p style="font-size:22px;font-weight:bold;">R$ 99<span style="font-size:13px;color:#999;">/mes</span></p>
<ul style="list-style:none;padding:0;font-size:14px;line-height:1.8;text-align:left;">
<li>Tudo do Pro</li><li>Multiusuarios</li><li>Logo na marca</li><li>Entregas por plataforma</li><li>Suporte prioritario</li>
</ul>
</div>
</div>
<div class="card">
<h3>Pacotes de Selecao</h3>
<table>
<tr><th>Nome</th><th>Limite</th><th>Preco</th>{% if current_user.is_authenticated and current_user.is_admin %}<th>Acao</th>{% endif %}</tr>
{% for p in packages %}
<tr>
<td>{{ p.label }}</td>
<td>{{ p.limit }} fotos</td>
<td>{{ p.price }}</td>
{% if current_user.is_authenticated and current_user.is_admin %}
<td><form method="POST" action="{{ url_for('delete_pacote', pid=p.id) }}" style="display:inline;"><button type="submit" class="btn-danger">Excluir</button></form></td>
{% endif %}
</tr>
{% else %}
<tr><td colspan="4" style="text-align:center;color:#999;">Nenhum pacote.</td></tr>
{% endfor %}
</table>
</div>
{% endblock %}"""

f['configuracoes.html'] = """{% extends 'base.html' %}
{% block title %}Configuracoes{% endblock %}
{% block content %}
<div class="page-header">
<h1>Configuracoes</h1>
<p>Gerencie sua conta</p>
</div>
<div class="card">
<h3>Conta</h3>
<p><strong>Estudio:</strong> {{ current_user.studio_name or 'Nao definido' }}</p>
<p><strong>Nome:</strong> {{ current_user.name or 'Nao definido' }}</p>
<p><strong>E-mail:</strong> {{ current_user.email }}</p>
<p><strong>Plano:</strong> {{ current_user.plan or 'free' }}</p>
{% if current_user.is_admin %}<p><strong>Acesso:</strong> Administrador</p>{% endif %}
</div>
{% if current_user.is_admin %}
<div class="card">
<h3>Configuracoes do App</h3>
<form method="POST" action="{{ url_for('admin_settings') }}">
<label>Nome do App</label>
<input type="text" name="app_name" value="{{ site_settings.app_name if site_settings else 'MeuFotoApp' }}">
<label>Cor Principal</label>
<input type="color" name="primary_color" value="{{ site_settings.primary_color if site_settings else '#4a90d9' }}">
<h4 style="margin-top:14px;">E-mail (SMTP)</h4>
<label>SMTP Host</label>
<input type="text" name="smtp_host" value="{{ site_settings.smtp_host if site_settings else '' }}" placeholder="smtp.gmail.com">
<label>SMTP Port</label>
<input type="number" name="smtp_port" value="{{ site_settings.smtp_port if site_settings else '' }}" placeholder="587">
<label>SMTP User</label>
<input type="text" name="smtp_user" value="{{ site_settings.smtp_user if site_settings else '' }}" placeholder="seuemail@gmail.com">
<label>SMTP Password</label>
<input type="password" name="smtp_password" value="{{ site_settings.smtp_password if site_settings else '' }}" placeholder="App Password">
<button type="submit" class="btn-primary">Salvar</button>
</form>
</div>
{% endif %}
<div class="card">
<h3>Acesso Rapido</h3>
<div style="display:flex;gap:10px;flex-wrap:wrap;">
<a href="{{ url_for('marca') }}" class="btn-primary">Marca d Agua</a>
<a href="{{ url_for('portfolio') }}" class="btn-primary">Portfolio</a>
<a href="{{ url_for('catalogo_poses') }}" class="btn-primary">Catalogo</a>
<a href="{{ url_for('planos') }}" class="btn-primary">Planos</a>
{% if current_user.is_admin %}
<a href="{{ url_for('admin') }}" class="btn-primary">Admin</a>
{% endif %}
</div>
</div>
{% endblock %}"""

f['admin.html'] = """{% extends 'base.html' %}
{% block title %}Admin{% endblock %}
{% block content %}
<div class="page-header">
<h1>Painel Admin</h1>
<p>Gerencie tudo</p>
</div>
<div class="stats-grid">
<div class="stat-card"><h3>{{ total_users }}</h3><p>Usuarios</p></div>
<div class="stat-card"><h3>{{ total_galerias }}</h3><p>Galerias</p></div>
<div class="stat-card"><h3>{{ total_fotos }}</h3><p>Fotos</p></div>
<div class="stat-card"><h3>{{ total_selecoes }}</h3><p>Selecoes</p></div>
</div>
<div class="card">
<h3>Configuracoes do App</h3>
<form method="POST" action="{{ url_for('admin_settings') }}">
<label>Nome do App</label>
<input type="text" name="app_name" value="{{ settings.app_name if settings else 'MeuFotoApp' }}">
<label>Cor Principal</label>
<input type="color" name="primary_color" value="{{ settings.primary_color if settings else '#4a90d9' }}">
<label>SMTP Host</label>
<input type="text" name="smtp_host" value="{{ settings.smtp_host if settings else '' }}" placeholder="smtp.gmail.com">
<label>SMTP Port</label>
<input type="number" name="smtp_port" value="{{ settings.smtp_port if settings else '' }}" placeholder="587">
<label>SMTP User</label>
<input type="text" name="smtp_user" value="{{ settings.smtp_user if settings else '' }}" placeholder="seuemail@gmail.com">
<label>SMTP Password</label>
<input type="password" name="smtp_password" value="{{ settings.smtp_password if settings else '' }}">
<button type="submit" class="btn-primary">Salvar</button>
</form>
</div>
<div class="card">
<h3>Categorias</h3>
<form method="POST" action="{{ url_for('admin_categorias') }}" style="display:flex;gap:6px;flex-wrap:wrap;">
<input type="text" name="slug" placeholder="slug" style="flex:1;min-width:100px;">
<input type="text" name="label" placeholder="Nome" style="flex:2;min-width:140px;">
<button type="submit" class="btn-primary">+ Adicionar</button>
</form>
<div style="margin-top:10px;">
{% for c in categories %}
<span style="display:inline-block;background:#e8f0fe;padding:5px 10px;border-radius:20px;margin:3px;font-size:13px;">
{{ c.label }}
<form method="POST" action="{{ url_for('delete_categoria', cid=c.id) }}" style="display:inline;">
<button type="submit" style="background:none;border:none;color:#ff6b6b;cursor:pointer;font-size:15px;">x</button>
</form>
</span>
{% endfor %}
</div>
</div>
<div class="card">
<h3>Pacotes</h3>
<form method="POST" action="{{ url_for('admin_pacotes') }}" style="display:flex;gap:6px;flex-wrap:wrap;">
<input type="text" name="key" placeholder="key" style="flex:1;min-width:90px;">
<input type="text" name="label" placeholder="Nome" style="flex:1;min-width:100px;">
<input type="number" name="limit" placeholder="Qtd" style="flex:1;min-width:70px;">
<input type="text" name="price" placeholder="Preco" style="flex:1;min-width:70px;">
<button type="submit" class="btn-primary">+ Adicionar</button>
</form>
<table style="margin-top:10px;">
<tr><th>Nome</th><th>Limite</th><th>Preco</th><th>Acao</th></tr>
{% for p in packages %}
<tr>
<td>{{ p.label }}</td><td>{{ p.limit }} fotos</td><td>{{ p.price }}</td>
<td><form method="POST" action="{{ url_for('delete_pacote', pid=p.id) }}" style="display:inline;"><button type="submit" class="btn-danger">Excluir</button></form></td>
</tr>
{% endfor %}
</table>
</div>
<div class="card">
<h3>Usuarios</h3>
<table>
<tr><th>Nome</th><th>Email</th><th>Plano</th><th>Admin</th><th>Status</th><th>Acoes</th></tr>
{% for u in users %}
<tr>
<td>{{ u.name or u.studio_name or u.email }}</td>
<td>{{ u.email }}</td>
<td>
<form method="POST" action="{{ url_for('change_plan', uid=u.id) }}">
<select name="plan" onchange="this.form.submit()" style="padding:4px;width:auto;">
<option value="free" {{ 'selected' if u.plan == 'free' else '' }}>Free</option>
<option value="pro" {{ 'selected' if u.plan == 'pro' else '' }}>Pro</option>
<option value="premium" {{ 'selected' if u.plan == 'premium' else '' }}>Premium</option>
</select>
</form>
</td>
<td>
<form method="POST" action="{{ url_for('toggle_admin', uid=u.id) }}">
<button type="submit" style="padding:4px 8px;border:none;border-radius:4px;cursor:pointer;background:{{ '#4a90d9' if u.is_admin else '#ccc' }};color:{{ '#fff' if u.is_admin else '#333' }};">{{ 'Sim' if u.is_admin else 'Nao' }}</button>
</form>
</td>
<td>
<form method="POST" action="{{ url_for('toggle_active', uid=u.id) }}">
<button type="submit" style="padding:4px 8px;border:none;border-radius:4px;cursor:pointer;background:{{ '#27ae60' if u.active else '#e74c3c' }};color:#fff;">{{ 'Ativo' if u.active else 'Inativo' }}</button>
</form>
</td>
<td>
{% if u.id != current_user.id %}
<form method="POST" action="{{ url_for('delete_user', uid=u.id) }}" style="display:inline;">
<button type="submit" class="btn-danger" onclick="return confirm('Excluir usuario?')">Excluir</button>
</form>
{% endif %}
</td>
</tr>
{% endfor %}
</table>
</div>
{% endblock %}"""

# Escreve CSS
with open(os.path.join(css_dir, 'style.css'), 'w', encoding='utf-8') as fh:
    fh.write(f['style.css'].strip() + '\n')
print('OK: style.css')

# Escreve todos os templates
for name in ['base.html','login.html','registro.html','dashboard.html','list_galerias.html','nova_galeria.html','galeria.html','cliente.html','selecoes.html','portfolio.html','catalogo_poses.html','marca.html','planos.html','configuracoes.html','admin.html']:
    with open(os.path.join(tpl, name), 'w', encoding='utf-8') as fh:
        fh.write(f[name].strip() + '\n')
    print(f'OK: {name}')

print('\nTODOS os templates recriados do zero!')