import os

base = os.path.dirname(os.path.abspath(__file__))
app_path = os.path.join(base, 'app.py')

with open(app_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Corrigir linha quebrada se existir
code = code.replace(
    "'diagonal' = request.form.get('position', 'diagonal')",
    "wm.position = request.form.get('position', 'diagonal')"
)
print('OK: linha de salvamento corrigida')

# 2. Reescrever serve_wm inteiro - SEMPRE diagonal
start_marker = "@app.route('/wm/<filename>')"
end_marker = "\n@app.route"

start = code.find(start_marker)
if start >= 0:
    end = code.find(end_marker, start + 10)
    if end < 0:
        end = code.find("\nif __name__", start)
    if end < 0:
        end = len(code)
    
    new_wm = """> @app.route('/wm/<filename>')
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
                    print('WM error: ' + str(e))
    return send_file(os.path.join(UPLOAD_FOLDER, filename))"""
    
    code = code[:start] + new_wm + code[end:]
    print('OK: serve_wm reescrito (sempre diagonal)')
else:
    print('ERRO: serve_wm nao encontrado')

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(code)

# 3. Script para atualizar banco
db_script = """from app import app, db, Watermark
app.app_context().push()
wms = Watermark.query.all()
for w in wms:
    w.position = 'diagonal'
db.session.commit()
print('BD: ' + str(len(wms)) + ' registro(s) atualizado(s) para diagonal')
"""
with open(os.path.join(base, 'fix_db.py'), 'w', encoding='utf-8') as f:
    f.write(db_script)
print('OK: fix_db.py criado')

print('\n=== RODE: python fix_db.py && python app.py ===')