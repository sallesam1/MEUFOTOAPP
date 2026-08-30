import os
base = os.path.dirname(os.path.abspath(__file__))
tpl = os.path.join(base, 'templates')
css_dir = os.path.join(base, 'static', 'css')
os.makedirs(tpl, exist_ok=True)
os.makedirs(css_dir, exist_ok=True)
files = {}

files['style.css'] = '''* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Segoe UI',Tahoma,sans-serif; background:#f5f6fa; color:#333; }
.sidebar { position:fixed; left:0; top:0; width:240px; height:100vh; background:#1e272e; padding:20px; overflow-y:auto; }
.sidebar h2 { color:#fff; font-size:18px; margin-bottom:20px; padding-bottom:14px; border-bottom:1px solid #353b48; }
.sidebar a { display:block; color:#a4b0be; text-decoration:none; padding:10px 14px; border-radius:8px; margin-bottom:3px; font-size:14px; }
.sidebar a:hover { background:#353b48; color:#fff; }
.sidebar a.active { background:#4a90d9; color:#fff; }
.sidebar a.logout { color:#ff6b6b; margin-top:16px; }
.main-content { margin-left:240px; padding:28px; }
.auth-wrapper { min-height:100vh; display:flex; align-items:center; justify-content:center; background:linear-gradient(135deg,#1e272e,#2d3436); }
.card { background:#fff; border-radius:12px; padding:22px; margin-bottom:18px; box-shadow:0 2px 8px rgba(0,0,0,0.06); }
.card h3 { margin-bottom:14px; font-size:17px; }
.btn-primary { background:#4a90d9; color:#fff; border:none; padding:10px 18px; border-radius:8px; cursor:pointer; font-size:14px; text-decoration:none; display:inline-block; }
.btn-primary:hover { background:#3a7bc8; }
.btn-danger { background:#ff6b6b; color:#fff; border:none; padding:6px 14px; border-radius:6px; cursor:pointer; font-size:13px; }
.btn-danger:hover { background:#e85555; }
.grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:18px; }
.page-header { margin-bottom:22px; }
.page-header h1 { font-size:22px; margin-bottom:4px; }
.page-header p { color:#777; font-size:14px; }
.flash { padding:10px 18px; border-radius:8px; margin-bottom:14px; font-size:14px; }
.flash.success { background:#d4edda; color:#155724; }
.flash.error { background:#f8d7da; color:#721c24; }
input,select,textarea { width:100%; padding:9px; margin-bottom:10px; border:1px solid #ddd; border-radius:8px; font-size:14px; }
input[type=checkbox] { width:auto; }
input[type=color] { width:55px; height:38px; padding:0; }
input[type=file] { padding:6px; }
input[type=range] { padding:0; }
label { display:block; font-size:13px; color:#555; margin-bottom:4px; }
table { width:100%; border-collapse:collapse; margin-bottom:16px; }
th,td { padding:10px; text-align:left; border-bottom:1px solid #eee; font-size:14px; }
th { background:#f8f9fa; font-weight:600; }
.stats-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-bottom:22px; }
.stat-card { background:#fff; border-radius:12px; padding:18px; text-align:center; box-shadow:0 2px 8px rgba(0,0,0,0.06); }
.stat-card h3 { font-size:28px; color:#4a90d9; }
.stat-card p { color:#777; font-size:13px; }
.auth-box { background:#fff; border-radius:16px; padding:36px; width:380px; box-shadow:0 10px 40px rgba(0,0,0,0.2); }
.auth-box h1 { text-align:center; margin-bottom:22px; font-size:22px; }
.auth-box a { color:#4a90d9; text-decoration:none; }
hr { margin:18px 0; border:none; border-top:1px solid #eee; }
img { max-width:100%; }'''

files['base.html'] = '''<!DOCTYPE html>
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
<a href="{{ url_for('admin') }}" style="background:#353b48; color:#fff;">ADMIN</a>
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
<div style="max-width:380px; margin:16px auto;">
{% for category, message in messages %}
<div class="flash {{ category }}">{{ message }}</div>
{% endfor %}
</div>
{% endif %}
{% endwith %}
{% block content %}{% endblock %}
{% endif %}
</body>
</html>'''

files['login.html'] = '''{% extends 'base.html' %}
{% block title %}Login — {{ site_settings.app_name if site_settings else 'MeuFotoApp' }}{% endblock %}
{% block content %}
<div class="auth-wrapper">
<div class="auth-box">
<h1>{{ site_settings.app_name if site_settings else 'MeuFotoApp' }}</h1>
<form method="POST">
<input type="email" name="email" placeholder="E-mail" required>
<input type="password" name="password" placeholder="Senha" required>
<button type="submit" class="btn-primary" style="width:100%; text-align:center;">Entrar</button>
</form>
<hr>
<a href="{{ url_for('login_google') }}" style="display:block; text-align:center; padding:10px; border:1px solid #ddd; border-radius:8px; text-decoration:none; color:#333;">Entrar com Google</a>
<p style="text-align:center; margin-top:14px; font-size:14px;">Nao tem conta? <a href="{{ url_for('registro') }}">Criar conta</a></p>
</div>
</div>
{% endblock %}'''

files['registro.html'] = '''{% extends 'base.html' %}
{% block title %}Criar conta — {{ site_settings.app_name if site_settings else 'MeuFotoApp' }}{% endblock %}
{% block content %}
<div class="auth-wrapper">
<div class="auth-box">
<h1>Criar Conta</h1>
<form method="POST">
<input type="text" name="studio_name" placeholder="Nome do Estudio">
<input type="text" name="name" placeholder="Seu nome">
<input type="email" name="email" placeholder="E-mail" required>
<input type="password" name="password" placeholder="Senha" required>
<button type="submit" class="btn-primary" style="width:100%; text-align:center;">Criar conta</button>
</form>
<p style="text-align:center; margin-top:14px; font-size:14px;">Ja tem conta? <a href="{{ url_for('login') }}">Entrar</a></p>
</div>
</div>
{% endblock %}'''

files['admin.html'] = '''{% extends 'base.html' %}
{% block title %}Admin — {{ site_settings.app_name if site_settings else 'MeuFotoApp' }}{% endblock %}
{% block content %}
<div class="page-header">
<h1>Painel Admin</h1>
<p>Gerencie usuarios, categorias, pacotes e configuracoes</p>
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
<h4 style="margin-top:14px;">E-mail (SMTP)</h4>
<label>SMTP Host (Gmail: smtp.gmail.com)</label>
<input type="text" name="smtp_host" value="{{ settings.smtp_host if settings else '' }}" placeholder="smtp.gmail.com">
<label>SMTP Port (Gmail: 587)</label>
<input type="number" name="smtp_port" value="{{ settings.smtp_port if settings else '' }}" placeholder="587">
<label>SMTP User (seu Gmail)</label>
<input type="text" name="smtp_user" value="{{ settings.smtp_user if settings else '' }}" placeholder="seuemail@gmail.com">
<label>SMTP Password (App Password)</label>
<input type="password" name="smtp_password" value="{{ settings.smtp_password if settings else '' }}" placeholder="App Password">
<button type="submit" class="btn-primary">Salvar</button>
</form>
</div>
<div class="card">
<h3>Categorias</h3>
<form method="POST" action="{{ url_for('admin_categorias') }}" style="display:flex; gap:6px; flex-wrap:wrap;">
<input type="text" name="slug" placeholder="slug" style="flex:1; min-width:100px;">
<input type="text" name="label" placeholder="Nome" style="flex:2; min-width:140px;">
<button type="submit" class="btn-primary">+ Adicionar</button>
</form>
<div style="margin-top:10px;">
{% for c in categories %}
<span style="display:inline-block; background:#e8f0fe; padding:5px 10px; border-radius:20px; margin:3px; font-size:13px;">
{{ c.label }}
<form method="POST" action="{{ url_for('delete_categoria', cid=c.id) }}" style="display:inline;">
<button type="submit" style="background:none; border:none; color:#ff6b6b; cursor:pointer; font-size:15px;">x</button>
</form>
</span>
{% endfor %}
</div>
</div>
<div class="card">
<h3>Pacotes de Selecao</h3>
<form method="POST" action="{{ url_for('admin_pacotes') }}" style="display:flex; gap:6px; flex-wrap:wrap;">
<input type="text" name="key" placeholder="key" style="flex:1; min-width:90px;">
<input type="text" name="label" placeholder="Nome" style="flex:1; min-width:100px;">
<input type="number" name="limit" placeholder="Qtd" style="flex:1; min-width:70px;">
<input type="text" name="price" placeholder="Preco" style="flex:1; min-width:70px;">
<button type="submit" class="btn-primary">+ Adicionar</button>
</form>
<table style="margin-top:10px;">
<tr><th>Nome</th><th>Limite</th><th>Preco</th><th>Acao</th></tr>
{% for p in packages %}
<tr>
<td>{{ p.label }}</td>
<td>{{ p.limit }} fotos</td>
<td>{{ p.price }}</td>
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
<select name="plan" onchange="this.form.submit()" style="padding:4px; width:auto;">
<option value="free" {{ 'selected' if u.plan == 'free' else '' }}>Free</option>
<option value="pro" {{ 'selected' if u.plan == 'pro' else '' }}>Pro</option>
<option value="premium" {{ 'selected' if u.plan == 'premium' else '' }}>Premium</option>
</select>
</form>
</td>
<td>
<form method="POST" action="{{ url_for('toggle_admin', uid=u.id) }}">
<button type="submit" style="padding:4px 8px; border:none; border-radius:4px; cursor:pointer; background:{{ '#4a90d9' if u.is_admin else '#ccc' }}; color:{{ '#fff' if u.is_admin else '#333' }};">{{ 'Sim' if u.is_admin else 'Nao' }}</button>
</form>
</td>
<td>
<form method="POST" action="{{ url_for('toggle_active', uid=u.id) }}">
<button type="submit" style="padding:4px 8px; border:none; border-radius:4px; cursor:pointer; background:{{ '#27ae60' if u.active else '#e74c3c' }}; color:#fff;">{{ 'Ativo' if u.active else 'Inativo' }}</button>
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
{% endblock %}'''

files['planos.html'] = '''{% extends 'base.html' %}
{% block title %}Planos — {{ site_settings.app_name if site_settings else 'MeuFotoApp' }}{% endblock %}
{% block content %}
<div class="page-header">
<h1>Planos e Pacotes</h1>
<p>Gerencie seus planos e precos</p>
</div>
<div class="card">
<h3>Planos de Assinatura</h3>
<div class="grid">
<div style="border:1px solid #e0e0e0; border-radius:12px; padding:18px;">
<h4 style="color:#4a90d9;">Gratuito</h4>
<p style="font-size:22px; font-weight:bold;">R$ 0<span style="font-size:13px; color:#999;">/mes</span></p>
<ul style="list-style:none; padding:0; font-size:14px; line-height:1.8;">
<li>3 galerias ativas</li>
<li>Ate 50 fotos por galeria</li>
<li>Selecao pelo cliente</li>
<li>Marca dagua automatica</li>
</ul>
</div>
<div style="border:1px solid #e0e0e0; border-radius:12px; padding:18px;">
<h4 style="color:#27ae60;">Pro</h4>
<p style="font-size:22px; font-weight:bold;">R$ 49<span style="font-size:13px; color:#999;">/mes</span></p>
<ul style="list-style:none; padding:0; font-size:14px; line-height:1.8;">
<li>Galerias ilimitadas</li>
<li>Fotos ilimitadas</li>
<li>Portfolio publico</li>
<li>Catalogo de poses</li>
<li>Redimensionamento</li>
</ul>
</div>
<div style="border:1px solid #e0e0e0; border-radius:12px; padding:18px;">
<h4 style="color:#e67e22;">Premium</h4>
<p style="font-size:22px; font-weight:bold;">R$ 99<span style="font-size:13px; color:#999;">/mes</span></p>
<ul style="list-style:none; padding:0; font-size:14px; line-height:1.8;">
<li>Tudo do Pro</li>
<li>Multiusuarios (equipe)</li>
<li>Logo na marca dagua</li>
<li>Entregas por plataforma</li>
<li>Suporte prioritario</li>
</ul>
</div>
</div>
</div>
<div class="card">
<h3>Pacotes de Selecao</h3>
<p style="color:#777; margin-bottom:14px; font-size:14px;">Pacotes que seus clientes escolhem ao selecionar fotos.</p>
{% if current_user.is_authenticated and current_user.is_admin %}
<form method="POST" action="{{ url_for('admin_pacotes') }}" style="display:flex; gap:6px; flex-wrap:wrap; margin-bottom:14px;">
<input type="text" name="key" placeholder="key" style="flex:1; min-width:90px;">
<input type="text" name="label" placeholder="Nome" style="flex:1; min-width:100px;">
<input type="number" name="limit" placeholder="Qtd" style="flex:1; min-width:70px;">
<input type="text" name="price" placeholder="Preco" style="flex:1; min-width:70px;">
<button type="submit" class="btn-primary">+ Adicionar</button>
</form>
{% endif %}
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
<tr><td colspan="4" style="text-align:center; color:#999;">Nenhum pacote cadastrado.</td></tr>
{% endfor %}
</table>
</div>
{% if current_user.is_authenticated and not current_user.is_admin %}
<div class="card">
<h3>Trial</h3>
{% if current_user.trial_started_at %}
<p>Inicio: {{ current_user.trial_started_at.strftime('%d/%m/%Y') }}</p>
{% endif %}
<a href="{{ url_for('planos') }}" class="btn-primary">Ver Planos</a>
</div>
{% endif %}
{% endblock %}'''

files['configuracoes.html'] = '''{% extends 'base.html' %}
{% block title %}Configuracoes — {{ site_settings.app_name if site_settings else 'MeuFotoApp' }}{% endblock %}
{% block content %}
<div class="page-header">
<h1>Configuracoes</h1>
<p>Gerencie sua conta e preferencias</p>
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
<label>SMTP Host (Gmail: smtp.gmail.com)</label>
<input type="text" name="smtp_host" value="{{ site_settings.smtp_host if site_settings else '' }}" placeholder="smtp.gmail.com">
<label>SMTP Port (Gmail: 587)</label>
<input type="number" name="smtp_port" value="{{ site_settings.smtp_port if site_settings else '' }}" placeholder="587">
<label>SMTP User (seu Gmail)</label>
<input type="text" name="smtp_user" value="{{ site_settings.smtp_user if site_settings else '' }}" placeholder="seuemail@gmail.com">
<label>SMTP Password (App Password)</label>
<input type="password" name="smtp_password" value="{{ site_settings.smtp_password if site_settings else '' }}" placeholder="App Password">
<button type="submit" class="btn-primary">Salvar Configuracoes</button>
</form>
</div>
{% endif %}
<div class="card">
<h3>Acesso Rapido</h3>
<div style="display:flex; gap:10px; flex-wrap:wrap;">
<a href="{{ url_for('marca') }}" class="btn-primary">Marca d Agua</a>
<a href="{{ url_for('portfolio') }}" class="btn-primary">Portfolio</a>
<a href="{{ url_for('catalogo_poses') }}" class="btn-primary">Catalogo de Poses</a>
<a href="{{ url_for('planos') }}" class="btn-primary">Planos</a>
{% if current_user.is_admin %}
<a href="{{ url_for('admin') }}" class="btn-primary">Painel Admin</a>
{% endif %}
</div>
</div>
{% endblock %}'''

files['marca.html'] = '''{% extends 'base.html' %}
{% block title %}Marca d Agua — {{ site_settings.app_name if site_settings else 'MeuFotoApp' }}{% endblock %}
{% block content %}
<div class="page-header">
<h1>Marca d Agua</h1>
<p>Configure a marca dagua aplicada nas suas fotos</p>
</div>
<div style="display:flex; gap:20px; flex-wrap:wrap;">
<div class="card" style="flex:1; min-width:280px;">
<form method="POST" enctype="multipart/form-data" action="{{ url_for('marca') }}" id="wm-form">
<label>Texto da marca dagua</label>
<input type="text" name="text" id="wm-text" value="{{ wm.text if wm else '' }}" placeholder="Seu nome ou estudio" oninput="updatePreview()">
<label>Cor</label>
<input type="color" name="color" id="wm-color" value="{{ wm.color if wm else '#ffffff' }}" oninput="updatePreview()">
<label>Opacidade: <span id="opacity-val">{{ wm.opacity if wm else 30 }}%</span></label>
<input type="range" name="opacity" id="wm-opacity" value="{{ wm.opacity if wm else 30 }}" min="0" max="100" oninput="updatePreview()">
<label>Posicao</label>
<select name="position" id="wm-position" onchange="updatePreview()">
<option value="diagonal" {{ 'selected' if wm and wm.position == 'diagonal' else '' }}>Diagonal (repetida)</option>
<option value="center" {{ 'selected' if wm and wm.position == 'center' else '' }}>Centro</option>
</select>
<label>Contorno (borda escura nas letras)</label>
<input type="checkbox" name="stroke" id="wm-stroke" {{ 'checked' if wm and wm.stroke else '' }} onchange="updatePreview()">
<label>Logo (opcional)</label>
<input type="file" name="logo" accept="image/*">
<button type="submit" class="btn-primary">Salvar Configuracoes</button>
</form>
</div>
<div class="card" style="flex:1; min-width:280px;">
<h3>Pre-visualizacao</h3>
<canvas id="preview-canvas" width="400" height="300" style="width:100%; border-radius:8px; background:#555;"></canvas>
<p style="color:#777; font-size:12px; margin-top:8px;">Simulacao da marca dagua. A real sera aplicada nas fotos no upload.</p>
</div>
</div>
<script>
function updatePreview() {
var canvas = document.getElementById('preview-canvas');
var ctx = canvas.getContext('2d');
var grad = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
grad.addColorStop(0, '#666');
grad.addColorStop(0.5, '#888');
grad.addColorStop(1, '#555');
ctx.fillStyle = grad;
ctx.fillRect(0, 0, canvas.width, canvas.height);
var text = document.getElementById('wm-text').value || 'MeuFotoApp';
var color = document.getElementById('wm-color').value;
var opacity = document.getElementById('wm-opacity').value / 100;
var position = document.getElementById('wm-position').value;
var stroke = document.getElementById('wm-stroke').checked;
document.getElementById('opacity-val').textContent = document.getElementById('wm-opacity').value + '%';
ctx.font = 'bold 20px Arial';
ctx.globalAlpha = opacity;
if (position === 'diagonal') {
for (var y = -20; y < canvas.height + 20; y += 80) {
for (var x = -100; x < canvas.width + 100; x += 200) {
if (stroke) { ctx.strokeStyle = 'rgba(0,0,0,' + opacity + ')'; ctx.lineWidth = 2; ctx.strokeText(text, x, y); }
ctx.fillStyle = color;
ctx.fillText(text, x, y);
}
}
} else {
var m = ctx.measureText(text);
var x = (canvas.width - m.width) / 2;
var y = canvas.height / 2;
if (stroke) { ctx.strokeStyle = 'rgba(0,0,0,' + opacity + ')'; ctx.lineWidth = 2; ctx.strokeText(text, x, y); }
ctx.fillStyle = color;
ctx.fillText(text, x, y);
}
ctx.globalAlpha = 1;
}
updatePreview();
</script>
{% endblock %}'''

for name, content in files.items():
    if name.endswith('.css'):
        path = os.path.join(css_dir, name)
    else:
        path = os.path.join(tpl, name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f'OK: {name}')

print('\nTemplates atualizados com sucesso!')