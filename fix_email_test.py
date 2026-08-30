import os, re

base_dir = os.path.dirname(os.path.abspath(__file__))
app_path = os.path.join(base_dir, 'app.py')
changes = []

# ========== 1. CORRIGIR BANCO ==========
from app import app, db
from models import AppSettings
from sqlalchemy import text

with app.app_context():
    engine = db.engine
    with engine.connect() as conn:
        # Setar smtp_host e smtp_port diretamente
        conn.execute(text("UPDATE app_settings SET smtp_host = 'smtp.gmail.com' WHERE smtp_host IS NULL OR smtp_host = ''"))
        conn.execute(text("UPDATE app_settings SET smtp_port = 587 WHERE smtp_port IS NULL"))
        conn.execute(text("UPDATE app_settings SET notification_email = smtp_user WHERE notification_email IS NULL OR notification_email = ''"))
        conn.execute(text("UPDATE app_settings SET smtp_server = 'smtp.gmail.com' WHERE smtp_server IS NULL OR smtp_server = ''"))
        conn.commit()
        changes.append('Banco: smtp_host, smtp_port e notification_email corrigidos')

    # Verificar
    s = AppSettings.query.first()
    print(f'  smtp_user: {s.smtp_user}')
    print(f'  smtp_host: {s.smtp_host}')
    print(f'  smtp_port: {s.smtp_port}')
    print(f'  smtp_password: {"configurado" if s.smtp_password else "VAZIO"}')
    print(f'  notification_email: {s.notification_email}')

# ========== 2. VERIFICAR ROTA DE SELECAO ==========
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Procurar a rota public_catalog_selecionar
selecionar_match = re.search(r"def public_catalog_selecar.*?\n(?=\n@app\.route|\nif __name__|\Z)", content, re.DOTALL)
if not selecionar_match:
    selecionar_match = re.search(r"def public_catalog_sele.*?\n(?=\n@app\.route|\nif __name__|\Z)", content, re.DOTALL)

if selecionar_match:
    func_code = selecionar_match.group(0)
    if 'send_notification_email' in func_code:
        changes.append('Rota de selecao: chama send_notification_email OK')
    else:
        changes.append('AVISO: Rota de selecao NAO chama send_notification_email!')
        # Vou ver o que a rota faz
        print(f'\n=== ROTA SELECAO ===\n{func_code[:500]}')
else:
    changes.append('AVISO: Rota public_catalog_selecionar nao encontrada')
    # Procurar todas as rotas com 'selecionar' ou 'selecao'
    for m in re.finditer(r"def \w*sele\w*.*", content):
        print(f'Rota encontrada: {m.group(0)}')

# ========== 3. TESTAR ENVIO DE EMAIL ==========
print('\n=== TESTE DE ENVIO ===')
try:
    from app import send_notification_email
    html = '<h2>TESTE MeuFotoApp</h2><p>Este e um email de teste do sistema de notificacoes.</p>'
    result = send_notification_email(
        'TESTE: Notificacao MeuFotoApp',
        html,
        'amssolucoesia@gmail.com'
    )
    if result:
        changes.append('TESTE: Email enviado com sucesso!')
    else:
        changes.append('TESTE: Falha no envio do email')
except Exception as e:
    changes.append(f'ERRO no teste: {e}')
    # Tentar chamar diretamente
    print(f'Erro: {e}')

# ========== RESULTADO ==========
print('\n' + '=' * 50)
for c in changes:
    print('OK: ' + c)
print('=' * 50)