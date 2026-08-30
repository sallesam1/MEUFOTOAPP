import os
base = os.path.dirname(os.path.abspath(__file__))
tpl = os.path.join(base, 'templates')
os.makedirs(tpl, exist_ok=True)
files = {}

files['dashboard.html'] = '''{% extends 'base.html' %}
{% block title %}Dashboard — {{ site_settings.app_name if site_settings else 'MeuFotoApp' }}{% endblock %}
{% block content %}
<div class="page-header">
  <h1>Dashboard</h1>
  <p>Bem-vindo, {{ current_user.name or current_user.studio_name or current_user.email }}!</p>
</div>
{% if trial_days_left is defined and trial_days_left is not none and trial_days_left > 0 and not current_user.is_admin %}
<div class="card" style="background:#fff3cd; border:1px solid #ffeaa7;">
  <p style="margin:0;">Trial: <strong>{{ trial_days_left }} dia(s)</strong> restante(s). <a href="{{ url_for('planos') }}">Fazer upgrade</a></p>
</div>
{% endif %}
<div class="stats-grid">
  <div class="stat-card"><h3>{{ galerias|length }}</h3><p>Galerias Recentes</p></div>
  <div class="stat-card"><h3>{{ total_fotos }}</h3><p>Fotos</p></div>
  <div class="stat-card"><h3>{{ total_selecoes }}</h3><p>Selecoes</p></div>
  <div class="stat-card"><h3>{{ current_user.plan|upper }}</h3><p>Plano</p></div>
</div>
<div class="card">
  <h3>Galerias Recentes</h3>
  {% if galerias %}
  <table>
    <tr><th>Titulo</th><th>Cliente</th><th>Criada em</th><th>Acoes</th></tr>
    {% for g in galerias %}
    <tr>
      <td>{{ g.title }}</td>
      <td>{{ g.client_name or '-' }}</td>
      <td>{{ g.created_at.strftime('%d/%m/%Y') }}</td>
      <td><a href="{{ url_for('galeria', gid=g.id) }}" class="btn-primary" style="padding:4px 10px; font-size:12px;">Abrir</a></td>
    </tr>
    {% endfor %}
  </table>
  {% else %}
  <p style="color:#888;">Nenhuma galeria ainda. <a href="{{ url_for('nova_galeria') }}">Criar primeira galeria</a></p>
  {% endif %}
</div>
{% endblock %}
'''

files['list_galerias.html'] = '''{% extends 'base.html' %}
{% block title %}Galerias — {{ site_settings.app_name if site_settings else 'MeuFotoApp' }}{% endblock %}
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
        <a href="{{ url_for('galeria', gid=g.id) }}" class="btn-primary" style="padding:4px 10px; font-size:12px;">Abrir</a>
        <form method="POST" action="{{ url_for('delete_galeria', gid=g.id) }}" style="display:inline;">
          <button type="submit" class="btn-danger" onclick="return confirm('Excluir?')">Excluir</button>
        </form>
      </td>
    </tr>
    {% endfor %}
  </table>
  {% else %}
  <p style="color:#888; text-align:center;">Nenhuma galeria. <a href="{{ url_for('nova_galeria') }}">Criar agora</a></p>
  {% endif %}
</div>
{% endblock %}
'''

files['nova_galeria.html'] = '''{% extends 'base.html' %}
{% block title %}Nova Galeria — {{ site_settings.app_name if site_settings else 'MeuFotoApp' }}{% endblock %}
{% block content %}
<div class="page-header">
  <h1>Nova Galeria</h1>
  <p>Crie uma nova galeria para seu cliente</p>
</div>
<div class="card">
  <form method="POST">
    <label>Titulo da galeria</label>
    <input type="text" name="title" placeholder="Ex: Casamento Joao e Maria" required>
    <label>Nome do cliente</label>
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
    <label>Mensagem para o cliente</label>
    <textarea name="client_message" rows="3" placeholder="Opcional"></textarea>
    <button type="submit" class="btn-primary">Criar Galeria</button>
  </form>
</div>
{% endblock %}
'''

files['galeria.html'] = '''{% extends 'base.html' %}
{% block title %}{{ galeria.title }} — {{ site_settings.app_name if site_settings else 'MeuFotoApp' }}{% endblock %}
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
  <p style="word-break:break-all; background:#f8f9fa; padding:10px; border-radius:8px;">
    http://localhost:5000/g/{{ galeria.share_token }}
  </p>
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
      <td><a href="{{ url_for('download_selection', sid=s.id) }}" class="btn-primary" style="padding:4px 10px; font-size:12px;">ZIP</a></td>
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
    <div style="position:relative; border-radius:8px; overflow:hidden;">
      <img src="{{ url_for('serve_upload', filename=p.filepath) }}" style="width:100%; border-radius:8px;">
      <div style="display:flex; gap:4px; margin-top:4px; flex-wrap:wrap;">
        <a href="{{ url_for('resize_photo', gid=galeria.id, pid=p.id, platform='instagram_feed') }}" class="btn-primary" style="padding:3px 6px; font-size:11px;">IG</a>
        <form method="POST" action="{{ url_for('enhance_photo', gid=galeria.id, pid=p.id) }}" style="display:inline;">
          <button type="submit" class="btn-primary" style="padding:3px 6px; font-size:11px;">Melhorar</button>
        </form>
        <form method="POST" action="{{ url_for('rewatermark', gid=galeria.id, pid=p.id) }}" style="display:inline;">
          <button type="submit" class="btn-primary" style="padding:3px 6px; font-size:11px;">Marca</button>
        </form>
        <form method="POST" action="{{ url_for('delete_photo', gid=galeria.id, pid=p.id) }}" style="display:inline;">
          <button type="submit" class="btn-danger" style="padding:3px 6px; font-size:11px;">Excluir</button>
        </form>
      </div>
    </div>
    {% endfor %}
  </div>
  {% else %}
  <p style="color:#888; text-align:center;">Nenhuma foto enviada ainda.</p>
  {% endif %}
</div>
{% endblock %}
'''

files['cliente.html'] = '''{% extends 'base.html' %}
{% block title %}{{ galeria.title }} — Selecao de Fotos{% endblock %}
{% block content %}
<div class="auth-wrapper" style="background:linear-gradient(135deg,#1e272e,#2d3436); min-height:100vh; padding:20px;">
<div style="max-width:900px; margin:0 auto;">
<div class="page-header" style="color:#fff;">
  <h1>{{ galeria.title }}</h1>
  <p>Ola{{ ', ' + galeria.client_name if galeria.client_name else '' }}! Selecione suas fotos favoritas.</p>
</div>
{% with messages = get_flashed_messages(with_categories=true) %}
{% if messages %}
{% for category, message in messages %}
<div class="flash {{ category }}">{{ message }}</div>
{% endfor %}
{% endif %}
{% endwith %}
{% if submitted %}
<div class="card" style="text-align:center; padding:40px;">
  <h2>Selecao enviada!</h2>
  <p>Obrigado{{ ', ' + galeria.client_name if galeria.client_name else '' }}. O fotografo recebera sua escolha.</p>
</div>
{% else %}
<form method="POST">
  {% if packages %}
  <div class="card" style="margin-bottom:16px;">
    <label><strong>Escolha seu pacote:</strong></label>
    <select name="package_key" style="padding:8px;">
      {% for p in packages %}
      <option value="{{ p.key }}">{{ p.label }} - {{ p.limit }} fotos - {{ p.price }}</option>
      {% endfor %}
    </select>
  </div>
  {% endif %}
  <div class="grid">
    {% for p in photos %}
    <div style="position:relative; border-radius:8px; overflow:hidden; background:#fff;">
      <label style="display:block; cursor:pointer; position:relative;">
        <img src="{{ url_for('serve_upload', filename=p.filepath) }}" style="width:100%; border-radius:8px;">
        <input type="checkbox" name="selected_photos" value="{{ p.id }}" style="position:absolute; top:8px; right:8px; width:24px; height:24px;">
      </label>
    </div>
    {% endfor %}
  </div>
  {% if photos %}
  <div style="text-align:center; margin-top:20px;">
    <button type="submit" class="btn-primary" style="padding:14px 40px; font-size:16px;">Enviar Selecao</button>
  </div>
  {% else %}
  <div class="card" style="text-align:center;">
    <p style="color:#888;">Nenhuma foto disponivel ainda.</p>
  </div>
  {% endif %}
</form>
{% endif %}
</div>
</div>
{% endblock %}
'''

files['selecoes.html'] = '''{% extends 'base.html' %}
{% block title %}Selecoes — {{ site_settings.app_name if site_settings else 'MeuFotoApp' }}{% endblock %}
{% block content %}
<div class="page-header">
  <h1>Selecoes</h1>
  <p>Selecoes recebidas dos seus clientes</p>
</div>
{% if selections %}
<div class="card">
  <table>
    <tr><th>Galeria</th><th>Cliente</th><th>Data</th><th>Pacote</th><th>Status</th><th>Download</th></tr>
    {% for s in selections %}
    {% set g = s.galeria_id %}
    <tr>
      <td>{{ s.galeria_id }}</td>
      <td>-</td>
      <td>{{ s.created_at.strftime('%d/%m/%Y %H:%M') }}</td>
      <td>{{ s.package_key or '-' }}</td>
      <td>{{ s.status }}</td>
      <td><a href="{{ url_for('download_selection', sid=s.id) }}" class="btn-primary" style="padding:4px 10px; font-size:12px;">Baixar ZIP</a></td>
    </tr>
    {% endfor %}
  </table>
</div>
{% else %}
<div class="card" style="text-align:center;">
  <p style="color:#888;">Nenhuma selecao recebida ainda.</p>
</div>
{% endif %}
{% endblock %}
'''

for name, content in files.items():
    with open(os.path.join(tpl, name), 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f'OK: {name}')

print('\nTemplates restantes atualizados com sucesso!')