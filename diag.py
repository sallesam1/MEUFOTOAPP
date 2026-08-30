import os
from flask import Flask

app = Flask(__name__)
print("PASTA RAIZ DO APP:", app.root_path)
print("PASTA STATIC:", os.path.join(app.root_path, 'static'))
print("PASTA ANTES-DEPOIS:", os.path.join(app.root_path, 'static', 'antes-depois'))

pasta = os.path.join(app.root_path, 'static', 'antes-depois')
if os.path.exists(pasta):
    arquivos = os.listdir(pasta)
    print("QTD ARQUIVOS NA PASTA:", len(arquivos))
    for a in sorted(arquivos):
        print("  -", a)
    # testa se os 20 nomes esperados existem
    esperados = ['advogada-antes.png','advogada-depois.png','medica-antes.png','medica-depois.png',
                 'executivo-antes.png','executivo-depois.png','empreendedor-antes.png','empreendedor-depois.png',
                 'senhora-antes.png','senhora-depois.png','newborn-antes.png','newborn-depois.png',
                 'aniversario-antes.png','aniversario-depois.png','viagem-antes.png','viagem-depois.png',
                 'formatura-antes.png','formatura-depois.png','glamour-antes.png','glamour-depois.png']
    for e in esperados:
        existe = os.path.exists(os.path.join(pasta, e))
        print(("OK  " if existe else "FALTA"), e)
else:
    print("ERRO: A pasta antes-depois NAO existe em", pasta)