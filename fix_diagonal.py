import os

base = os.path.dirname(os.path.abspath(__file__))
app_path = os.path.join(base, 'app.py')

# Corrigir app.py
with open(app_path, 'r', encoding='utf-8') as f:
    code = f.read()

if "wm.position" in code:
    code = code.replace("wm.position", "'diagonal'")
    print('OK: wm.position -> diagonal no app.py')

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(code)

# Atualizar banco de dados
exec(open(os.path.join(base, 'fix_db.py'), 'w').write("""
from app import app, db, Watermark
app.app_context().push()
wms = Watermark.query.all()
for w in wms:
    w.position = 'diagonal'
db.session.commit()
print('BD: diagonal forcado em ' + str(len(wms)) + ' registros')
""") or '')

# Criar arquivo separado para rodar no banco
db_script = """from app import app, db, Watermark
app.app_context().push()
wms = Watermark.query.all()
for w in wms:
    w.position = 'diagonal'
db.session.commit()
print('BD: diagonal forcado em ' + str(len(wms)) + ' registros')
"""
db_path = os.path.join(base, 'fix_db.py')
with open(db_path, 'w', encoding='utf-8') as f:
    f.write(db_script)

print('OK: fix_db.py criado')
print('\n=== RODE AGORA: python fix_db.py ===')