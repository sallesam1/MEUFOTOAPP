import os
import zipfile
from datetime import datetime

base = os.path.dirname(os.path.abspath(__file__))
data = datetime.now().strftime('%Y-%m-%d_%H%M')
zip_nome = f'BACKUP_MeuFotoApp_{data}.zip'

# Salvar na pasta PAI do projeto (OneDrive/Desktop)
zip_path = os.path.join(os.path.dirname(base), zip_nome)

ignorar = {'__pycache__', 'venv', '.git', 'node_modules'}
ext_ignorar = {'.pyc', '.pyo', '.log'}

total = 0
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for raiz, dirs, arquivos in os.walk(base):
        dirs[:] = [d for d in dirs if d not in ignorar]
        for arq in arquivos:
            ext = os.path.splitext(arq)[1].lower()
            if ext in ext_ignorar or arq.startswith('BACKUP_'):
                continue
            completo = os.path.join(raiz, arq)
            relativo = os.path.relpath(completo, base)
            zf.write(completo, relativo)
            total += 1

tamanho = os.path.getsize(zip_path) / (1024 * 1024)
print(f"BACKUP CRIADO!")
print(f"Arquivo: {zip_nome}")
print(f"Local: {zip_path}")
print(f"Arquivos: {total}")
print(f"Tamanho: {tamanho:.1f} MB")