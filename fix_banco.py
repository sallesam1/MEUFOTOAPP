import sqlite3, os

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fotografia.db')
if not os.path.exists(db_path):
    # Procurar o banco
    for f in os.listdir(os.path.dirname(os.path.abspath(__file__))):
        if f.endswith('.db'):
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f)
            break

print(f'Banco: {db_path}')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Listar colunas atuais
cursor.execute("PRAGMA table_info(app_settings)")
cols = [row[1] for row in cursor.fetchall()]
print(f'Colunas atuais: {cols}')

changes = []

# Adicionar colunas que faltam
new_cols = [
    ('notification_email', 'VARCHAR(180)'),
    ('smtp_server', 'VARCHAR(200)'),
    ('smtp_port', 'INTEGER'),
    ('smtp_password', 'VARCHAR(200)'),
]

for col_name, col_type in new_cols:
    if col_name not in cols:
        cursor.execute(f"ALTER TABLE app_settings ADD COLUMN {col_name} {col_type}")
        changes.append(f'Coluna {col_name} adicionada')
    else:
        changes.append(f'Coluna {col_name} ja existe')

conn.commit()
conn.close()

print('=' * 50)
for c in changes:
    print('OK: ' + c)
print('=' * 50)
print('\nPRONTO! Rode: python app.py')