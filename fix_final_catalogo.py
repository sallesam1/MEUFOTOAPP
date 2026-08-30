import os, shutil

base_dir = os.path.dirname(os.path.abspath(__file__))

# ===== 1. LIMPAR CACHE DO FLASK/JINJA2 =====
for pasta in ['__pycache__', 'templates/__pycache__']:
    p = os.path.join(base_dir, pasta)
    if os.path.exists(p):
        shutil.rmtree(p)
        print(f'OK: cache removido - {pasta}')
    else:
        print(f'OK: sem cache - {pasta}')

# ===== 2. REESCREVER catalogo_categoria.html COM object-fit:contain =====
cat_cat = os.path.join(base_dir, 'templates', 'catalogo_categoria.html')
with open(cat_cat, 'w', encoding='utf-8') as f:
    f.write(r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ category }} - Catalogo</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Segoe UI',Arial,sans-serif; background:#f0f2f5; color:#333; }
.sidebar { position:fixed; left:0; top:0; width:220px; height:100vh; background:#1a1a2e; padding:20px 0; overflow-y:auto; z-index:100; }
.sidebar .logo { color:#fff; font-size:18px; font-weight:700; padding:0 20px 24px; border-bottom:1px solid rgba(255,255,255,0.1); }
.sidebar a { display:block; color:#aab; text-decoration:none; padding:12px 20px; font-size:13px; transition:0.2s; }
.sidebar a:hover { background:rgba(255,255,255,0.05); color:#fff; }
.sidebar a.active { background:rgba(77,166,255,0.15); color:#4da6ff; border-left:3px solid #4da6ff; }
.main { margin-left:220px; padding:24px; }
.page-header { display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:20px; flex-wrap:wrap; gap:12px; }
.page-header h1 { font-size:24px; font-weight:700; }
.page-header a.back { color:#4da6ff; text-decoration:none; font-size:13px; }
.info-badge { background:#e8f4fd; color:#1976d2; padding:4px 12px; border-radius:12px; font-size:12px; font-weight:600; }
.add-form { background:#fff; border-radius:12px; padding:24px; box-shadow:0 2px 10px rgba(0,0,0,0.06); margin-bottom:28px; }
.add-form h2 { font-size:16px; margin-bottom:16px; color:#333; }
.form-row { display:flex; gap:16px; flex-wrap:wrap; align-items:flex-start; }
.form-group { flex:1; min-width:200px; }
.form-group label { display:block; font-size:12px; font-weight:600; color:#555; margin-bottom:6px; }
.form-group input[type="file"] { width:100%; padding:8px; border:1px solid #ddd; border-radius:8px; font-size:12px; }
.form-group textarea { width:100%; min-height:80px; padding:10px; border:1px solid #ddd; border-radius:8px; font-size:13px; font-family:monospace; resize:vertical; }
.btn-add { background:#27ae60; color:#fff; border:none; padding:10px 24px; border-radius:8px; font-size:14px; font-weight:600; cursor:pointer; align-self:flex-end; }
.btn-add:hover { background:#219a52; }
.preview-img { max-width:160px; max-height:160px; border-radius:8px; margin-top:8px; display:none; object-fit:contain; }
.poses-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:20px; }
.pose-card { background:#fff; border-radius:12px; overflow:hidden; box-shadow:0 2px 10px rgba(0,0,0,0.06); transition:box-shadow 0.2s; display:flex; flex-direction:column; }
.pose-card:hover { box-shadow:0 4px 16px rgba(0,0,0,0.1); }
.pose-img-wrap { width:100%; height:300px; overflow:hidden; background:#f5f5f5; display:flex; align-items:center; justify-content:center; }
.pose-card img { max-width:100%; max-height:300px; object-fit:contain; display:block; }
.pose-no-img { width:100%; height:300px; display:flex; align-items:center; justify-content:center; background:#f5f5f5; color:#ccc; font-size:48px; }
.pose-body { padding:14px; flex:1; display:flex; flex-direction:column; }
.pose-prompt { font-size:12px; color:#555; line-height:1.5; max-height:100px; overflow:hidden; word-break:break-word; flex:1; }
.pose-actions { display:flex; gap:8px; margin-top:12px; flex-wrap:wrap; }
.btn-copy { background:#27ae60; color:#fff; border:none; padding:6px 12px; border-radius:6px; font-size:11px; cursor:pointer; font-weight:600; }
.btn-del { background:#e74c3c; color:#fff; border:none; padding:6px 12px; border-radius:6px; font-size:11px; cursor:pointer; font-weight:600; }
.flash { padding:10px 16px; border-radius:8px; margin-bottom:16px; font-size:13px; }
.flash.success { background:#d4edda; color:#155724; }
.flash.error { background:#f8d7da; color:#721c24; }
</style>
</head>
<body>
<div class="sidebar">
<div class="logo">MeuFotoApp</div>
<a href="/dashboard">Dashboard</a>
<a href="/galerias">Galerias</a>
<a href="/nova-galeria">+ Nova Galeria</a>
<a href="/selecoes">Selecoes</a>
<a href="/portfolio">Portfolio</a>
<a href="/catalogo-poses" class="active">Catalogo de Poses</a>
{% if current_user.is_admin %}<a href="/admin">Admin</a>{% endif %}
<a href="/marca">Marca d'Agua</a>
<a href="/planos">Planos</a>
<a href="/configuracoes">Configuracoes</a>
<a href="/logout">Sair</a>
</div>
<div class="main">
<div class="page-header">
<div>
<a href="{{ url_for('catalogo_poses') }}" class="back">&larr; Voltar ao Catalogo</a>
<h1 style="margin-top:6px;">{{ category }}</h1>
</div>
<span class="info-badge">{{ poses|length }} pose{{ 's' if poses|length != 1 else '' }} disponivel{{ 'is' if poses|length != 1 else '' }}</span>
</div>
{% with messages = get_flashed_messages(with_categories=true) %}
{% if messages %}
{% for category_msg, message in messages %}
<div class="flash {{ category_msg }}">{{ message }}</div>
{% endfor %}
{% endif %}
{% endwith %}
<div class="add-form">
<h2>+ Adicionar Nova Pose</h2>
<form method="POST" action="{{ url_for('add_pose', category=category) }}" enctype="multipart/form-data">
<div class="form-row">
<div class="form-group" style="flex:0 0 180px;">
<label>Foto da Pose</label>
<input type="file" name="photo" accept="image/*" onchange="previewFile(this)">
<img class="preview-img" id="preview">
</div>
<div class="form-group">
<label>Prompt (texto descritivo da pose)</label>
<textarea name="prompt" placeholder="Ex: Mulher sentada, maos sobre o colo, olhar direto para camera, blazer escuro, fundo neutro, iluminacao de estudio..."></textarea>
</div>
<button type="submit" class="btn-add">Adicionar Pose</button>
</div>
</form>
</div>
{% if poses %}
<div class="poses-grid">
{% for p in poses %}
<div class="pose-card">
{% if p.filepath and p.filepath != 'placeholder_new_category.png' %}
<div class="pose-img-wrap"><img src="/uploads/{{ p.filepath }}" alt="Pose"></div>
{% else %}
<div class="pose-no-img">&#128247;</div>
{% endif %}
<div class="pose-body">
<div class="pose-prompt">{{ p.prompt or 'Sem prompt' }}</div>
<div class="pose-actions">
<button class="btn-copy" onclick="copyPrompt({{ loop.index }})">Copiar Prompt</button>
<form method="POST" action="{{ url_for('delete_pose', category=category, pid=p.id) }}" style="display:inline;" onsubmit="return confirm('Excluir esta pose?')">
<button type="submit" class="btn-del">Excluir</button>
</form>
</div>
</div>
<textarea id="prompt_{{ loop.index }}" style="display:none;">{{ p.prompt or '' }}</textarea>
</div>
{% endfor %}
</div>
{% else %}
<div style="text-align:center;padding:40px;color:#999;">
<p style="font-size:16px;">Nenhuma pose nesta categoria ainda.</p>
<p style="margin-top:8px;">Use o formulario acima para adicionar a primeira pose!</p>
</div>
{% endif %}
</div>
<script>
function previewFile(input) {
    var preview = document.getElementById('preview');
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) { preview.src = e.target.result; preview.style.display = 'block'; };
        reader.readAsDataURL(input.files[0]);
    } else {
        preview.style.display = 'none';
    }
}
function copyPrompt(id) {
    var text = document.getElementById('prompt_' + id).value;
    navigator.clipboard.writeText(text).then(function() {
        alert('Prompt copiado!');
    });
}
</script>
</body>
</html>""")
print('OK: catalogo_categoria.html reescrito com object-fit:contain')

# ===== 3. REESCREVER catalogo_poses.html COM object-fit:contain =====
cat_main = os.path.join(base_dir, 'templates', 'catalogo_poses.html')
with open(cat_main, 'w', encoding='utf-8') as f:
    f.write(r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Catalogo de Poses</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Segoe UI',Arial,sans-serif; background:#f0f2f5; color:#333; }
.sidebar { position:fixed; left:0; top:0; width:220px; height:100vh; background:#1a1a2e; padding:20px 0; overflow-y:auto; z-index:100; }
.sidebar .logo { color:#fff; font-size:18px; font-weight:700; padding:0 20px 24px; border-bottom:1px solid rgba(255,255,255,0.1); }
.sidebar a { display:block; color:#aab; text-decoration:none; padding:12px 20px; font-size:13px; transition:0.2s; }
.sidebar a:hover { background:rgba(255,255,255,0.05); color:#fff; }
.sidebar a.active { background:rgba(77,166,255,0.15); color:#4da6ff; border-left:3px solid #4da6ff; }
.main { margin-left:220px; padding:24px; }
.page-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:24px; }
.page-header h1 { font-size:24px; font-weight:700; }
.btn-new-cat { background:#4da6ff; color:#fff; border:none; padding:10px 20px; border-radius:8px; font-size:14px; font-weight:600; cursor:pointer; }
.btn-new-cat:hover { background:#3a96f0; }
.cat-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:20px; }
.cat-card { background:#fff; border-radius:12px; overflow:hidden; box-shadow:0 2px 10px rgba(0,0,0,0.08); cursor:pointer; transition:transform 0.2s,box-shadow 0.2s; text-decoration:none; color:inherit; display:block; }
.cat-card:hover { transform:translateY(-3px); box-shadow:0 6px 20px rgba(0,0,0,0.12); }
.cat-thumb { width:100%; height:200px; overflow:hidden; background:#f5f5f5; display:flex; align-items:center; justify-content:center; }
.cat-thumb img { max-width:100%; max-height:200px; object-fit:contain; display:block; }
.cat-thumb-icon { font-size:48px; color:#ccc; }
.cat-body { padding:16px; }
.cat-body h3 { font-size:16px; font-weight:700; margin-bottom:4px; }
.cat-body p { font-size:12px; color:#888; }
.cat-badge { display:inline-block; background:#e8f4fd; color:#1976d2; padding:3px 10px; border-radius:10px; font-size:11px; font-weight:600; margin-top:8px; }
.modal-overlay { display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:1000; justify-content:center; align-items:center; }
.modal-overlay.show { display:flex; }
.modal { background:#fff; border-radius:12px; padding:28px; width:400px; max-width:90%; }
.modal h2 { font-size:18px; margin-bottom:16px; }
.modal input { width:100%; padding:12px; border:1px solid #ddd; border-radius:8px; font-size:14px; margin-bottom:16px; }
.modal-btns { display:flex; gap:10px; justify-content:flex-end; }
.modal-btns button { padding:10px 20px; border-radius:8px; font-size:14px; font-weight:600; cursor:pointer; border:none; }
.btn-cancel { background:#f0f0f0; color:#555; }
.btn-create { background:#27ae60; color:#fff; }
.flash { padding:10px 16px; border-radius:8px; margin-bottom:16px; font-size:13px; }
.flash.success { background:#d4edda; color:#155724; }
.flash.error { background:#f8d7da; color:#721c24; }
</style>
</head>
<body>
<div class="sidebar">
<div class="logo">MeuFotoApp</div>
<a href="/dashboard">Dashboard</a>
<a href="/galerias">Galerias</a>
<a href="/nova-galeria">+ Nova Galeria</a>
<a href="/selecoes">Selecoes</a>
<a href="/portfolio">Portfolio</a>
<a href="/catalogo-poses" class="active">Catalogo de Poses</a>
{% if current_user.is_admin %}<a href="/admin">Admin</a>{% endif %}
<a href="/marca">Marca d'Agua</a>
<a href="/planos">Planos</a>
<a href="/configuracoes">Configuracoes</a>
<a href="/logout">Sair</a>
</div>
<div class="main">
<div class="page-header">
<h1>Catalogo de Poses</h1>
<button class="btn-new-cat" onclick="document.getElementById('modalNewCat').classList.add('show')">+ Nova Categoria</button>
</div>
{% with messages = get_flashed_messages(with_categories=true) %}
{% if messages %}
{% for category, message in messages %}
<div class="flash {{ category }}">{{ message }}</div>
{% endfor %}
{% endif %}
{% endwith %}
{% if categorias %}
<div class="cat-grid">
{% for cat in categorias %}
<a href="{{ url_for('catalogo_categoria', category=cat.nome) }}" class="cat-card">
{% if cat.thumb and cat.thumb != 'placeholder_new_category.png' %}
<div class="cat-thumb"><img src="/uploads/{{ cat.thumb }}" alt="{{ cat.nome }}"></div>
{% else %}
<div class="cat-thumb"><div class="cat-thumb-icon">&#128247;</div></div>
{% endif %}
<div class="cat-body">
<h3>{{ cat.nome }}</h3>
<p>{{ cat.count }} pose{{ 's' if cat.count != 1 else '' }} disponivel{{ 'is' if cat.count != 1 else '' }}</p>
<span class="cat-badge">Ver poses &rarr;</span>
</div>
</a>
{% endfor %}
</div>
{% else %}
<div style="text-align:center;padding:60px 20px;">
<p style="font-size:18px;color:#999;margin-bottom:16px;">Nenhuma categoria cadastrada ainda.</p>
<p style="color:#aaa;">Clique em "+ Nova Categoria" para comecar!</p>
</div>
{% endif %}
</div>
<div class="modal-overlay" id="modalNewCat">
<div class="modal">
<h2>Nova Categoria de Poses</h2>
<form method="POST" action="{{ url_for('nova_categoria_pose') }}">
<input type="text" name="nome_categoria" placeholder="Ex: MEDICA, ENGENHEIRA, ARQUITETA..." required>
<div class="modal-btns">
<button type="button" class="btn-cancel" onclick="document.getElementById('modalNewCat').classList.remove('show')">Cancelar</button>
<button type="submit" class="btn-create">Criar Categoria</button>
</div>
</form>
</div>
</div>
</body>
</html>""")
print('OK: catalogo_poses.html reescrito com object-fit:contain')

# ===== 4. VERIFICAR app.py TEM TEMPLATES_AUTO_RELOAD =====
app_path = os.path.join(base_dir, 'app.py')
with open(app_path, 'r', encoding='utf-8') as f:
    app_content = f.read()

if 'TEMPLATES_AUTO_RELOAD' not in app_content:
    inject = "app.config['TEMPLATES_AUTO_RELOAD'] = True\n"
    pos = app_content.find('app.config.from_object(Config)')
    if pos != -1:
        end = app_content.find('\n', pos) + 1
        app_content = app_content[:end] + inject + app_content[end:]
        with open(app_path, 'w', encoding='utf-8') as f:
            f.write(app_content)
        print('OK: TEMPLATES_AUTO_RELOAD=True adicionado ao app.py')
    else:
        print('AVISO: nao encontrou config para adicionar TEMPLATES_AUTO_RELOAD')
else:
    print('OK: TEMPLATES_AUTO_RELOAD ja presente')

print('\nPRONTO! Rode: python app.py')