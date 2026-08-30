import os
tpl = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

# ===== 1. ADMIN.HTML (sem botao de toggle admin) =====
admin_html = """{% extends 'base.html' %}
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
<tr><th>Nome</th><th>Email</th><th>Plano</th><th>Status</th><th>Acoes</th></tr>
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
with open(os.path.join(tpl, 'admin.html'), 'w', encoding='utf-8') as f:
    f.write(admin_html.strip() + '\n')
print('OK: admin.html (sem botao toggle)')

# ===== 2. PORTFOLIO.HTML (com links de entrega visiveis) =====
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
<p style="font-size:13px;word-break:break-all;margin:0;color:#333;">http://localhost:5000/p/{{ item.share_token }}</p>
<p style="font-size:11px;color:#666;margin:6px 0 0 0;">Envie este link para o cliente ver o antes e depois</p>
</div>
{% endif %}
<div style="display:flex;gap:8px;flex-wrap:wrap;">
{% if item.before_path %}
<div>
<p style="font-size:12px;color:#888;margin-bottom:4px;">ANTES</p>
<img src="{{ url_for('serve_upload', filename=item.before_path) }}" style="width:200px;border-radius:8px;">
</div>
{% endif %}
{% if item.after_path %}
<div>
<p style="font-size:12px;color:#888;margin-bottom:4px;">DEPOIS</p>
<img src="{{ url_for('serve_upload', filename=item.after_path) }}" style="width:200px;border-radius:8px;">
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
<p style="text-align:center;color:#888;margin-top:24px;">Nenhum item no portfolio ainda.</p>
{% endif %}
{% endblock %}"""
with open(os.path.join(tpl, 'portfolio.html'), 'w', encoding='utf-8') as f:
    f.write(portfolio_html.strip() + '\n')
print('OK: portfolio.html (links de entrega)')

# ===== 3. GALERIA.HTML (com nota de entrega + link do cliente) =====
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
As fotos ficam armazenadas <strong>sem marca dagua</strong>. O cliente ve as fotos <strong>com marca dagua automaticamente</strong>.
Quando o cliente seleciona e envia, voce recebe as fotos <strong>originais (sem marca)</strong> no download ZIP e por e-mail.
</p>
<div style="background:#fff;padding:10px;border-radius:8px;margin-top:8px;">
<p style="font-size:13px;margin:0 0 4px 0;"><strong>LINK DO CLIENTE:</strong></p>
<p style="font-size:14px;word-break:break-all;margin:0;color:#4a90d9;">http://localhost:5000/g/{{ galeria.share_token }}</p>
<p style="font-size:11px;color:#666;margin:6px 0 0 0;">Envie este link para o cliente selecionar as fotos</p>
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
<td><a href="{{ url_for('download_selection', sid=s.id) }}" class="btn-primary" style="padding:4px 10px;font-size:12px;">Baixar ZIP (sem marca)</a></td>
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
<p style="color:#888;text-align:center;">Nenhuma foto enviada ainda.</p>
{% endif %}
</div>
{% endblock %}"""
with open(os.path.join(tpl, 'galeria.html'), 'w', encoding='utf-8') as f:
    f.write(galeria_html.strip() + '\n')
print('OK: galeria.html (nota de entrega + link do cliente)')

print('\nCorrecoes aplicadas!')