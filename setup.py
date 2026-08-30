import os

base = os.path.dirname(os.path.abspath(__file__))

files = {}

files['static/css/style.css'] = """
*{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI',sans-serif}
body{background:#0f1117;color:#e0e0e0}
.sidebar{position:fixed;left:0;top:0;width:220px;height:100vh;background:#1a1d27;padding:20px 0;display:flex;flex-direction:column}
.sidebar-logo h2{font-size:18px;padding:0 20px 20px;color:#fff}
.sidebar-nav{flex:1;list-style:none}
.sidebar-nav li a{display:block;padding:12px 20px;color:#8b8d93;text-decoration:none;font-size:14px;transition:.2s}
.sidebar-nav li a:hover{color:#fff;background:#262932}
.sidebar-nav li a.active{color:#fff;background:#2d6cdf;border-left:3px solid #4a90d9}
.sidebar-footer{padding:20px}
.btn-logout{display:block;padding:10px;text-align:center;background:#e74c3c;color:#fff;text-decoration:none;border-radius:6px;font-size:13px}
.main-content{margin-left:220px;padding:30px;min-height:100vh}
.auth-main{display:flex;justify-content:center;align-items:center;min-height:100vh}
.auth-card{background:#1a1d27;padding:40px;border-radius:12px;width:400px;max-width:90%}
.auth-header{text-align:center;margin-bottom:30px}
.auth-header h1{font-size:28px;color:#fff;margin-bottom:8px}
.auth-header p{color:#8b8d93;font-size:14px}
.auth-form .form-group{margin-bottom:20px}
.auth-form label{display:block;margin-bottom:6px;font-size:13px;color:#8b8d93}
.auth-form input{width:100%;padding:12px;background:#0f1117;border:1px solid #2d3142;color:#fff;border-radius:6px;font-size:14px}
.auth-form input:focus{outline:none;border-color:#4a90d9}
.btn-primary{width:100%;padding:12px;background:#4a90d9;color:#fff;border:none;border-radius:6px;font-size:14px;cursor:pointer}
.btn-primary:hover{background:#3a7bc8}
.auth-footer{text-align:center;margin-top:20px}
.auth-footer a{color:#4a90d9;text-decoration:none;font-size:13px}
.auth-footer p{color:#8b8d93;font-size:13px}
.card{background:#1a1d27;border-radius:10px;padding:24px;margin-bottom:20px}
.stats-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-bottom:30px}
.stat-card{background:#1a1d27;padding:24px;border-radius:10px;text-align:center}
.stat-value{font-size:32px;font-weight:700;color:#4a90d9}
.stat-label{color:#8b8d93;font-size:13px;margin-top:4px}
.btn{display:inline-block;padding:10px 20px;background:#4a90d9;color:#fff;text-decoration:none;border-radius:6px;font-size:13px;border:none;cursor:pointer}
.btn:hover{background:#3a7bc8}
.btn-danger{background:#e74c3c}
.btn-danger:hover{background:#c0392b}
.btn-success{background:#27ae60}
table{width:100%;border-collapse:collapse}
th,td{padding:12px;text-align:left;border-bottom:1px solid #2d3142}
th{color:#8b8d93;font-size:13px;text-transform:uppercase}
td{color:#e0e0e0;font-size:14px}
.photo-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}
.photo-item{position:relative;border-radius:8px;overflow:hidden}
.photo-item img{width:100%;height:150px;object-fit:cover}
.alert{padding:12px 16px;border-radius:6px;margin-bottom:16px;font-size:14px}
.alert-success{background:#1a3a2a;color:#27ae60;border:1px solid #2d5a3d}
.alert-error{background:#3a1a1a;color:#e74c3c;border:1px solid #5a2d2d}
.form-group{margin-bottom:16px}
.form-group label{display:block;margin-bottom:6px;font-size:13px;color:#8b8d93}
.form-group input,.form-group select,.form-group textarea{width:100%;padding:10px;background:#0f1117;border:1px solid #2d3142;color:#fff;border-radius:6px;font-size:14px}
.form-group input:focus,.form-group select:focus,.form-group textarea:focus{outline:none;border-color:#4a90d9}
h1{font-size:24px;margin-bottom:20px;color:#fff}
h2,h3{color:#fff}
a{color:#4a90d9}
.share-url{background:#0f1117;padding:12px;border-radius:6px;color:#4a90d9;font-size:13px;word-break:break-all;margin:10px 0}
.pricing-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.pricing-card{background:#1a1d27;border-radius:12px;padding:30px;text-align:center}
.pricing-card h3{font-size:20px;margin-bottom:8px}
.pricing-card .price{font-size:36px;font-weight:700;color:#4a90d9;margin:16px 0}
.pricing-card ul{list-style:none;text-align:left;margin:20px 0}
.pricing-card ul li{padding:8px 0;color:#8b8d93;font-size:14px;border-bottom:1px solid #2d3142}
"""

files['templates/base.html'] = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}MeuFotoApp{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
{% if current_user.is_authenticated %}
<nav class="sidebar">
    <div class="sidebar-logo"><h2>MeuFotoApp</h2></div>
    <ul class="sidebar-nav">
        <li><a href="{{ url_for('dashboard') }}" class="{% if request.endpoint == 'dashboard' %}active{% endif %}">Dashboard</a></li>
        <li><a href="{{ url_for('list_galerias') }}" class="{% if request.endpoint == 'list_galerias' %}active{% endif %}">Galerias</a></li>
        <li><a href="{{ url_for('selecoes') }}" class="{% if request.endpoint == 'selecoes' %}active{% endif %}">Selecoes</a></li>
        <li><a href="{{ url_for('portfolio') }}" class="{% if request.endpoint == 'portfolio' %}active{% endif %}">Portfolio</a></li>
        <li><a href="{{ url_for('catalogo_poses') }}" class="{% if request.endpoint == 'catalogo_poses' %}active{% endif %}">Catalogo de Poses</a></li>
        <li><a href="{{ url_for('marca') }}" class="{% if request.endpoint == 'marca' %}active{% endif %}">Marca Dagua</a></li>
        <li><a href="{{ url_for('planos') }}" class="{% if request.endpoint == 'planos' %}active{% endif %}">Planos</a></li>
        <li><a href="{{ url_for('configuracoes') }}" class="{% if request.endpoint == 'configuracoes' %}active{% endif %}">Configuracoes</a></li>
        {% if current_user.is_admin %}
        <li><a href="{{ url_for('admin') }}" class="{% if request.endpoint == 'admin' %}active{% endif %}">Admin</a></li>
        {% endif %}
    </ul>
    <div class="sidebar-footer"><a href="{{ url_for('logout') }}" class="btn-logout">Sair</a></div>
</nav>
<main class="main-content">
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}{% for category, message in messages %}
            <div class="alert alert-{{ category }}">{{ message }}</div>
        {% endfor %}{% endif %}
    {% endwith %}
    {% block content %}{% endblock %}
</main>
{% else %}
<main class="auth-main">
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}{% for category, message in messages %}
            <div class="alert alert-{{ category }}">{{ message }}</div>
        {% endfor %}{% endif %}
    {% endwith %}
    {% block auth_content %}{% endblock %}
</main>
{% endif %}
</body>
</html>
"""

files['templates/login.html'] = """{% extends "base.html" %}
{% block title %}Login - MeuFotoApp{% endblock %}
{% block auth_content %}
<div class="auth-card">
    <div class="auth-header">
        <h1>MeuFotoApp</h1>
        <p>Faca login para gerenciar suas galerias</p>
    </div>
    <form method="POST" class="auth-form">
        <div class="form-group">
            <label>E-mail</label>
            <input type="email" name="email" required placeholder="seu@email.com">
        </div>
        <div class="form-group">
            <label>Senha</label>
            <input type="password" name="password" required placeholder="********">
        </div>
        <button type="submit" class="btn-primary">Entrar</button>
    </form>
    <div class="auth-footer">
        <p>Nao tem conta? <a href="{{ url_for('registro') }}">Criar conta gratuita</a></p>
    </div>
</div>
{% endblock %}
"""

files['templates/registro.html'] = """{% extends "base.html" %}
{% block title %}Criar conta - MeuFotoApp{% endblock %}
{% block auth_content %}
<div class="auth-card">
    <div class="auth-header">
        <h1>MeuFotoApp</h1>
        <p>Crie sua conta gratuita</p>
    </div>
    <form method="POST" class="auth-form">
        <div class="form-group">
            <label>Nome do Estudio</label>
            <input type="text" name="studio_name" placeholder="Estudio Foto Arte">
        </div>
        <div class="form-group">
            <label>Seu nome</label>
            <input type="text" name="name" required placeholder="Joao Silva">
        </div>
        <div class="form-group">
            <label>E-mail</label>
            <input type="email" name="email" required placeholder="seu@email.com">
        </div>
        <div class="form-group">
            <label>Senha</label>
            <input type="password" name="password" required placeholder="********">
        </div>
        <button type="submit" class="btn-primary">Criar conta</button>
    </form>
    <div class="auth-footer">
        <p>Ja tem conta? <a href="{{ url_for('login') }}">Fazer login</a></p>
    </div>
</div>
{% endblock %}
"""

files['templates/dashboard.html'] = """{% extends "base.html" %}
{% block title %}Dashboard - MeuFotoApp{% endblock %}
{% block content %}
<h1>Dashboard</h1>
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-value">{{ galerias|length }}</div>
        <div class="stat-label">Galerias</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">{{ total_photos }}</div>
        <div class="stat-label">Fotos</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">{{ total_selections }}</div>
        <div class="stat-label">Selecoes</div>
    </div>
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
            <td>{{ g.created_at.strftime('%d/%m/%Y') if g.created_at else '-' }}</td>
            <td><a href="{{ url_for('view_galeria', galeria_id=g.id) }}" class="btn">Abrir</a></td>
        </tr>
        {% endfor %}
    </table>
    {% else %}
    <p>Nenhuma galeria ainda. <a href="{{ url_for('nova_galeria') }}">Criar primeira galeria</a></p>
    {% endif %}
</div>
<p><a href="{{ url_for('nova_galeria') }}" class="btn">+ Nova Galeria</a></p>
{% endblock %}
"""

files['templates/list_galerias.html'] = """{% extends "base.html" %}
{% block title %}Galerias - MeuFotoApp{% endblock %}
{% block content %}
<h1>Galerias</h1>
<p style="margin-bottom:20px"><a href="{{ url_for('nova_galeria') }}" class="btn">+ Nova Galeria</a></p>
{% if galerias %}
<div class="card">
    <table>
        <tr><th>Titulo</th><th>Cliente</th><th>Categoria</th><th>Criada em</th><th>Acoes</th></tr>
        {% for g in galerias %}
        <tr>
            <td>{{ g.title }}</td>
            <td>{{ g.client_name or '-' }}</td>
            <td>{{ g.category or '-' }}</td>
            <td>{{ g.created_at.strftime('%d/%m/%Y') if g.created_at else '-' }}</td>
            <td>
                <a href="{{ url_for('view_galeria', galeria_id=g.id) }}" class="btn">Abrir</a>
                <form method="POST" action="{{ url_for('delete_galeria', galeria_id=g.id) }}" style="display:inline" onsubmit="return confirm('Excluir esta galeria?')">
                    <button type="submit" class="btn btn-danger">Excluir</button>
                </form>
            </td>
        </tr>
        {% endfor %}
    </table>
</div>
{% else %}
<div class="card"><p>Nenhuma galeria criada ainda.</p></div>
{% endif %}
{% endblock %}
"""

files['templates/nova_galeria.html'] = """{% extends "base.html" %}
{% block title %}Nova Galeria - MeuFotoApp{% endblock %}
{% block content %}
<h1>Nova Galeria</h1>
<div class="card" style="max-width:600px">
    <form method="POST">
        <div class="form-group">
            <label>Titulo *</label>
            <input type="text" name="title" required placeholder="Casamento Joao e Maria">
        </div>
        <div class="form-group">
            <label>Nome do Cliente</label>
            <input type="text" name="client_name" placeholder="Joao Silva">
        </div>
        <div class="form-group">
            <label>E-mail do Cliente</label>
            <input type="email" name="client_email" placeholder="cliente@email.com">
        </div>
        <div class="form-group">
            <label>Categoria</label>
            <select name="category">
                <option value="">Selecione...</option>
                {% for c in categorias %}
                <option value="{{ c.slug }}">{{ c.label }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="form-group">
            <label>Data do Evento</label>
            <input type="date" name="event_date">
        </div>
        <div class="form-group">
            <label>Mensagem para o Cliente</label>
            <textarea name="client_message" rows="3" placeholder="Ola! Selecione suas fotos favoritas..."></textarea>
        </div>
        <button type="submit" class="btn">Criar Galeria</button>
    </form>
</div>
<p><a href="{{ url_for('list_galerias') }}">Voltar</a></p>
{% endblock %}
"""

files['templates/galeria.html'] = """{% extends "base.html" %}
{% block title %}{{ galeria.title }} - MeuFotoApp{% endblock %}
{% block content %}
<h1>{{ galeria.title }}</h1>
<div class="card">
    <h3>Detalhes</h3>
    <p><strong>Cliente:</strong> {{ galeria.client_name or '-' }}</p>
    <p><strong>Categoria:</strong> {{ galeria.category or '-' }}</p>
    <p><strong>Data:</strong> {{ galeria.event_date or '-' }}</p>
    {% if share_url %}
    <p><strong>Link de compartilhamento:</strong></p>
    <div class="share-url">{{ share_url }}</div>
    {% endif %}
</div>
<div class="card">
    <h3>Enviar Fotos</h3>
    <form method="POST" action="{{ url_for('upload_photo', galeria_id=galeria.id) }}" enctype="multipart/form-data">
        <div class="form-group">
            <label>Selecionar fotos</label>
            <input type="file" name="photos" multiple accept="image/*">
        </div>
        <button type="submit" class="btn">Enviar</button>
    </form>
</div>
<div class="card">
    <h3>Fotos ({{ photos|length }})</h3>
    {% if photos %}
    <div class="photo-grid">
        {% for p in photos %}
        <div class="photo-item">
            <img src="{{ url_for('serve_photo', photo_id=p.id) }}" alt="{{ p.filename or '' }}">
            <form method="POST" action="{{ url_for('delete_photo', photo_id=p.id) }}" style="display:inline" onsubmit="return confirm('Excluir esta foto?')">
                <button type="submit" class="btn btn-danger" style="width:100%;font-size:11px">Excluir</button>
            </form>
        </div>
        {% endfor %}
    </div>
    {% else %}
    <p>Nenhuma foto enviada ainda.</p>
    {% endif %}
</div>
<p><a href="{{ url_for('list_galerias') }}">Voltar</a></p>
{% endblock %}
"""

files['templates/cliente.html'] = """{% extends "base.html" %}
{% block title %}{{ galeria.title }}{% endblock %}
{% block auth_content %}
<div class="auth-card" style="width:90%;max-width:800px">
    <div class="auth-header">
        <h1>{{ galeria.title }}</h1>
        <p>Fotografo: {{ photographer.studio_name if photographer else 'MeuFotoApp' }}</p>
        {% if galeria.client_message %}
        <p style="margin-top:10px;color:#8b8d93">{{ galeria.client_message }}</p>
        {% endif %}
    </div>
    <form method="POST" action="{{ url_for('cliente_selecionar', token=galeria.share_token) }}" id="selForm">
        <input type="hidden" name="photo_ids" id="photo_ids">
        <div class="form-group">
            <label>Escolha um pacote:</label>
            <select name="package_key" id="package_key">
                {% for pkg in pacotes %}
                <option value="{{ pkg.key }}">{{ pkg.label }} - {{ pkg.price }} ({{ pkg.limit }} fotos)</option>
                {% endfor %}
            </select>
        </div>
        <div class="photo-grid">
            {% for p in photos %}
            <div class="photo-item" onclick="togglePhoto({{ p.id }}, this)" id="photo_{{ p.id }}" style="cursor:pointer">
                <img src="{{ url_for('serve_photo', photo_id=p.id) }}" alt="">
            </div>
            {% endfor %}
        </div>
        <p style="margin:10px 0;color:#8b8d93">Selecionadas: <span id="count">0</span></p>
        <button type="submit" class="btn-primary">Enviar Selecao</button>
    </form>
</div>
<script>
var selected = [];
function togglePhoto(id, el) {
    var idx = selected.indexOf(id);
    if (idx > -1) { selected.splice(idx, 1); el.style.border='none'; }
    else { selected.push(id); el.style.border='3px solid #4a90d9'; }
    document.getElementById('photo_ids').value = selected.join(',');
    document.getElementById('count').textContent = selected.length;
}
</script>
{% endblock %}
"""

files['templates/selecoes.html'] = """{% extends "base.html" %}
{% block title %}Selecoes - MeuFotoApp{% endblock %}
{% block content %}
<h1>Selecoes dos Clientes</h1>
{% if selecoes %}
{% for item in selecoes %}
<div class="card">
    <h3>{{ item.galeria.title }} - {{ item.selection.package_key }}</h3>
    <p><strong>Status:</strong> {{ item.selection.status }}</p>
    <p><strong>Data:</strong> {{ item.selection.created_at.strftime('%d/%m/%Y') if item.selection.created_at else '-' }}</p>
    <p><strong>Fotos selecionadas ({{ item.photos|length }}):</strong></p>
    <div class="photo-grid">
        {% for p in item.photos %}
        <div class="photo-item"><img src="{{ url_for('serve_photo', photo_id=p.id) }}" alt=""></div>
        {% endfor %}
    </div>
</div>
{% endfor %}
{% else %}
<div class="card"><p>Nenhuma selecao recebida ainda.</p></div>
{% endif %}
{% endblock %}
"""

files['templates/portfolio.html'] = """{% extends "base.html" %}
{% block title %}Portfolio - MeuFotoApp{% endblock %}
{% block content %}
<h1>Portfolio</h1>
<div class="card" style="max-width:600px">
    <h3>Adicionar Foto</h3>
    <form method="POST" action="{{ url_for('upload_portfolio') }}" enctype="multipart/form-data">
        <div class="form-group">
            <label>Foto</label>
            <input type="file" name="photo" accept="image/*" required>
        </div>
        <div class="form-group">
            <label>Titulo</label>
            <input type="text" name="title" placeholder="Casamento na praia">
        </div>
        <button type="submit" class="btn">Adicionar</button>
    </form>
</div>
<div class="card">
    <h3>Suas Fotos ({{ photos|length }})</h3>
    {% if photos %}
    <div class="photo-grid">
        {% for p in photos %}
        <div class="photo-item">
            <img src="{{ url_for('static', filename='uploads/' ~ p.filepath.split('/')[-1]) if false else p.filepath }}" alt="{{ p.title or '' }}" style="object-fit:cover;width:100%;height:150px">
            <form method="POST" action="{{ url_for('delete_portfolio', photo_id=p.id) }}" style="display:inline" onsubmit="return confirm('Remover?')">
                <button type="submit" class="btn btn-danger" style="width:100%;font-size:11px">Remover</button>
            </form>
        </div>
        {% endfor %}
    </div>
    {% else %}
    <p>Nenhuma foto no portfolio.</p>
    {% endif %}
</div>
{% endblock %}
"""

files['templates/catalogo_poses.html'] = """{% extends "base.html" %}
{% block title %}Catalogo de Poses - MeuFotoApp{% endblock %}
{% block content %}
<h1>Catalogo de Poses</h1>
<div class="card" style="max-width:600px">
    <h3>Adicionar Pose</h3>
    <form method="POST" action="{{ url_for('upload_pose') }}" enctype="multipart/form-data">
        <div class="form-group">
            <label>Foto</label>
            <input type="file" name="photo" accept="image/*" required>
        </div>
        <div class="form-group">
            <label>Categoria</label>
            <select name="category">
                {% for c in categorias %}
                <option value="{{ c.slug }}">{{ c.label }}</option>
                {% endfor %}
            </select>
        </div>
        <button type="submit" class="btn">Adicionar</button>
    </form>
</div>
<div class="card">
    <h3>Poses ({{ photos|length }})</h3>
    {% if photos %}
    <div class="photo-grid">
        {% for p in photos %}
        <div class="photo-item">
            <img src="{{ p.filepath }}" alt="{{ p.category or '' }}" style="object-fit:cover;width:100%;height:150px">
            <form method="POST" action="{{ url_for('delete_pose', photo_id=p.id) }}" style="display:inline" onsubmit="return confirm('Remover?')">
                <button type="submit" class="btn btn-danger" style="width:100%;font-size:11px">Remover</button>
            </form>
        </div>
        {% endfor %}
    </div>
    {% else %}
    <p>Nenhuma pose adicionada.</p>
    {% endif %}
</div>
{% endblock %}
"""

files['templates/marca.html'] = """{% extends "base.html" %}
{% block title %}Marca Dagua - MeuFotoApp{% endblock %}
{% block content %}
<h1>Marca Dagua</h1>
<div class="card" style="max-width:600px">
    <form method="POST" action="{{ url_for('salvar_marca') }}">
        <div class="form-group">
            <label>Texto da marca</label>
            <input type="text" name="text" value="{{ watermark.text if watermark else '' }}" placeholder="@seu_estudio">
        </div>
        <div class="form-group">
            <label>Cor</label>
            <input type="color" name="color" value="{{ watermark.color if watermark else '#ffffff' }}">
        </div>
        <div class="form-group">
            <label>Opacidade (0-100)</label>
            <input type="number" name="opacity" min="0" max="100" value="{{ watermark.opacity if watermark else 30 }}">
        </div>
        <button type="submit" class="btn">Salvar</button>
    </form>
</div>
{% endblock %}
"""

files['templates/planos.html'] = """{% extends "base.html" %}
{% block title %}Planos - MeuFotoApp{% endblock %}
{% block content %}
<h1>Planos</h1>
<div class="pricing-grid">
    {% for plano in planos %}
    <div class="pricing-card">
        <h3>{{ plano.label }}</h3>
        <p style="color:#8b8d93;font-size:14px">{{ plano.description }}</p>
        <div class="price">{{ plano.price }}<span style="font-size:14px;color:#8b8d93">{{ plano.period }}</span></div>
        <ul>
            {% for f in plano.features %}
            <li>{{ f }}</li>
            {% endfor %}
        </ul>
    </div>
    {% endfor %}
</div>
{% endblock %}
"""

files['templates/configuracoes.html'] = """{% extends "base.html" %}
{% block title %}Configuracoes - MeuFotoApp{% endblock %}
{% block content %}
<h1>Configuracoes</h1>
<div class="card" style="max-width:600px">
    <form method="POST" action="{{ url_for('salvar_configuracoes') }}">
        <div class="form-group">
            <label>Nome do Estudio</label>
            <input type="text" name="studio_name" value="{{ user.studio_name or '' }}">
        </div>
        <div class="form-group">
            <label>Seu Nome</label>
            <input type="text" name="name" value="{{ user.name or '' }}">
        </div>
        <div class="form-group">
            <label>E-mail</label>
            <input type="email" value="{{ user.email or '' }}" disabled>
        </div>
        <button type="submit" class="btn">Salvar</button>
    </form>
</div>
{% endblock %}
"""

files['templates/admin.html'] = """{% extends "base.html" %}
{% block title %}Admin - MeuFotoApp{% endblock %}
{% block content %}
<h1>Painel Admin</h1>
<div class="card">
    <h3>Usuarios ({{ users|length }})</h3>
    <table>
        <tr><th>ID</th><th>Nome</th><th>Email</th><th>Plano</th><th>Admin</th></tr>
        {% for u in users %}
        <tr>
            <td>{{ u.id }}</td>
            <td>{{ u.name or '-' }}</td>
            <td>{{ u.email }}</td>
            <td>{{ u.plan }}</td>
            <td>{{ 'Sim' if u.is_admin else 'Nao' }}</td>
        </tr>
        {% endfor %}
    </table>
</div>
{% endblock %}
"""

for rel_path, content in files.items():
    full_path = os.path.join(base, rel_path.replace('/', os.sep))
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f'OK: {rel_path}')

print('\nTodos os arquivos criados!')