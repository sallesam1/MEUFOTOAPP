import os
import secrets
import base64
import json
import urllib.request, secrets, io, zipfile, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from flask import (Flask, render_template, request, redirect, url_for,
                   flash, send_file, abort, send_from_directory)
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from models import db, User, Galeria, Photo, Selection, Watermark, PortfolioPhoto, PosePhoto, AppSettings, PoseSelection, Plan
from config import Config
from watermark import apply_watermark, enhance_image, get_watermarked_bytes
from social_sizes import resize_for_social, SOCIAL_SIZES
from supabase_storage import upload_bytes, get_public_url, delete_file, download_bytes
load_dotenv()
app = Flask(__name__)
app.config.from_object(Config)
app.config['TEMPLATES_AUTO_RELOAD'] = True
# ===== CORRECAO: usa o banco do Supabase (PostgreSQL) se DATABASE_URL existir =====
_database_url = os.environ.get('DATABASE_URL')
if _database_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = _database_url
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping': True}
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
google = None
if os.environ.get('GOOGLE_CLIENT_ID'):
    try:
        from authlib.integrations.flask_client import OAuth
        oauth = OAuth(app)
        google = oauth.register(
            name='google', client_id=os.environ.get('GOOGLE_CLIENT_ID'),
            client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_kwargs={'scope': 'openid email profile'})
    except ImportError:
        pass
def allowed_file(fn):
    return '.' in fn and fn.rsplit('.', 1)[1].lower() in ALLOWED
def trial_expired(user):
    if user.is_admin: return False
    if user.trial_started_at:
        return datetime.utcnow() > user.trial_started_at + timedelta(days=7)
    return False
def send_notification_email(subject, body_html, recipient_email):
    settings = AppSettings.query.first()
    if not settings:
        print('AVISO: Nenhuma configuracao encontrada.')
        return False
    smtp_host = getattr(settings, 'smtp_host', None) or getattr(settings, 'smtp_server', None) or 'smtp.gmail.com'
    smtp_user = getattr(settings, 'smtp_user', None) or getattr(settings, 'notification_email', None)
    smtp_pass = getattr(settings, 'smtp_password', None)
    smtp_port = getattr(settings, 'smtp_port', None) or 587
    if not smtp_user or not smtp_pass:
        print(f'AVISO: Email ou senha nao configurados. user={smtp_user}, pass={"sim" if smtp_pass else "NAO"}')
        return False
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = smtp_user
        msg['To'] = recipient_email
        html_part = MIMEText(body_html, 'html')
        msg.attach(html_part)
        print(f'Conectando a {smtp_host}:{smtp_port} com user={smtp_user}')
        server = smtplib.SMTP(smtp_host, int(smtp_port))
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, recipient_email, msg.as_string())
        server.quit()
        print(f'EMAIL ENVIADO para {recipient_email}')
        return True
    except Exception as e:
        print(f'ERRO ao enviar email: {e}')
        return False
# ===== AUTH =====
@app.route('/')
def index():
    return render_template('landing.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = User.query.filter_by(email=request.form.get('email', '').lower()).first()
        if u and u.password_hash and bcrypt.check_password_hash(u.password_hash, request.form.get('password', '')):
            if not u.active:
                flash('Conta desativada.', 'error'); return render_template('login.html')
            login_user(u); return redirect(url_for('dashboard'))
        flash('Credenciais invalidas', 'error')
    return render_template('login.html')
@app.route('/login/google')
def login_google():
    if not google:
        flash('Login com Google nao configurado.', 'error'); return redirect(url_for('login'))
    return google.authorize_redirect(url_for('authorize_google', _external=True))
@app.route('/authorize/google')
def authorize_google():
    if not google: return redirect(url_for('login'))
    token = google.authorize_access_token()
    info = google.parse_id_token(token)
    email = info.get('email', '').lower()
    gid = info.get('sub'); name = info.get('name', '')
    u = User.query.filter_by(email=email).first()
    if not u:
        u = User(email=email, name=name, google_id=gid, studio_name=name)
        db.session.add(u); db.session.commit()
        db.session.add(Watermark(user_id=u.id, text=name or 'MeuFotoApp')); db.session.commit()
    elif not u.google_id:
        u.google_id = gid; db.session.commit()
    login_user(u); return redirect(url_for('dashboard'))
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        email = request.form.get('email', '').lower()
        if User.query.filter_by(email=email).first():
            flash('E-mail ja cadastrado', 'error'); return render_template('registro.html')
        hashed = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
        is_first = User.query.count() == 0
        u = User(studio_name=request.form.get('studio_name'), name=request.form.get('name'),
                 email=email, password_hash=hashed, is_admin=is_first)
        db.session.add(u); db.session.commit()
        db.session.add(Watermark(user_id=u.id, text=u.studio_name or 'MeuFotoApp')); db.session.commit()
        login_user(u); return redirect(url_for('dashboard'))
    return render_template('registro.html')
@app.route('/logout')
@login_required
def logout():
    logout_user(); return redirect(url_for('login'))
# ===== DASHBOARD =====
@app.route('/dashboard')
@login_required
def dashboard():
    gs = Galeria.query.filter_by(user_id=current_user.id).order_by(Galeria.created_at.desc()).limit(6).all()
    ids = [g.id for g in gs]
    tf = Photo.query.filter(Photo.galeria_id.in_(ids)).count() if ids else 0
    ts = Selection.query.filter(Selection.galeria_id.in_(ids)).count() if ids else 0
    td = None
    if current_user.trial_started_at and not current_user.is_admin:
        td = max(0, 7 - (datetime.utcnow() - current_user.trial_started_at).days)
    return render_template('dashboard.html', galerias=gs, total_fotos=tf, total_selecoes=ts, trial_days_left=td)
# ===== GALERIAS =====
@app.route('/galerias')
@login_required
def list_galerias():
    gs = Galeria.query.filter_by(user_id=current_user.id).order_by(Galeria.created_at.desc()).all()
    return render_template('list_galerias.html', galerias=gs)
@app.route('/nova-galeria', methods=['GET', 'POST'])
@login_required
def nova_galeria():
    if trial_expired(current_user):
        flash('Trial expirado. Faca upgrade.', 'error'); return redirect(url_for('planos'))
    if request.method == 'POST':
        tok = secrets.token_urlsafe(32)
        g = Galeria(user_id=current_user.id, title=request.form.get('title'),
                    client_name=request.form.get('client_name'), client_email=request.form.get('client_email'),
                    category=request.form.get('category'), event_date=request.form.get('event_date'),
                    client_message=request.form.get('client_message'), share_token=tok)
        db.session.add(g); db.session.commit()
        return redirect(url_for('galeria', gid=g.id))
    return render_template('nova_galeria.html', categories=[])
@app.route('/galeria/<int:gid>', methods=['GET', 'POST'])
@login_required
def galeria(gid):
    g = Galeria.query.get_or_404(gid)
    if g.user_id != current_user.id and not current_user.is_admin: abort(403)
    if request.method == 'POST':
        files = request.files.getlist('photos')
        wm = Watermark.query.filter_by(user_id=current_user.id).first()
        for f in files:
            if f and allowed_file(f.filename):
                fn = secure_filename(f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{f.filename}")
                upload_bytes(f.read(), fn, f.content_type or 'image/jpeg')
                db.session.add(Photo(galeria_id=g.id, filepath=fn, filename=f.filename, has_watermark=False))
        db.session.commit()
        flash(f'{len(files)} foto(s) enviada(s)!', 'success')
        return redirect(url_for('galeria', gid=g.id))
    photos = Photo.query.filter_by(galeria_id=g.id).all()
    sels = Selection.query.filter_by(galeria_id=g.id).all()
    return render_template('galeria.html', galeria=g, photos=photos, selections=sels)
@app.route('/galeria/<int:gid>/delete', methods=['POST'])
@login_required
def delete_galeria(gid):
    g = Galeria.query.get_or_404(gid)
    if g.user_id != current_user.id: abort(403)
    for p in Photo.query.filter_by(galeria_id=g.id).all():
        try: delete_file(p.filepath)
        except: pass
        db.session.delete(p)
    Selection.query.filter_by(galeria_id=g.id).delete()
    db.session.delete(g); db.session.commit()
    flash('Galeria excluida.', 'success'); return redirect(url_for('list_galerias'))
@app.route('/galeria/<int:gid>/photo/<int:pid>/delete', methods=['POST'])
@login_required
def delete_photo(gid, pid):
    p = Photo.query.get_or_404(pid); g = Galeria.query.get_or_404(gid)
    if g.user_id != current_user.id: abort(403)
    try: delete_file(p.filepath)
    except: pass
    db.session.delete(p); db.session.commit()
    flash('Foto excluida.', 'success'); return redirect(url_for('galeria', gid=gid))
@app.route('/galeria/<int:gid>/photo/<int:pid>/enhance', methods=['POST'])
@login_required
def enhance_photo(gid, pid):
    p = Photo.query.get_or_404(pid); g = Galeria.query.get_or_404(gid)
    if g.user_id != current_user.id: abort(403)
    try:
        data = download_bytes(p.filepath)
        tmp = os.path.join(UPLOAD_FOLDER, '_tmp_' + p.filepath)
        with open(tmp, 'wb') as f:
            f.write(data)
        enhance_image(tmp)
        with open(tmp, 'rb') as f:
            upload_bytes(f.read(), p.filepath, 'image/jpeg')
        try: os.remove(tmp)
        except: pass
        p.enhanced = True; db.session.commit()
        flash('Imagem melhorada!', 'success')
    except: flash('Erro ao melhorar.', 'error')
    return redirect(url_for('galeria', gid=gid))
@app.route('/galeria/<int:gid>/photo/<int:pid>/resize/<platform>')
@login_required
def resize_photo(gid, pid, platform):
    p = Photo.query.get_or_404(pid); g = Galeria.query.get_or_404(gid)
    if g.user_id != current_user.id: abort(403)
    data = download_bytes(p.filepath)
    tmp = os.path.join(UPLOAD_FOLDER, '_tmp_' + p.filepath)
    with open(tmp, 'wb') as f:
        f.write(data)
    out = resize_for_social(tmp, platform)
    try: os.remove(tmp)
    except: pass
    if out: return send_file(out, as_attachment=True)
    flash('Plataforma invalida.', 'error'); return redirect(url_for('galeria', gid=gid))
@app.route('/galeria/<int:gid>/photo/<int:pid>/rewatermark', methods=['POST'])
@login_required
def rewatermark(gid, pid):
    p = Photo.query.get_or_404(pid); g = Galeria.query.get_or_404(gid)
    if g.user_id != current_user.id: abort(403)
    wm = Watermark.query.filter_by(user_id=current_user.id).first()
    if wm:
        try:
            data = download_bytes(p.filepath)
            tmp = os.path.join(UPLOAD_FOLDER, '_tmp_' + p.filepath)
            with open(tmp, 'wb') as f:
                f.write(data)
            apply_watermark(tmp, wm.text or 'MeuFotoApp', wm.color, wm.opacity, 'diagonal', wm.stroke, wm.logo_path)
            with open(tmp, 'rb') as f:
                upload_bytes(f.read(), p.filepath, 'image/jpeg')
            try: os.remove(tmp)
            except: pass
            p.has_watermark = True; db.session.commit()
            flash('Marca dagua reaplicada!', 'success')
        except: flash('Erro ao aplicar marca dagua.', 'error')
    return redirect(url_for('galeria', gid=gid))
@app.route('/uploads/<filename>')
def serve_upload(filename):
    if filename == 'pending':
        abort(404)
    return redirect(get_public_url(filename))
@app.route('/wm/<filename>')
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
            try:
                data = download_bytes(filename)
                tmp = os.path.join(UPLOAD_FOLDER, '_tmp_' + filename)
                with open(tmp, 'wb') as f:
                    f.write(data)
                img_bytes = get_watermarked_bytes(
                    tmp,
                    wm.text or 'MeuFotoApp',
                    wm.color or '#ffffff',
                    wm.opacity or 30,
                    'diagonal',
                    wm.stroke,
                    wm.logo_path
                )
                try: os.remove(tmp)
                except: pass
                return send_file(img_bytes, mimetype='image/jpeg')
            except Exception as e:
                print('WM error: ' + str(e))
    if filename == 'pending':
        abort(404)
    return send_from_directory(UPLOAD_FOLDER, filename)
@app.route('/g/<token>', methods=['GET', 'POST'])
def cliente_view(token):
    g = Galeria.query.filter_by(share_token=token).first_or_404()
    if request.method == 'POST':
        ids = request.form.getlist('selected_photos')
        sel = Selection(galeria_id=g.id, photo_ids=','.join(ids), package_key=request.form.get('package_key'), status='received')
        db.session.add(sel); db.session.commit()
        try:
            owner = User.query.get(g.user_id)
            recipient = None
            if owner and owner.email:
                recipient = owner.email
            settings = AppSettings.query.first()
            if settings:
                if settings.notification_email:
                    recipient = settings.notification_email
                elif settings.smtp_user:
                    recipient = settings.smtp_user
            print(f'>>> EMAIL GALERIA: recipient={recipient}')
            if recipient:
                html = '<h2 style="color:#238636;">Nova selecao na galeria: ' + g.title + '</h2>'
                html += '<p>Um cliente acabou de selecionar fotos na galeria <strong>' + g.title + '</strong>.</p>'
                html += '<p>Fotos selecionadas: ' + str(len(ids)) + '</p>'
                html += '<p>Acesse o painel para ver as fotos selecionadas.</p>'
                result = send_notification_email('Nova selecao de fotos - ' + g.title, html, recipient)
                print(f'>>> EMAIL GALERIA result: {result}')
        except Exception as e:
            print(f'>>> EMAIL GALERIA ERRO: {e}')
        flash('Selecao enviada! O fotografo recebera sua escolha.', 'success')
        return render_template('cliente.html', galeria=g, photos=[], packages=[], submitted=True)
    photos = Photo.query.filter_by(galeria_id=g.id).all()
    return render_template('cliente.html', galeria=g, photos=photos, packages=[], submitted=False)
# ===== SELECOES =====
@app.route('/selecoes')
@login_required
def selecoes():
    ids = [g.id for g in Galeria.query.filter_by(user_id=current_user.id).all()]
    sels = Selection.query.filter(Selection.galeria_id.in_(ids)).order_by(Selection.created_at.desc()).all() if ids else []
    return render_template('selecoes.html', selections=sels)
@app.route('/selecoes/<int:sid>/download')
@login_required
def download_selection(sid):
    sel = Selection.query.get_or_404(sid); g = Galeria.query.get_or_404(sel.galeria_id)
    if g.user_id != current_user.id and not current_user.is_admin: abort(403)
    ids = [int(x) for x in sel.photo_ids.split(',') if x.strip().isdigit()]
    photos = Photo.query.filter(Photo.id.in_(ids)).all()
    mem = io.BytesIO()
    with zipfile.ZipFile(mem, 'w') as zf:
        for p in photos:
            try:
                data = download_bytes(p.filepath)
                tmp = os.path.join(UPLOAD_FOLDER, '_tmp_' + p.filepath)
                with open(tmp, 'wb') as f:
                    f.write(data)
                zf.write(tmp, p.filename or p.filepath)
                try: os.remove(tmp)
                except: pass
            except Exception:
                pass
    mem.seek(0)
    return send_file(mem, mimetype='application/zip', as_attachment=True, download_name=f'selecao_{sid}.zip')
# ===== PORTFOLIO =====
@app.route('/portfolio', methods=['GET', 'POST'])
@login_required
def portfolio():
    if request.method == 'POST':
        tok = secrets.token_urlsafe(32); before = request.files.get('before'); after = request.files.get('after')
        bn = an = None
        if before and allowed_file(before.filename):
            bn = secure_filename(f"pf_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{before.filename}")
            upload_bytes(before.read(), bn, before.content_type or 'image/jpeg')
        if after and allowed_file(after.filename):
            an = secure_filename(f"pf_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{after.filename}")
            upload_bytes(after.read(), an, after.content_type or 'image/jpeg')
        db.session.add(PortfolioPhoto(user_id=current_user.id, before_path=bn, after_path=an,
                     title=request.form.get('title', ''), share_token=tok)); db.session.commit()
        flash('Item adicionado!', 'success'); return redirect(url_for('portfolio'))
    items = PortfolioPhoto.query.filter_by(user_id=current_user.id).order_by(PortfolioPhoto.created_at.desc()).all()
    return render_template('portfolio.html', items=items)
@app.route('/portfolio/<int:iid>/delete', methods=['POST'])
@login_required
def delete_portfolio(iid):
    item = PortfolioPhoto.query.get_or_404(iid)
    if item.user_id != current_user.id: abort(403)
    for p in [item.before_path, item.after_path]:
        if p:
            try: delete_file(p)
            except: pass
    db.session.delete(item); db.session.commit()
    flash('Item removido.', 'success'); return redirect(url_for('portfolio'))
@app.route('/p/<token>')
def portfolio_public(token):
    item = PortfolioPhoto.query.filter_by(share_token=token).first()
    if not item:
        try:
            item = PortfolioPhoto.query.get_or_404(int(token))
        except (ValueError, TypeError):
            abort(404)
    return render_template('portfolio_public.html', item=item)
# ===== CATALOGO POSES =====
@app.route('/c/<token>')
def public_catalog(token):
    user = User.query.filter_by(catalog_token=token).first()
    if not user:
        abort(404)
    from sqlalchemy import func
    rows = db.session.query(
        PosePhoto.profession,
        func.count(PosePhoto.id).label('total')
    ).filter(
        PosePhoto.user_id == user.id
    ).filter(
        PosePhoto.profession.isnot(None)
    ).group_by(
        PosePhoto.profession
    ).order_by(
        PosePhoto.profession.asc()
    ).all()
    cat_list = []
    for cat in rows:
        first = PosePhoto.query.filter_by(
            user_id=user.id,
            profession=cat.profession
        ).filter(
            PosePhoto.filepath != 'pending'
        ).order_by(PosePhoto.id.asc()).first()
        cat_list.append({
            'profession': cat.profession,
            'total': cat.total,
            'first_photo': first.filepath if first else None
        })
    studio = user.studio_name if user.studio_name else 'Catalogo de Poses'
    return render_template('public_catalog.html', categorias=cat_list, token=token, studio_name=studio, category=None, poses=[])
@app.route('/c/<token>/<path:category>')
def public_catalog_cat(token, category):
    user = User.query.filter_by(catalog_token=token).first()
    if not user:
        abort(404)
    poses = PosePhoto.query.filter_by(
        user_id=user.id,
        profession=category
    ).order_by(PosePhoto.id.asc()).all()
    studio = user.studio_name if user.studio_name else 'Catalogo de Poses'
    return render_template('public_catalog.html', poses=poses, token=token, studio_name=studio, category=category, categorias=[])
@app.route('/m/<token>')
def poses_public(token):
    pose = PosePhoto.query.filter_by(share_token=token).first_or_404()
    related = PosePhoto.query.filter_by(user_id=pose.user_id, group_name=pose.group_name).all()
    return render_template('catalogo_poses.html', poses=related, public=True)
# ===== MARCA DAGUA =====
@app.route('/marca', methods=['GET', 'POST'])
@login_required
def marca():
    if request.method == 'POST':
        wm = Watermark.query.filter_by(user_id=current_user.id).first()
        if not wm: wm = Watermark(user_id=current_user.id); db.session.add(wm)
        wm.text = request.form.get('text', ''); wm.color = request.form.get('color', '#ffffff')
        wm.opacity = int(request.form.get('opacity', 30)); wm.position = request.form.get('position', 'diagonal')
        wm.stroke = request.form.get('stroke') == 'on'
        logo = request.files.get('logo')
        if logo and allowed_file(logo.filename):
            ln = secure_filename(f"wm_logo_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{logo.filename}")
            upload_bytes(logo.read(), ln, logo.content_type or 'image/png'); wm.logo_path = ln
        db.session.commit(); flash('Marca dagua salva!', 'success'); return redirect(url_for('marca'))
    return render_template('marca.html', wm=Watermark.query.filter_by(user_id=current_user.id).first())
# ===== PLANOS =====
@app.route('/planos')
def planos():
    return render_template('planos.html')
# ===== ADMIN =====
@app.route('/admin')
@login_required
def admin():
    users = User.query.order_by(User.created_at.desc()).all()
    stats = {
        'total': len(users),
        'active': sum(1 for u in users if hasattr(u, 'is_active') and u.is_active),
        'inactive': sum(1 for u in users if not (hasattr(u, 'is_active') and u.is_active)),
        'free': sum(1 for u in users if (u.plan if hasattr(u, 'plan') else 'FREE') == 'FREE'),
        'pro': sum(1 for u in users if (u.plan if hasattr(u, 'plan') else '') == 'PRO'),
        'premium': sum(1 for u in users if (u.plan if hasattr(u, 'plan') else '') == 'PREMIUM'),
    }
    return render_template('admin.html', users=users, stats=stats)
@app.route('/admin/settings', methods=['POST'])
@login_required
def admin_settings():
    if not current_user.is_admin: abort(403)
    s = AppSettings.query.first()
    if not s: s = AppSettings(); db.session.add(s)
    s.app_name = request.form.get('app_name', 'MeuFotoApp')
    s.primary_color = request.form.get('primary_color', '#4a90d9')
    s.smtp_host = request.form.get('smtp_host', '')
    s.smtp_port = int(request.form.get('smtp_port', 587)) if request.form.get('smtp_port') else None
    s.smtp_user = request.form.get('smtp_user', ''); s.smtp_password = request.form.get('smtp_password', '')
    db.session.commit(); flash('Configuracoes salvas!', 'success'); return redirect(url_for('admin'))
@app.route('/admin/categorias', methods=['POST'])
@login_required
def admin_categorias():
    if not current_user.is_admin: abort(403)
    flash('Gestao de categorias em manutencao.', 'error')
    return redirect(url_for('admin'))
@app.route('/admin/categorias/<int:cid>/delete', methods=['POST'])
@login_required
def delete_categoria(cid):
    if not current_user.is_admin: abort(403)
    flash('Gestao de categorias em manutencao.', 'error'); return redirect(url_for('admin'))
@app.route('/admin/pacotes', methods=['POST'])
@login_required
def admin_pacotes():
    if not current_user.is_admin: abort(403)
    flash('Gestao de pacotes em manutencao.', 'error')
    return redirect(url_for('admin'))
@app.route('/admin/pacotes/<int:pid>/delete', methods=['POST'])
@login_required
def delete_pacote(pid):
    if not current_user.is_admin: abort(403)
    flash('Gestao de pacotes em manutencao.', 'error'); return redirect(url_for('admin'))
# ===== CONFIGURACOES =====
@app.route('/configuracoes')
@login_required
def configuracoes():
    return render_template('configuracoes.html')
# ===== SEED =====
def seed_data():
    try:
        if not AppSettings.query.first():
            db.session.add(AppSettings(app_name='MeuFotoApp'))
            db.session.commit()
    except:
        db.session.rollback()
def public_portfolio_item(iid):
    item = PortfolioPhoto.query.get_or_404(iid)
    return render_template('public_portfolio.html', item=item)
@app.route('/extrair_prompt/<int:pid>', methods=['POST'])
@login_required
def extrair_prompt(pid):
    pose = PosePhoto.query.get_or_404(pid)
    settings = AppSettings.query.first()
    if not settings or not getattr(settings, 'openai_api_key', None):
        flash('Configure a OpenAI API Key no Admin > Catalogo primeiro', 'error')
        return redirect(url_for('catalogo_poses'))
    try:
        from PIL import Image
        data = download_bytes(pose.filepath)
        fp = os.path.join(UPLOAD_FOLDER, '_tmp_' + pose.filepath)
        with open(fp, 'wb') as f:
            f.write(data)
        img = Image.open(fp)
        if max(img.size) > 1024:
            ratio = 1024.0 / max(img.size)
            img = img.resize((int(img.width * ratio), int(img.height * ratio)))
        buf = io.BytesIO()
        img.save(buf, format='JPEG', quality=85)
        img_data = base64.b64encode(buf.getvalue()).decode('utf-8')
        payload = json.dumps({
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": [
                {"type": "text", "text": "Analyze this photo and generate a detailed prompt for AI image generation. Describe: pose, clothing, setting, lighting, expression, camera angle, and style. Write a single paragraph prompt ready to use in English."},
                {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + img_data}}
            ]}],
            "max_tokens": 500
        }).encode('utf-8')
        req = urllib.request.Request("https://api.openai.com/v1/chat/completions", data=payload, headers={"Authorization": "Bearer " + settings.openai_api_key, "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            prompt = result['choices'][0]['message']['content']
        pose.prompt = prompt
        db.session.commit()
        flash('Prompt extraido com IA!', 'success')
    except Exception as e:
        flash('Erro ao extrair: ' + str(e), 'error')
    return redirect(url_for('catalogo_poses'))
@app.route('/salvar_prompt/<int:pid>', methods=['POST'])
@login_required
def salvar_prompt(pid):
    pose = PosePhoto.query.get_or_404(pid)
    pose.prompt = request.form.get('prompt', '')
    db.session.commit()
    flash('Prompt salvo!', 'success')
    return redirect(url_for('catalogo_poses'))
@app.route('/admin/catalogo')
@login_required
def admin_catalogo():
    if not current_user.is_admin:
        abort(403)
    poses = PosePhoto.query.all()
    return render_template('admin_catalogo.html', poses=poses)
@app.route('/admin/catalogo/add', methods=['POST'])
@login_required
def admin_catalogo_add():
    if not current_user.is_admin:
        abort(403)
    if 'photo' not in request.files:
        flash('Selecione uma foto', 'error')
        return redirect(url_for('admin_catalogo'))
    f = request.files['photo']
    if f.filename:
        fn = secrets.token_urlsafe(8) + '_' + secure_filename(f.filename)
        upload_bytes(f.read(), fn, f.content_type or 'image/jpeg')
        pose = PosePhoto(filepath=fn, filename=f.filename, prompt=request.form.get('prompt', ''), profession=request.form.get('profession', ''), user_id=current_user.id)
        db.session.add(pose)
        db.session.commit()
        flash('Foto adicionada ao catalogo', 'success')
    return redirect(url_for('admin_catalogo'))
@app.route('/admin/catalogo/delete/<int:pid>', methods=['POST'])
@login_required
def admin_catalogo_delete(pid):
    if not current_user.is_admin:
        abort(403)
    pose = PosePhoto.query.get_or_404(pid)
    try:
        delete_file(pose.filepath)
    except:
        pass
    db.session.delete(pose)
    db.session.commit()
    flash('Foto removida', 'success')
    return redirect(url_for('admin_catalogo'))
@app.route('/admin/catalogo/prompt/<int:pid>', methods=['POST'])
@login_required
def admin_catalogo_prompt(pid):
    if not current_user.is_admin:
        abort(403)
    pose = PosePhoto.query.get_or_404(pid)
    pose.prompt = request.form.get('prompt', '')
    db.session.commit()
    flash('Prompt atualizado', 'success')
    return redirect(url_for('admin_catalogo'))
@app.route('/admin/catalogo/extrair/<int:pid>', methods=['POST'])
@login_required
def admin_catalogo_extrair(pid):
    if not current_user.is_admin:
        abort(403)
    pose = PosePhoto.query.get_or_404(pid)
    settings = AppSettings.query.first()
    if not settings or not getattr(settings, 'openai_api_key', None):
        flash('Configure a OpenAI API Key primeiro', 'error')
        return redirect(url_for('admin_catalogo'))
    try:
        from PIL import Image
        data = download_bytes(pose.filepath)
        fp = os.path.join(UPLOAD_FOLDER, '_tmp_' + pose.filepath)
        with open(fp, 'wb') as f:
            f.write(data)
        img = Image.open(fp)
        if max(img.size) > 1024:
            ratio = 1024.0 / max(img.size)
            img = img.resize((int(img.width * ratio), int(img.height * ratio)))
        buf = io.BytesIO()
        img.save(buf, format='JPEG', quality=85)
        img_data = base64.b64encode(buf.getvalue()).decode('utf-8')
        payload = json.dumps({
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": [
                {"type": "text", "text": "Analyze this photo and generate a detailed prompt for AI image generation. Describe: pose, clothing, setting, lighting, expression, camera angle, and style. Write a single paragraph prompt ready to use in English."},
                {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + img_data}}
            ]}],
            "max_tokens": 500
        }).encode('utf-8')
        req = urllib.request.Request("https://api.openai.com/v1/chat/completions", data=payload, headers={"Authorization": "Bearer " + settings.openai_api_key, "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            prompt = result['choices'][0]['message']['content']
        pose.prompt = prompt
        db.session.commit()
        flash('Prompt extraido com IA!', 'success')
    except Exception as e:
        flash('Erro: ' + str(e), 'error')
    return redirect(url_for('admin_catalogo'))
@app.route('/admin/apikey', methods=['POST'])
@login_required
def admin_apikey():
    if not current_user.is_admin:
        abort(403)
    settings = AppSettings.query.first()
    if not settings:
        settings = AppSettings()
        db.session.add(settings)
    settings.openai_api_key = request.form.get('openai_api_key', '')
    db.session.commit()
    flash('API Key salva', 'success')
    return redirect(url_for('admin_catalogo'))
# ===== ADICIONAR POSES DENTRO DE CATEGORIAS =====
@app.route('/admin/user/<int:uid>/make-admin', methods=['POST'])
@login_required
def admin_make_admin(uid):
    if not current_user.is_admin:
        abort(403)
    user = User.query.get_or_404(uid)
    user.is_admin = not user.is_admin
    db.session.commit()
    flash('Permissao de admin alterada.', 'success')
    return redirect(url_for('admin'))
@app.route('/admin/user/<int:uid>/delete', methods=['POST'])
@login_required
def admin_delete_user(uid):
    if not current_user.is_admin:
        abort(403)
    if uid == current_user.id:
        flash('Voce nao pode deletar a si mesmo.', 'error')
        return redirect(url_for('admin'))
    user = User.query.get_or_404(uid)
    galerias = Galeria.query.filter_by(user_id=uid).all()
    for g in galerias:
        Photo.query.filter_by(galeria_id=g.id).delete()
        Selection.query.filter_by(galeria_id=g.id).delete()
    Galeria.query.filter_by(user_id=uid).delete()
    PortfolioPhoto.query.filter_by(user_id=uid).delete()
    Watermark.query.filter_by(user_id=uid).delete()
    db.session.delete(user)
    db.session.commit()
    flash('Usuario deletado.', 'success')
    return redirect(url_for('admin'))
# ===== NOVA CATEGORIA DE POSES =====
# ===== CATALOGO DE POSES (LIMPO) =====
@app.route('/catalogo-poses')
@login_required
def catalogo_poses():
    from sqlalchemy import distinct, or_
    cats_cat = db.session.query(distinct(PosePhoto.category)).filter_by(user_id=current_user.id).all()
    cats_prof = db.session.query(distinct(PosePhoto.profession)).filter_by(user_id=current_user.id).all()
    todas_cats = set()
    for c in cats_cat:
        if c[0]:
            todas_cats.add(c[0])
    for c in cats_prof:
        if c[0]:
            todas_cats.add(c[0])
    categorias = sorted(list(todas_cats))
    cat_info = []
    for cat in categorias:
        count = PosePhoto.query.filter_by(user_id=current_user.id).filter(
            or_(PosePhoto.category == cat, PosePhoto.profession == cat)
        ).count()
        thumb = PosePhoto.query.filter_by(user_id=current_user.id).filter(
            or_(PosePhoto.category == cat, PosePhoto.profession == cat)
        ).filter(PosePhoto.filepath.isnot(None)).first()
        cat_info.append({'nome': cat, 'count': count, 'thumb': thumb.filepath if thumb else None})
    return render_template('catalogo_poses.html', categorias=cat_info)
@app.route('/catalogo-poses/nova-categoria', methods=['POST'])
@login_required
def nova_categoria_pose():
    nome = request.form.get('nome_categoria', '').strip()
    if not nome:
        flash('Digite um nome para a categoria.', 'error')
        return redirect(url_for('catalogo_poses'))
    from sqlalchemy import or_
    existente = PosePhoto.query.filter(
        or_(PosePhoto.category == nome, PosePhoto.profession == nome)
    ).filter_by(user_id=current_user.id).first()
    if existente:
        flash('Esta categoria ja existe!', 'error')
        return redirect(url_for('catalogo_poses'))
    try:
        pose = PosePhoto(
            user_id=current_user.id,
            category=nome,
            profession=nome if hasattr(PosePhoto, 'profession') else None,
            prompt='Nova categoria - adicione poses aqui',
            filepath='placeholder_new_category.png',
            share_token=secrets.token_hex(16)
        )
        db.session.add(pose)
        db.session.commit()
        flash(f'Categoria "{nome}" criada com sucesso!', 'success')
        return redirect(url_for('catalogo_categoria', category=nome))
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao criar categoria: {str(e)}', 'error')
        return redirect(url_for('catalogo_poses'))
@app.route('/catalogo-poses/<path:category>')
@login_required
def catalogo_categoria(category):
    from urllib.parse import unquote
    from sqlalchemy import or_
    category = unquote(category)
    poses = PosePhoto.query.filter_by(user_id=current_user.id).filter(
        or_(PosePhoto.category == category, PosePhoto.profession == category)
    ).order_by(PosePhoto.id.asc()).all()
    return render_template('catalogo_categoria.html', poses=poses, category=category)
@app.route('/catalogo-poses/<path:category>/add', methods=['GET', 'POST'])
@login_required
def add_pose(category):
    from urllib.parse import unquote
    from sqlalchemy import or_
    category = unquote(category)
    if request.method == 'POST':
        prompt_text = request.form.get('prompt', '')
        photo_file = request.files.get('photo')
        filepath = 'placeholder_new_category.png'
        if photo_file and photo_file.filename:
            ext = photo_file.filename.rsplit('.', 1)[-1].lower() if '.' in photo_file.filename else 'jpg'
            fn = f"pose_{secrets.token_hex(8)}.{ext}"
            upload_bytes(photo_file.read(), fn, photo_file.content_type or 'image/jpeg')
            filepath = fn
        pose = PosePhoto(
            user_id=current_user.id,
            category=category,
            profession=category if hasattr(PosePhoto, 'profession') else None,
            prompt=prompt_text,
            filepath=filepath,
            share_token=secrets.token_hex(16)
        )
        db.session.add(pose)
        db.session.commit()
        flash('Pose adicionada com sucesso!', 'success')
        return redirect(url_for('catalogo_categoria', category=category))
    return redirect(url_for('catalogo_categoria', category=category))
@app.route('/catalogo-poses/<path:category>/pose/<int:pid>/delete', methods=['POST'])
@login_required
def delete_pose(category, pid):
    from urllib.parse import unquote
    category = unquote(category)
    pose = PosePhoto.query.get_or_404(pid)
    if pose.user_id != current_user.id:
        abort(403)
    db.session.delete(pose)
    db.session.commit()
    flash('Pose removida.', 'success')
    return redirect(url_for('catalogo_categoria', category=category))
# ===== ADMIN ACTIONS =====
@app.route('/admin/user/<int:uid>/plan', methods=['POST'])
@login_required
def admin_change_plan(uid):
    if not current_user.is_admin:
        abort(403)
    user = User.query.get_or_404(uid)
    novo_plano = request.form.get('plano', 'free')
    if novo_plano in ['free', 'pro', 'premium']:
        user.plan = novo_plano.upper()
        db.session.commit()
        flash(f'Plano alterado para {novo_plano.upper()}.', 'success')
    else:
        flash('Plano invalido.', 'error')
    return redirect(url_for('admin'))
@app.route('/admin/user/<int:uid>/toggle-block', methods=['POST'])
@login_required
def admin_toggle_block(uid):
    if not current_user.is_admin:
        abort(403)
    user = User.query.get_or_404(uid)
    if user.id == current_user.id:
        flash('Voce nao pode bloquear a si mesmo.', 'error')
        return redirect(url_for('admin'))
    user.active = not user.active
    db.session.commit()
    estado = 'ATIVO' if user.active else 'BLOQUEADO'
    flash(f'Usuario {estado}.', 'success')
    return redirect(url_for('admin'))
# ===== UPLOAD DE FOTO PARA POSE EXISTENTE =====
@app.route('/catalogo-poses/<path:category>/<int:pid>/upload-photo', methods=['POST'])
@login_required
def upload_pose_photo(category, pid):
    from urllib.parse import unquote
    from sqlalchemy import or_
    category = unquote(category)
    pose = PosePhoto.query.filter_by(id=pid, user_id=current_user.id).first_or_404()
    photo_file = request.files.get('photo')
    if photo_file and photo_file.filename:
        ext = photo_file.filename.rsplit('.', 1)[-1].lower() if '.' in photo_file.filename else 'jpg'
        fn = f"pose_{secrets.token_hex(8)}.{ext}"
        upload_bytes(photo_file.read(), fn, photo_file.content_type or 'image/jpeg')
        pose.filepath = fn
        db.session.commit()
        flash('Foto anexada a pose com sucesso!', 'success')
    else:
        flash('Nenhum arquivo selecionado.', 'error')
    return redirect(url_for('catalogo_categoria', category=category))
# ===== RENOMEAR CATEGORIA =====
@app.route('/catalogo-poses/<path:category>/rename', methods=['POST'])
@login_required
def rename_category(category):
    from urllib.parse import unquote
    from sqlalchemy import or_
    category = unquote(category)
    new_name = request.form.get('new_name', '').strip()
    if not new_name:
        flash('Nome invalido.', 'error')
        return redirect(url_for('catalogo_categoria', category=category))
    poses = PosePhoto.query.filter(
        or_(PosePhoto.category == category, PosePhoto.profession == category)
    ).all()
    for p in poses:
        if p.category == category:
            p.category = new_name
        if p.profession == category:
            p.profession = new_name
    db.session.commit()
    flash('Categoria renomeada!', 'success')
    return redirect(url_for('catalogo_categoria', category=new_name))
# ===== SALVAR NOME DO APP =====
@app.route('/configuracoes/app-name', methods=['POST'])
@login_required
def save_app_name():
    app_name_val = request.form.get('app_name', '').strip()
    if app_name_val:
        settings = AppSettings.query.first()
        if not settings:
            settings = AppSettings()
            db.session.add(settings)
        settings.app_name = app_name_val
        db.session.commit()
        flash('Nome do app atualizado!', 'success')
    return redirect(url_for('configuracoes'))
# ===== CATALOGO PUBLICO (SEM LOGIN) =====
@app.route('/catalogo-publico/<path:category>')
def catalogo_publico(category):
    from urllib.parse import unquote
    from sqlalchemy import or_
    category = unquote(category)
    poses = PosePhoto.query.filter(
        or_(PosePhoto.category == category, PosePhoto.profession == category)
    ).order_by(PosePhoto.id.asc()).all()
    return render_template('public_catalog.html', poses=poses, category=category)
# ===== SELECAO DE POSES PELO CLIENTE =====
@app.route('/catalogo-publico/<path:category>/selecionar', methods=['POST'])
def public_catalog_selecionar(category):
    from urllib.parse import unquote
    category = unquote(category)
    sel = PoseSelection()
    sel.category = category
    sel.client_name = request.form.get('client_name', '')
    sel.client_email = request.form.get('client_email', '')
    sel.selected_poses = request.form.get('selected_poses', '')
    sel.message = request.form.get('message', '')
    db.session.add(sel)
    db.session.commit()
    pose_ids = [int(x) for x in sel.selected_poses.split(',') if x.strip().isdigit()]
    selected_poses = PosePhoto.query.filter(PosePhoto.id.in_(pose_ids)).all() if pose_ids else []
    settings = AppSettings.query.first()
    recipient = None
    if settings:
        recipient = settings.notification_email or settings.smtp_user
    print(f'>>> EMAIL: recipient={recipient}, settings.smtp_user={getattr(settings, "smtp_user", None)}, settings.notification_email={getattr(settings, "notification_email", None)}')
    if recipient:
        try:
            html = f'<h2 style="color:#238636;">Nova selecao de poses - {category}</h2>'
            html += f'<p><strong>Cliente:</strong> {sel.client_name}</p>'
            html += f'<p><strong>E-mail:</strong> {sel.client_email}</p>'
            if sel.message:
                html += f'<p><strong>Mensagem:</strong> {sel.message}</p>'
            html += f'<p><strong>Poses selecionadas:</strong> {len(pose_ids)} foto(s)</p>'
            html += f'<p>ID da selecao: #{sel.id}</p>'
            html += f'<p>Acesse o painel para ver as poses selecionadas.</p>'
            result = send_notification_email('Nova selecao de poses - ' + category, html, recipient)
            print(f'>>> EMAIL result: {result}')
        except Exception as e:
            print(f'>>> EMAIL ERRO: {e}')
    else:
        print('>>> EMAIL: Nenhum destinatario configurado!')
    return render_template('public_catalog.html', category=category, poses=PosePhoto.query.filter_by(category=category).all(), selection_sent=True, site_settings=settings)
@app.route('/selecoes-poses')
@login_required
def selecoes_poses():
    selections = PoseSelection.query.order_by(PoseSelection.created_at.desc()).all()
    for sel in selections:
        pose_ids = [int(x) for x in sel.selected_poses.split(',') if x.strip().isdigit()]
        sel.poses = PosePhoto.query.filter(PosePhoto.id.in_(pose_ids)).all() if pose_ids else []
    return render_template('selecoes_poses.html', selections=selections)
# ===== BLOQUEAR/DESBLOQUEAR USUARIO =====
@app.route('/admin/usuario/<int:user_id>/bloquear', methods=['POST'])
@login_required
def bloquear_usuario(user_id):
    user = User.query.get_or_404(user_id)
    user.active = not user.active
    db.session.commit()
    flash('Usuario {} com sucesso!'.format('bloqueado' if not user.active else 'desbloqueado'), 'success')
    return redirect(url_for('admin'))
# ===== ALTERAR PLANO DO USUARIO =====
@app.route('/admin/usuario/<int:user_id>/plano', methods=['POST'])
@login_required
def alterar_plano_usuario(user_id):
    user = User.query.get_or_404(user_id)
    user.plan = request.form.get('plan', 'FREE')
    db.session.commit()
    flash('Plano do usuario atualizado!', 'success')
    return redirect(url_for('admin'))
# ===== SALVAR CONFIG DE EMAIL =====
@app.route('/configuracoes/email', methods=['POST'])
@login_required
def save_email_config():
    settings = AppSettings.query.first()
    if not settings:
        settings = AppSettings()
        db.session.add(settings)
    settings.smtp_user = request.form.get('smtp_user', '').strip()
    settings.notification_email = request.form.get('smtp_user', '').strip()
    settings.smtp_host = request.form.get('smtp_host', '').strip()
    settings.smtp_server = request.form.get('smtp_host', '').strip()
    smtp_port_str = request.form.get('smtp_port', '587').strip()
    try:
        settings.smtp_port = int(smtp_port_str) if smtp_port_str else 587
    except ValueError:
        settings.smtp_port = 587
    settings.smtp_password = request.form.get('smtp_password', '').strip()
    db.session.commit()
    flash('Configuracoes de email salvas!', 'success')
    return redirect(url_for('configuracoes'))
# ===== DELETAR SELECAO =====
@app.route('/selecao/<int:sid>/deletar', methods=['POST'])
@login_required
def deletar_selecao(sid):
    from models import Selection
    sel = Selection.query.get_or_404(sid)
    db.session.delete(sel)
    db.session.commit()
    flash('Selecao deletada!', 'success')
    return redirect(request.referrer or url_for('galeria', gid=sel.galeria_id))
@app.route('/selecao-pose/<int:sid>/deletar', methods=['POST'])
@login_required
def deletar_selecao_pose(sid):
    sel = PoseSelection.query.get_or_404(sid)
    db.session.delete(sel)
    db.session.commit()
    flash('Selecao de poses deletada!', 'success')
    return redirect(request.referrer or url_for('selecoes_poses'))
@app.route('/landing')
def landing():
    return render_template('landing.html')
# ===== CORRECAO: cria as tabelas automaticamente ao iniciar (funciona no Render) =====
with app.app_context():
    db.create_all()
if __name__ == '__main__':
    app.run(debug=False)