import os

app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.py')

with open(app_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Procurar a linha com "db.session.add(sel); db.session.commit()"
start = None
for i, line in enumerate(lines):
    if 'db.session.add(sel); db.session.commit()' in line:
        start = i
        break

if start is None:
    print('ERRO: nao achei db.session.add(sel)')
    exit()

# Procurar o "flash('Selecao enviada" depois dessa linha
end = None
for i in range(start+1, min(start+30, len(lines))):
    if 'Selecao enviada' in lines[i] or 'Seleção enviada' in lines[i]:
        end = i
        break

if end is None:
    print('ERRO: nao achei flash Selecao enviada')
    exit()

print(f'Substituindo linhas {start+1} ate {end+1}')
for i in range(start, end+1):
    print(f'  {i+1}: {lines[i].rstrip()}')

# Novo bloco com indentacao correta (8 espacos)
new_block = [
    "        db.session.add(sel); db.session.commit()\n",
    "        \n",
    "        # Enviar email de notificacao\n",
    "        try:\n",
    "            settings = AppSettings.query.first()\n",
    "            recipient = None\n",
    "            if settings:\n",
    "                recipient = settings.notification_email or settings.smtp_user\n",
    "            if not recipient:\n",
    "                owner = User.query.get(g.user_id)\n",
    "                if owner and owner.email:\n",
    "                    recipient = owner.email\n",
    "            print(f'>>> EMAIL GALERIA: recipient={recipient}')\n",
    "            if recipient:\n",
    "                html = '<h2 style=\"color:#238636;\">Nova selecao na galeria: ' + g.title + '</h2>'\n",
    "                html += '<p>Um cliente acabou de selecionar fotos na galeria <strong>' + g.title + '</strong>.</p>'\n",
    "                html += '<p>Fotos selecionadas: ' + str(len(ids)) + '</p>'\n",
    "                html += '<p>Acesse o painel para ver as fotos selecionadas.</p>'\n",
    "                result = send_notification_email('Nova selecao de fotos - ' + g.title, html, recipient)\n",
    "                print(f'>>> EMAIL GALERIA result: {result}')\n",
    "        except Exception as e:\n",
    "            print(f'>>> EMAIL GALERIA ERRO: {e}')\n",
    "        \n",
    "        flash('Selecao enviada! O fotografo recebera sua escolha.', 'success')\n",
]

# Substituir as linhas
lines = lines[:start] + new_block + lines[end+1:]

with open(app_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('\nOK: Bloco de email corrigido com indentacao correta')
print('PRONTO! Rode: python app.py')