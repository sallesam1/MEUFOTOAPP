import os
import shutil

base = os.path.dirname(os.path.abspath(__file__))

# ===== 1. Cria o ajudante que fala com o Supabase =====
helper = '''import os
from supabase import create_client
from supabase_config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_BUCKET

_cliente = None

def get_client():
    global _cliente
    if _cliente is None:
        _cliente = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _cliente

def upload_bytes(data, filename, content_type="image/jpeg"):
    cliente = get_client()
    cliente.storage.from_(SUPABASE_BUCKET).upload(
        filename, data, {"content-type": content_type}
    )
    return filename

def download_bytes(filename):
    cliente = get_client()
    return cliente.storage.from_(SUPABASE_BUCKET).download(filename)

def get_public_url(filename):
    return f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{filename}"

def delete_file(filename):
    try:
        cliente = get_client()
        cliente.storage.from_(SUPABASE_BUCKET).remove([filename])
    except Exception:
        pass
'''
with open(os.path.join(base, 'supabase_storage.py'), 'w', encoding='utf-8') as f:
    f.write(helper)
print("OK: supabase_storage.py criado.")

# ===== 2. Backup do app.py =====
app_path = os.path.join(base, 'app.py')
backup_path = app_path + '.backup'
shutil.copy2(app_path, backup_path)
print("OK: backup salvo em app.py.backup")

# ===== 3. Aplica as mudancas no app.py =====
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Import do ajudante
content = content.replace(
    "from social_sizes import resize_for_social, SOCIAL_SIZES",
    "from social_sizes import resize_for_social, SOCIAL_SIZES\nfrom supabase_storage import upload_bytes, get_public_url, delete_file, download_bytes",
    1)

# Salvar fotos: troca de pasta local -> nuvem (todas as ocorrencias)
content = content.replace(
    "f.save(os.path.join(UPLOAD_FOLDER, fn))",
    "upload_bytes(f.read(), fn, f.content_type or 'image/jpeg')")
content = content.replace(
    "photo_file.save(os.path.join(UPLOAD_FOLDER, fn))",
    "upload_bytes(photo_file.read(), fn, photo_file.content_type or 'image/jpeg')")
content = content.replace(
    "before.save(os.path.join(UPLOAD_FOLDER, bn))",
    "upload_bytes(before.read(), bn, before.content_type or 'image/jpeg')", 1)
content = content.replace(
    "after.save(os.path.join(UPLOAD_FOLDER, an))",
    "upload_bytes(after.read(), an, after.content_type or 'image/jpeg')", 1)
content = content.replace(
    "logo.save(os.path.join(UPLOAD_FOLDER, ln))",
    "upload_bytes(logo.read(), ln, logo.content_type or 'image/png')", 1)

# Servir fotos: em vez de ler da pasta, redireciona para a URL publica da nuvem
content = content.replace(
    """@app.route('/uploads/<filename>')
def serve_upload(filename):
    if filename == 'pending':
        abort(404)
    return send_from_directory(UPLOAD_FOLDER, filename)""",
    """@app.route('/uploads/<filename>')
def serve_upload(filename):
    if filename == 'pending':
        abort(404)
    return redirect(get_public_url(filename))""", 1)

# Marca dagua: baixa da nuvem, aplica, e mostra
content = content.replace(
    """            fp = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.exists(fp):
                try:
                    img_bytes = get_watermarked_bytes(
                        fp,
                        wm.text or 'MeuFotoApp',
                        wm.color or '#ffffff',
                        wm.opacity or 30,
                        'diagonal',
                        wm.stroke,
                        wm.logo_path
                    )
                    return send_file(img_bytes, mimetype='image/jpeg')
                except Exception as e:
                    print('WM error: ' + str(e))""",
    """            try:
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
                print('WM error: ' + str(e))""", 1)

# Melhorar foto: baixa, melhora, sobe de volta
content = content.replace(
    "        enhance_image(os.path.join(UPLOAD_FOLDER, p.filepath)); p.enhanced = True; db.session.commit()",
    "        data = download_bytes(p.filepath)\n        tmp = os.path.join(UPLOAD_FOLDER, '_tmp_' + p.filepath)\n        with open(tmp, 'wb') as f:\n            f.write(data)\n        enhance_image(tmp)\n        with open(tmp, 'rb') as f:\n            upload_bytes(f.read(), p.filepath, 'image/jpeg')\n        try: os.remove(tmp)\n        except: pass\n        p.enhanced = True; db.session.commit()", 1)

# Redimensionar: baixa, redimensiona, mostra
content = content.replace(
    "    out = resize_for_social(os.path.join(UPLOAD_FOLDER, p.filepath), platform)\n    if out: return send_file(out, as_attachment=True)",
    "    data = download_bytes(p.filepath)\n    tmp = os.path.join(UPLOAD_FOLDER, '_tmp_' + p.filepath)\n    with open(tmp, 'wb') as f:\n        f.write(data)\n    out = resize_for_social(tmp, platform)\n    try: os.remove(tmp)\n    except: pass\n    if out: return send_file(out, as_attachment=True)", 1)

# Reaplicar marca dagua: baixa, aplica, sobe de volta
content = content.replace(
    "            apply_watermark(os.path.join(UPLOAD_FOLDER, p.filepath), wm.text or 'MeuFotoApp', wm.color, wm.opacity, 'diagonal', wm.stroke, wm.logo_path)\n            p.has_watermark = True; db.session.commit()",
    "            data = download_bytes(p.filepath)\n            tmp = os.path.join(UPLOAD_FOLDER, '_tmp_' + p.filepath)\n            with open(tmp, 'wb') as f:\n                f.write(data)\n            apply_watermark(tmp, wm.text or 'MeuFotoApp', wm.color, wm.opacity, 'diagonal', wm.stroke, wm.logo_path)\n            with open(tmp, 'rb') as f:\n                upload_bytes(f.read(), p.filepath, 'image/jpeg')\n            try: os.remove(tmp)\n            except: pass\n            p.has_watermark = True; db.session.commit()", 1)

# Baixar selecao (zip): baixa cada foto da nuvem
content = content.replace(
    "        for p in photos:\n            fp = os.path.join(UPLOAD_FOLDER, p.filepath)\n            if os.path.exists(fp): zf.write(fp, p.filename or p.filepath)",
    "        for p in photos:\n            try:\n                data = download_bytes(p.filepath)\n                tmp = os.path.join(UPLOAD_FOLDER, '_tmp_' + p.filepath)\n                with open(tmp, 'wb') as f:\n                    f.write(data)\n                zf.write(tmp, p.filename or p.filepath)\n                try: os.remove(tmp)\n                except: pass\n            except Exception:\n                pass", 1)

# Apagar fotos: apaga da nuvem
content = content.replace(
    "    for p in Photo.query.filter_by(galeria_id=g.id).all():\n        try: os.remove(os.path.join(UPLOAD_FOLDER, p.filepath))\n        except: pass\n        db.session.delete(p)",
    "    for p in Photo.query.filter_by(galeria_id=g.id).all():\n        try: delete_file(p.filepath)\n        except: pass\n        db.session.delete(p)", 1)
content = content.replace(
    "    try: os.remove(os.path.join(UPLOAD_FOLDER, p.filepath))\n    except: pass\n    db.session.delete(p); db.session.commit()",
    "    try: delete_file(p.filepath)\n    except: pass\n    db.session.delete(p); db.session.commit()", 1)
content = content.replace(
    "    for p in [item.before_path, item.after_path]:\n        if p:\n            try: os.remove(os.path.join(UPLOAD_FOLDER, p))\n            except: pass",
    "    for p in [item.before_path, item.after_path]:\n        if p:\n            try: delete_file(p)\n            except: pass", 1)
content = content.replace(
    "    try:\n        os.remove(os.path.join(UPLOAD_FOLDER, pose.filepath))\n    except:\n        pass",
    "    try:\n        delete_file(pose.filepath)\n    except:\n        pass", 1)

# Extrair prompt (IA): baixa a foto da nuvem primeiro
content = content.replace(
    "        from PIL import Image\n        fp = os.path.join(UPLOAD_FOLDER, pose.filepath)\n        img = Image.open(fp)",
    "        from PIL import Image\n        data = download_bytes(pose.filepath)\n        fp = os.path.join(UPLOAD_FOLDER, '_tmp_' + pose.filepath)\n        with open(fp, 'wb') as f:\n            f.write(data)\n        img = Image.open(fp)")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("PRONTO! app.py atualizado para usar o Supabase.")
print("Backup do original salvo em: app.py.backup")