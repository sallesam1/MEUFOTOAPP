import os

app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.py')

with open(app_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Remover o > que foi colocado antes do @app.route
code = code.replace("> @app.route('/wm/<filename>')", "@app.route('/wm/<filename>')")
code = code.replace(">@app.route('/wm/<filename>')", "@app.route('/wm/<filename>')")
print('OK: > removido')

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(code)

# Criar fix_db.py limpo
db_script = """from app import app, db, Watermark
app.app_context().push()
wms = Watermark.query.all()
for w in wms:
    w.position = 'diagonal'
db.session.commit()
print('BD: ' + str(len(wms)) + ' registro(s) atualizado(s) para diagonal')
"""
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fix_db.py')
with open(db_path, 'w', encoding='utf-8') as f:
    f.write(db_script)
print('OK: fix_db.py criado')