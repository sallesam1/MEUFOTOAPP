import os, re

base_dir = os.path.dirname(os.path.abspath(__file__))
app_path = os.path.join(base_dir, 'app.py')
models_path = os.path.join(base_dir, 'models.py')
tpl_dir = os.path.join(base_dir, 'templates')

changes = []

# ========== 1. MODELS.PY: Adicionar campos de email no AppSettings ==========
with open(models_path, 'r', encoding='utf-8') as f:
    models = f.read()

if 'class AppSettings' in models:
    # Adicionar campos se nao existirem
    if 'notification_email' not in models:
        old_settings = re.search(r'class AppSettings\(db\.Model\):(.*?)(?=\nclass |\Z)', models, re.DOTALL)
        if old_settings:
            new_fields = old_settings.group(0) + """
    notification_email = db.Column(db.String(180))
    smtp_server = db.Column(db.String(200))
    smtp_port = db.Column(db.Integer)
    smtp_password = db.Column(db.String(200))
"""
            models = models.replace(old_settings.group(0), new_fields)
            with open(models_path, 'w', encoding='utf-8') as f:
                f.write(models)
            changes.append('Campos de email adicionados ao AppSettings')
    else:
        changes.append('Campos de email ja existem no AppSettings')
else:
    changes.append('AVISO: AppSettings nao encontrado no models.py')

# ========== 2. APP.PY: Adicionar funcao de envio de email ==========
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Adicionar imports de email
if 'import smtplib' not in content:
    # Inserir apos os imports existentes
    import_area = re.search(r'^(import .*?\n(?:import .*?\n)*)', content, re.MULTILINE)
    if import_area:
        content = content[:import_area.end()] + "import smtplib\nfrom email.mime.text import MIMEText\nfrom email.mime.multipart import MIMEMultipart\n" + content[import_area.end():]
        changes.append('Imports de email adicionados ao app.py')

# Adicionar funcao send_notification_email antes da rota de selecao
if 'def send_notification_email(' not in content:
    email_func = '''
# ===== FUNCAO DE ENVIO DE EMAIL =====
def send_notification_email(subject, body_html, recipient_email):
    settings = AppSettings.query.first()
    if not settings or not settings.notification_email or not settings.smtp_password:
        print('AVISO: Email nao configurado em Configuracoes. Selecao salva apenas no banco.')
        return False
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = settings.notification_email
        msg['To'] = recipient_email
        html_part = MIMEText(body_html, 'html')
        msg.attach(html_part)
        server = smtplib.SMTP(settings.smtp_server or 'smtp.mail.yahoo.com', settings.smtp_port or 587)
        server.starttls()
        server.login(settings.notification_email, settings.smtp_password)
        server.sendmail(settings.notification_email, recipient_email, msg.as_string())
        server.quit()
        print(f'EMAIL ENVIADO para {recipient_email}')
        return True
    except Exception as e:
        print(f'ERRO ao enviar email: {e}')
        return False

'''
    marker = "if __name__"
    if marker in content:
        pos = content.index(marker)
        content = content[:pos] + email_func + '\n' + content[pos:]
    else:
        content += '\n' + email_func
    changes.append('Funcao send_notification_email adicionada')

# ========== 3. APP.PY: Atualizar rota public_catalog_selecionar para enviar email ==========
old_selecionar = """@app.route('/catalogo-publico/<path:category>/selecionar', methods=['POST'])
def public_catalog_selecionar(category):
    from urllib.parse import unquote
    from sqlalchemy import or_
    category = unquote(category)
    sel = PoseSelection()
    sel.category = category
    sel.client_name = request.form.get('client_name', '')
    sel.client_email = request.form.get('client_email', '')
    sel.selected_poses = request.form.get('selected_poses', '')
    sel.message = request.form.get('message', '')
    db.session.add(sel)
    db.session.commit()
    poses = PosePhoto.query.filter(
        or_(PosePhoto.category == category, PosePhoto.profession == category)
    ).order_by(PosePhoto.id.asc()).all()
    return render_template('public_catalog.html', poses=poses, category=category, selection_sent=True)"""

new_selecionar = """@app.route('/catalogo-publico/<path:category>/selecionar', methods=['POST'])
def public_catalog_selecionar(category):
    from urllib.parse import unquote
    from sqlalchemy import or_
    category = unquote(category)
    sel = PoseSelection()
    sel.category = category
    sel.client_name = request.form.get('client_name', '')
    sel.client_email = request.form.get('client_email', '')
    sel.selected_poses = request.form.get('selected_poses', '')
    sel.message = request.form.get('message', '')
    db.session.add(sel)
    db.session.commit()

    # Buscar poses selecionadas para o email
    pose_ids = [int(x) for x in sel.selected_poses.split(',') if x.strip().isdigit()]
    selected_poses = PosePhoto.query.filter(PosePhoto.id.in_(pose_ids)).all() if pose_ids else []

    # Enviar email de notificacao
    settings = AppSettings.query.first()
    if settings and settings.notification_email:
        poses_html = ''
        for p in selected_poses:
            poses_html += f'<div style="display:inline-block;margin:5px;"><img src="http://127.0.0.1:5000/uploads/{p.filepath}" style="width:120px;height:120px;object-fit:cover;border-radius:8px;border:1px solid #30363d;"></div>'

        email_body = f'''
        <html><body style="font-family:Segoe UI,sans-serif;background:#0d1117;color:#fff;padding:20px;">
        <h2 style="color:#238636;">Nova Selecao de Poses!</h2>
        <p><strong>Cliente:</strong> {sel.client_name}</p>
        <p><strong>Email:</strong> {sel.client_email}</p>
        <p><strong>Categoria:</strong> {sel.category}</p>
        <p><strong>Fotos selecionadas:</strong> {len(selected_poses)}</p>
        {f'<p><strong>Mensagem:</strong> {sel.message}</p>' if sel.message else ''}
        <hr style="border-color:#30363d;margin:20px 0;">
        <p style="color:#8b949e;font-size:13px;">Fotos selecionadas pelo cliente:</p>
        <div style="margin:10px 0;">{poses_html}</div>
        <hr style="border-color:#30363d;margin:20px 0;">
        <p style="color:#8b949e;font-size:12px;">Veja todas as selecoes em: http://127.0.0.1:5000/selecoes-poses</p>
        </body></html>
        '''
        send_notification_email(
            f'Nova Selecao de {sel.client_name} - {sel.category}',
            email_body,
            settings.notification_email
        )

    poses = PosePhoto.query.filter(
        or_(PosePhoto.category == category, PosePhoto.profession == category)
    ).order_by(PosePhoto.id.asc()).all()
    return render_template('public_catalog.html', poses=poses, category=category, selection_sent=True)"""

if old_selecionar in content:
    content = content.replace(old_selecionar, new_selecionar)
    changes.append('Rota public_catalog_selecionar atualizada com envio de email')
else:
    changes.append('AVISO: rota public_catalog_selecionar nao encontrada para substituir')

# ========== 4. APP.PY: Adicionar rota para salvar configuracoes de email ==========
if 'def save_email_config(' not in content:
    email_route = '''
# ===== SALVAR CONFIG DE EMAIL =====
@app.route('/configuracoes/email', methods=['POST'])
@login_required
def save_email_config():
    settings = AppSettings.query.first()
    if not settings:
        settings = AppSettings()
        db.session.add(settings)
    settings.notification_email = request.form.get('notification_email', '').strip()
    settings.smtp_server = request.form.get('smtp_server', '').strip()
    settings.smtp_port = int(request.form.get('smtp_port', '587') or '587')
    settings.smtp_password = request.form.get('smtp_password', '').strip()
    db.session.commit()
    flash('Configuracoes de email salvas!', 'success')
    return redirect(url_for('configuracoes'))

'''
    marker = "if __name__"
    if marker in content:
        pos = content.index(marker)
        content = content[:pos] + email_route + '\n' + content[pos:]
    else:
        content += '\n' + email_route
    changes.append('Rota save_email_config adicionada')

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)

# ========== 5. CONFIGURACOES.HTML: Adicionar formulario de email ==========
config_path = os.path.join(tpl_dir, 'configuracoes.html')
if os.path.exists(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        config = f.read()

    if 'notification_email' not in config:
        email_form = """
<div style="background:#161b22;border:1px solid #30363d;border-radius:12px;padding:24px;margin-bottom:20px;">
<h3 style="color:#fff;margin-bottom:16px;">📧 Configuracoes de E-mail (Notificacoes)</h3>
<p style="color:#8b949e;font-size:12px;margin-bottom:16px;">Configure seu e-mail para receber notificacoes quando clientes enviarem selecoes de poses.</p>
<form method="POST" action="{{ url_for('save_email_config') }}">
<label style="display:block;margin-bottom:6px;color:#8b949e;font-size:12px;">SEU E-MAIL (PARA RECEBER NOTIFICACOES)</label>
<input type="email" name="notification_email" value="{{ site_settings.notification_email if site_settings else '' }}" placeholder="seuemail@yahoo.com.br" style="width:100%;padding:10px;background:#0d1117;border:1px solid #30363d;border-radius:8px;color:#fff;font-size:14px;margin-bottom:12px;">

<label style="display:block;margin-bottom:6px;color:#8b949e;font-size:12px;">SERVIDOR SMTP</label>
<input type="text" name="smtp_server" value="{{ site_settings.smtp_server if site_settings and site_settings.smtp_server else 'smtp.mail.yahoo.com' }}" style="width:100%;padding:10px;background:#0d1117;border:1px solid #30363d;border-radius:8px;color:#fff;font-size:14px;margin-bottom:12px;">

<label style="display:block;margin-bottom:6px;color:#8b949e;font-size:12px;">PORTA</label>
<input type="number" name="smtp_port" value="{{ site_settings.smtp_port if site_settings and site_settings.smtp_port else 587 }}" style="width:100%;padding:10px;background:#0d1117;border:1px solid #30363d;border-radius:8px;color:#fff;font-size:14px;margin-bottom:12px;">

<label style="display:block;margin-bottom:6px;color:#8b949e;font-size:12px;">SENHA DO APP (nao e sua senha normal - veja instrucoes abaixo)</label>
<input type="password" name="smtp_password" value="{{ site_settings.smtp_password if site_settings else '' }}" placeholder="Senha de app" style="width:100%;padding:10px;background:#0d1117;border:1px solid #30363d;border-radius:8px;color:#fff;font-size:14px;margin-bottom:12px;">

<div style="background:#0d1117;border:1px solid #30363d;border-radius:8px;padding:12px;margin-bottom:12px;">
<p style="color:#8b949e;font-size:11px;line-height:1.6;">
<strong style="color:#58a6ff;">Como obter a Senha de App (Yahoo):</strong><br>
1. Acesse <a href="https://login.yahoo.com/account/security" target="_blank" style="color:#58a6ff;">Seguranca da conta Yahoo</a><br>
2. Ative a verificacao em duas etapas<br>
3. Clique em "Gerenciar senhas de app"<br>
4. Crie uma senha de app (escolha "Outro app")<br>
5. Copie a senha gerada e cole aqui acima
</p>
</div>

<button type="submit" style="background:#238636;color:#fff;border:none;padding:10px 20px;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer;">Salvar Configuracoes de Email</button>
</form>
</div>
"""
        body_idx = config.find('<body')
        if body_idx >= 0:
            end_tag = config.find('>', body_idx)
            config = config[:end_tag+1] + '\n' + email_form + config[end_tag+1:]
        else:
            config = email_form + config
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config)
        changes.append('Formulario de configuracao de email adicionado em configuracoes.html')
    else:
        changes.append('Formulario de email ja existe em configuracoes.html')

# ========== RESULTADO ==========
print('=' * 50)
for c in changes:
    print('OK: ' + c)
print('=' * 50)
print('\nPRONTO! Rode: python app.py')
print('\nDepois va em Configuracoes e configure seu email.')
print('Use SMTP do Yahoo: smtp.mail.yahoo.com / Porta: 587')