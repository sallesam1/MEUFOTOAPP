import os
tpl = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

content = """<!DOCTYPE html>
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
</body>
</html>"""

with open(os.path.join(tpl, 'base.html'), 'w', encoding='utf-8') as f:
    f.write(content.strip() + '\n')

print('OK: base.html corrigido!')