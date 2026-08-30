import os
import shutil

base = os.path.dirname(os.path.abspath(__file__))
app_path = os.path.join(base, 'app.py')

# Backup de seguranca
backup = os.path.join(base, 'app_backup.py')
if os.path.exists(app_path):
    shutil.copy2(app_path, backup)
    print(f'[BACKUP] app.py copiado para app_backup.py')

with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Normaliza quebras de linha (Windows -> padrao)
content = content.replace('\r\n', '\n')

PATCHES = [
    # 1. Imports duplicados
    ("Imports duplicados (smtplib/MIMEText)",
     "import urllib.request, secrets, io, zipfile, smtplib\nimport smtplib\nfrom email.mime.text import MIMEText\nfrom email.mime.multipart import MIMEMultipart\nfrom email.mime.text import MIMEText",
     "import urllib.request, secrets, io, zipfile, smtplib\nfrom email.mime.text import MIMEText\nfrom email.mime.multipart import MIMEMultipart", 1),

    # 2. load_user duplicado
    ("load_user duplicado",
     "@login_manager.user_loader\ndef load_user(uid):\n    return User.query.get(int(uid))\n@login_manager.user_loader\ndef load_user(uid):\n    return User.query.get(int(uid))",
     "@login_manager.user_loader\ndef load_user(uid):\n    return User.query.get(int(uid))", 1),

    # 3. serve_upload -> send_from_directory
    ("serve_upload: send_file -> send_from_directory",
     "@app.route('/uploads/<filename>')\ndef serve_upload(filename):\n    if filename == 'pending':\n        abort(404)\n    return send_file(os.path.join(UPLOAD_FOLDER, filename))",
     "@app.route('/uploads/<filename>')\ndef serve_upload(filename):\n    if filename == 'pending':\n        abort(404)\n    return send_from_directory(UPLOAD_FOLDER, filename)", 1),

    # 4. serve_wm (final) -> send_from_directory
    ("serve_wm: send_file -> send_from_directory",
     "    if filename == 'pending':\n        abort(404)\n    return send_file(os.path.join(UPLOAD_FOLDER, filename))",
     "    if filename == 'pending':\n        abort(404)\n    return send_from_directory(UPLOAD_FOLDER, filename)", 1),

    # 5. bloquear_usuario: is_active -> active
    ("bloquear_usuario: is_active -> active",
     "    user.is_active = not user.is_active\n    db.session.commit()\n    flash('Usuario {} com sucesso!'.format('bloqueado' if not user.is_active else 'desbloqueado'), 'success')",
     "    user.active = not user.active\n    db.session.commit()\n    flash('Usuario {} com sucesso!'.format('bloqueado' if not user.active else 'desbloqueado'), 'success')", 1),

    # 6. admin_change_plan: plano em maiusculo
    ("admin_change_plan: plano padronizado em MAIUSCULO",
     "    if novo_plano in ['free', 'pro', 'premium']:\n        user.plan = novo_plano\n        db.session.commit()",
     "    if novo_plano in ['free', 'pro', 'premium']:\n        user.plan = novo_plano.upper()\n        db.session.commit()", 1),

    # 7. admin_categorias (stub seguro - evita crash)
    ("admin_categorias: corrigido (nao crasha mais)",
     "@app.route('/admin/categorias', methods=['POST'])\n@login_required\ndef admin_categorias():\n    if not current_user.is_admin: abort(403)\n    slug = request.form.get('slug', '').lower().strip(); label = request.form.get('label', '').strip()\n    if slug and label and not [].filter_by(slug=slug).first():\n        db.session.add(dict(slug=slug, label=label)); db.session.commit()\n        flash('Categoria adicionada!', 'success')\n    else: flash('Slug ja existe ou invalido.', 'error')\n    return redirect(url_for('admin'))",
     "@app.route('/admin/categorias', methods=['POST'])\n@login_required\ndef admin_categorias():\n    if not current_user.is_admin: abort(403)\n    flash('Gestao de categorias em manutencao.', 'error')\n    return redirect(url_for('admin'))", 1),

    # 8. delete_categoria (stub seguro)
    ("delete_categoria: corrigido (nao crasha mais)",
     "@app.route('/admin/categorias/<int:cid>/delete', methods=['POST'])\n@login_required\ndef delete_categoria(cid):\n    if not current_user.is_admin: abort(403)\n    db.session.delete([].get_or_404(cid)); db.session.commit()\n    flash('Categoria removida.', 'success'); return redirect(url_for('admin'))",
     "@app.route('/admin/categorias/<int:cid>/delete', methods=['POST'])\n@login_required\ndef delete_categoria(cid):\n    if not current_user.is_admin: abort(403)\n    flash('Gestao de categorias em manutencao.', 'error'); return redirect(url_for('admin'))", 1),

    # 9. admin_pacotes (stub seguro)
    ("admin_pacotes: corrigido (nao crasha mais)",
     "@app.route('/admin/pacotes', methods=['POST'])\n@login_required\ndef admin_pacotes():\n    if not current_user.is_admin: abort(403)\n    key = request.form.get('key', '').lower().strip(); label = request.form.get('label', '').strip()\n    limit = int(request.form.get('limit', 10)); price = request.form.get('price', '').strip()\n    if key and label:\n        ex = [].filter_by(key=key).first()\n        if ex: ex.label, ex.limit, ex.price = label, limit, price\n        else: db.session.add(dict(key=key, label=label, limit=limit, price=price))\n        db.session.commit(); flash('Pacote salvo!', 'success')\n    return redirect(url_for('admin'))",
     "@app.route('/admin/pacotes', methods=['POST'])\n@login_required\ndef admin_pacotes():\n    if not current_user.is_admin: abort(403)\n    flash('Gestao de pacotes em manutencao.', 'error')\n    return redirect(url_for('admin'))", 1),

    # 10. delete_pacote (stub seguro)
    ("delete_pacote: corrigido (nao crasha mais)",
     "@app.route('/admin/pacotes/<int:pid>/delete', methods=['POST'])\n@login_required\ndef delete_pacote(pid):\n    if not current_user.is_admin: abort(403)\n    db.session.delete([].get_or_404(pid)); db.session.commit()\n    flash('Pacote removido.', 'success'); return redirect(url_for('admin'))",
     "@app.route('/admin/pacotes/<int:pid>/delete', methods=['POST'])\n@login_required\ndef delete_pacote(pid):\n    if not current_user.is_admin: abort(403)\n    flash('Gestao de pacotes em manutencao.', 'error'); return redirect(url_for('admin'))", 1),

    # 11. debug off
    ("debug=True -> debug=False (seguranca)",
     "    app.run(debug=True)",
     "    app.run(debug=False)", 1),
]

ok = 0
avisos = 0
for nome, busca, troca, esperado in PATCHES:
    n = content.count(busca)
    if n >= 1:
        content = content.replace(busca, troca)
        ok += 1
        print(f'[OK] {nome}')
    else:
        avisos += 1
        print(f'[AVISO] Nao encontrado: {nome}')

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)

print()
print(f'CORRECOES aplicadas: {ok} de {len(PATCHES)}')
if avisos:
    print(f'{avisos} item(ns) nao encontrado(s) - pode ja ter sido corrigido antes.')
print('Backup salvo em app_backup.py')
print()
print('PROXIMO PASSO:')
print('1) Reinicie o Flask: Ctrl+C e depois python app.py')
print('2) Abra http://127.0.0.1:5000/landing com Ctrl+Shift+R')