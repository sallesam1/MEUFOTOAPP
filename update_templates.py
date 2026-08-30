import os
base = os.path.dirname(os.path.abspath(__file__))
tpl = os.path.join(base, 'templates')
os.makedirs(tpl, exist_ok=True)
files = {}

files['portfolio.html'] = '''{% extends 'base.html' %}
{% block content %}
<div class="page-header">
  <h1>📁 Portfólio</h1>
  <p>Mostre seu trabalho com fotos antes e depois</p>
</div>
{% if not public %}
<form method="POST" enctype="multipart/form-data" action="{{ url_for('portfolio') }}" class="card">
  <h3>Adicionar Item</h3>
  <input type="text" name="title" placeholder="Título do trabalho" required>
  <div style="display:flex; gap:16px; flex-wrap:wrap;">
    <div>
      <label> Foto Antes</label><br>
      <input type="file" name="before" accept="image/*">
    </div>
    <div>
      <label> Foto Depois</label><br>
      <input type="file" name="after" accept="image/*">
    </div>
  </div>
  <br><button type="submit" class="btn-primary">Adicionar</button>
</form>
{% endif %}
<div class="grid">
  {% for item in items %}
  <div class="card">
    <h3>{{ item.title }}</h3>
    <div style="display:flex; gap:8px; flex-wrap:wrap;">
      {% if item.before_path %}
      <div>
        <p style="font-size:12px; color:#888;">ANTES</p>
        <img src="{{ url_for('serve_upload', filename=item.before_path) }}" style="width:200px; border-radius:8px;">
      </div>
      {% endif %}
      {% if item.after_path %}
      <div>
        <p style="font-size:12px; color:#888;">DEPOIS</p>
        <img src="{{ url_for('serve_upload', filename=item.after_path) }}" style="width:200px; border-radius:8px;">
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
<p style="text-align:center; color:#888; margin-top:24px;">Nenhum item no portfólio ainda.</p>
{% endif %}
{% endblock %}
'''

files['catalogo_poses.html'] = '''{% extends 'base.html' %}
{% block content %}
<div class="page-header">
  <h1>📸 Catálogo de Poses</h1>
  <p>Inspirações e referências para seus clientes</p>
</div>
{% if not public %}
<form method="POST" enctype="multipart/form-data" action="{{ url_for('catalogo_poses') }}" class="card">
  <h3>Adicionar Pose</h3>
  <input type="file" name="photo" accept="image/*" required><br><br>
  {% if categories is defined %}
  <select name="category">
    <option value="">Sem categoria</option>
    {% for c in categories %}
    <option value="{{ c.slug }}">{{ c.label }}</option>
    {% endfor %}
  </select>
  {% endif %}
  <br><br>
  <input type="text" name="group_name" placeholder="Grupo (ex: Casamento 1)"><br><br>
  <textarea name="prompt_text" placeholder="Prompt ou descrição da pose" rows="3" style="width:100%;"></textarea><br><br>
  <button type="submit" class="btn-primary">Adicionar</button>
</form>
{% endif %}
<div class="grid">
  {% for pose in poses %}
  <div class="card">
    <img src="{{ url_for('serve_upload', filename=pose.filepath) }}" style="width:100%; border-radius:8px;">
    {% if pose.group_name %}<p><strong>{{ pose.group_name }}</strong></p>{% endif %}
    {% if pose.prompt_text %}<p style="font-size:14px; color:#666;">{{ pose.prompt_text }}</p>{% endif %}
    {% if not public %}
    <form method="POST" action="{{ url_for('delete_pose', pid=pose.id) }}" style="margin-top:8px;">
      <button type="submit" class="btn-danger">Excluir</button>
    </form>
    {% endif %}
  </div>
  {% endfor %}
</div>
{% if not poses %}
<p style="text-align:center; color:#888; margin-top:24px;">Nenhuma pose cadastrada ainda.</p>
{% endif %}
{% endblock %}
'''

files['marca.html'] = '''{% extends 'base.html' %}
{% block content %}
<div class="page-header">
  <h1>💧 Marca d'Água</h1>
  <p>Configure a marca d'água aplicada nas suas fotos</p>
</div>
<form method="POST" enctype="multipart/form-data" action="{{ url_for('marca') }}" class="card">
  <div style="margin-bottom:16px;">
    <label><strong>Texto da marca d'água:</strong></label><br>
    <input type="text" name="text" value="{{ wm.text if wm else '' }}" placeholder="Seu nome ou estúdio" style="width:100%; padding:8px;">
  </div>
  <div style="margin-bottom:16px;">
    <label><strong>Cor:</strong></label><br>
    <input type="color" name="color" value="{{ wm.color if wm else '#ffffff' }}">
  </div>
  <div style="margin-bottom:16px;">
    <label><strong>Opacidade (%):</strong></label><br>
    <input type="number" name="opacity" value="{{ wm.opacity if wm else 30 }}" min="0" max="100" style="padding:8px;">
  </div>
  <div style="margin-bottom:16px;">
    <label><strong>Posição:</strong></label><br>
    <select name="position" style="padding:8px;">
      <option value="diagonal" {{ 'selected' if wm and wm.position == 'diagonal' else '' }}>Diagonal (repetida)</option>
      <option value="center" {{ 'selected' if wm and wm.position == 'center' else '' }}>Centro</option>
    </select>
  </div>
  <div style="margin-bottom:16px;">
    <label><strong>Contorno (borda escura nas letras):</strong></label><br>
    <input type="checkbox" name="stroke" {{ 'checked' if wm and wm.stroke else '' }}>
  </div>
  <div style="margin-bottom:16px;">
    <label><strong>Logo (opcional):</strong></label><br>
    <input type="file" name="logo" accept="image/*">
  </div>
  <button type="submit" class="btn-primary">Salvar Configurações</button>
</form>
{% endblock %}
'''

files['configuracoes.html'] = '''{% extends 'base.html' %}
{% block content %}
<div class="page-header">
  <h1>⚙️ Configurações</h1>
  <p>Gerencie as configurações da sua conta</p>
</div>
<div class="card">
  <h3>Informações da Conta</h3>
  <p><strong>Estúdio:</strong> {{ current_user.studio_name or 'Não definido' }}</p>
  <p><strong>Nome:</strong> {{ current_user.name or 'Não definido' }}</p>
  <p><strong>E-mail:</strong> {{ current_user.email }}</p>
  <p><strong>Plano:</strong> {{ current_user.plan or 'free' }}</p>
</div>
<div class="card">
  <h3>Configurações do App</h3>
  {% if site_settings %}
  <p><strong>Nome do App:</strong> {{ site_settings.app_name }}</p>
  <p><strong>Cor principal:</strong> {{ site_settings.primary_color }}</p>
  {% if site_settings.smtp_host %}
  <p><strong>SMTP:</strong> {{ site_settings.smtp_host }}:{{ site_settings.smtp_port }}</p>
  {% else %}
  <p><strong>SMTP:</strong> Não configurado</p>
  {% endif %}
  {% else %}
  <p>Nenhuma configuração definida.</p>
  {% endif %}
</div>
{% endblock %}
'''

for name, content in files.items():
    with open(os.path.join(tpl, name), 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f'OK: {name}')

print('\nTemplates atualizados com sucesso!')