import os

base = os.path.dirname(os.path.abspath(__file__))
tpl = os.path.join(base, 'templates')
app_path = os.path.join(base, 'app.py')

with open(app_path, 'r', encoding='utf-8') as f:
    code = f.read()
patches = 0

# 1. Extend serve_wm to handle portfolio photos
if 'def serve_wm' in code and 'PortfolioPhoto.query.filter_by(before_path' not in code:
    start = code.find("@app.route('/wm/<filename>')")
    if start >= 0:
        next_route = code.find("\n@app.route", start + 10)
        if next_route < 0:
            next_route = code.find("\nif __name__", start)
        if next_route < 0:
            next_route = len(code)
        new_wm = """@app.route('/wm/<filename>')
def serve_wm(filename):
    user_id = None
    photo = Photo.query.filter_by(filepath=filename).first()
    if photo:
        galeria = Galeria.query.get(photo.galeria_id)
        if galeria:
            user_id = galeria.user_id
    if not user_id:
        try:
            pp = PortfolioPhoto.query.filter_by(before_path=filename).first()
            if not pp:
                pp = PortfolioPhoto.query.filter_by(after_path=filename).first()
            if pp:
                user_id = getattr(pp, 'user_id', None)
        except:
            pass
    if user_id:
        wm = Watermark.query.filter_by(user_id=user_id).first()
        if wm:
            fp = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.exists(fp):
                try:
                    img_bytes = get_watermarked_bytes(fp, wm.text or 'MeuFotoApp', wm.color or '#ffffff', wm.opacity or 30, wm.position or 'diagonal', wm.stroke, wm.logo_path)
                    return send_file(img_bytes, mimetype='image/jpeg')
                except Exception as e:
                    print('WM error: ' + str(e))
    return send_file(os.path.join(UPLOAD_FOLDER, filename))

"""
        code = code[:start] + new_wm + code[next_route:]
        patches += 1
        print('  OK: serve_wm extended for portfolio')
    else:
        print('  SKIP: serve_wm route not found')
else:
    print('  SKIP: serve_wm already extended or not found')

# 2. Add /p/<int:iid> route for public portfolio
if 'def public_portfolio_item' not in code:
    pp_route = """
@app.route('/p/<int:iid>')
def public_portfolio_item(iid):
    item = PortfolioPhoto.query.get_or_404(iid)
    return render_template('public_portfolio.html', item=item)

"""
    if 'if __name__ ==' in code:
        code = code.replace('if __name__ ==', pp_route + 'if __name__ ==')
        patches += 1
        print('  OK: /p/<int:iid> route added')
    else:
        code += pp_route
        patches += 1
        print('  OK: /p/<int:iid> route appended')
else:
    print('  SKIP: /p/<int:iid> already exists')

# 3. Fix galeria route
if 'def galeria(' in code:
    if 'photos=Photo.query' not in code or 'selections=Selection.query' not in code:
        start = code.find("@app.route('/galeria/<int:gid>')")
        if start >= 0:
            next_route = code.find("\n@app.route", start + 10)
            if next_route < 0:
                next_route = code.find("\nif __name__", start)
            if next_route < 0:
                next_route = len(code)
            new_route = """@app.route('/galeria/<int:gid>')
@login_required
def galeria(gid):
    g = Galeria.query.get_or_404(gid)
    if g.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    photos = Photo.query.filter_by(galeria_id=gid).all()
    selections = Selection.query.filter_by(galeria_id=gid).all()
    return render_template('galeria.html', galeria=g, photos=photos, selections=selections)

"""
            code = code[:start] + new_route + code[next_route:]
            patches += 1
            print('  OK: galeria route fixed')
        else:
            print('  SKIP: galeria route not found')
    else:
        print('  OK: galeria route already passes photos and selections')
else:
    galeria_route = """
@app.route('/galeria/<int:gid>')
@login_required
def galeria(gid):
    g = Galeria.query.get_or_404(gid)
    if g.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    photos = Photo.query.filter_by(galeria_id=gid).all()
    selections = Selection.query.filter_by(galeria_id=gid).all()
    return render_template('galeria.html', galeria=g, photos=photos, selections=selections)

"""
    if 'if __name__ ==' in code:
        code = code.replace('if __name__ ==', galeria_route + 'if __name__ ==')
        patches += 1
        print('  OK: galeria route added')
    else:
        code += galeria_route
        patches += 1
        print('  OK: galeria route appended')

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(code)
print(f'app.py: {patches} patches applied')

# 4. Rewrite base.html (safety)
base_html = """<!DOCTYPE html>
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
    f.write(base_html.strip() + '\n')
print('OK: base.html')

# 5. Rewrite portfolio.html (clickable links + watermark)
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
<a href="http://localhost:5000/p/{{ item.id }}" style="font-size:14px;color:#4a90d9;word-break:break-all;display:inline-block;">http://localhost:5000/p/{{ item.id }}</a>
<p style="font-size:11px;color:#666;margin:6px 0 0 0;">Clique no link para visualizar o antes e depois com marca d'agua</p>
</div>
{% endif %}
<div style="display:flex;gap:8px;flex-wrap:wrap;">
{% if item.before_path %}
<div>
<p style="font-size:12px;color:#888;margin-bottom:4px;">ANTES</p>
<img src="{{ url_for('serve_wm', filename=item.before_path) }}" style="width:200px;border-radius:8px;">
</div>
{% endif %}
{% if item.after_path %}
<div>
<p style="font-size:12px;color:#888;margin-bottom:4px;">DEPOIS</p>
<img src="{{ url_for('serve_wm', filename=item.after_path) }}" style="width:200px;border-radius:8px;">
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
print('OK: portfolio.html (links clicaveis + watermark)')

# 6. Add public_portfolio.html template
public_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ item.title }} - Portfolio</title>
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
<div style="max-width:800px;margin:0 auto;padding:28px;">
<div class="page-header">
<h1>{{ item.title }}</h1>
<p>Antes e depois</p>
</div>
<div class="card">
<div style="display:flex;gap:16px;flex-wrap:wrap;">
{% if item.before_path %}
<div>
<p style="font-size:14px;color:#888;margin-bottom:6px;"><strong>ANTES</strong></p>
<img src="{{ url_for('serve_wm', filename=item.before_path) }}" style="width:350px;border-radius:8px;">
</div>
{% endif %}
{% if item.after_path %}
<div>
<p style="font-size:14px;color:#888;margin-bottom:6px;"><strong>DEPOIS</strong></p>
<img src="{{ url_for('serve_wm', filename=item.after_path) }}" style="width:350px;border-radius:8px;">
</div>
{% endif %}
</div>
</div>
<p style="text-align:center;color:#999;font-size:13px;margin-top:20px;">Fotos protegidas com marca d'agua</p>
</div>
</body>
</html>"""
with open(os.path.join(tpl, 'public_portfolio.html'), 'w', encoding='utf-8') as f:
    f.write(public_html.strip() + '\n')
print('OK: public_portfolio.html (pagina publica)')

# 7. Rewrite galeria.html (with delivery note + client link)
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
<a href="http://localhost:5000/g/{{ galeria.share_token }}" style="font-size:14px;color:#4a90d9;word-break:break-all;">http://localhost:5000/g/{{ galeria.share_token }}</a>
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
print('OK: galeria.html (nota de entrega + link clicavel)')

print('\n=== CORRECOES APLICADAS! ===')