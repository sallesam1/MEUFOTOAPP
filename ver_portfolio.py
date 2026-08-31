import os

base = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(base, 'templates')

achou = False
for nome in os.listdir(templates):
    if 'portfolio' in nome.lower() or 'portifolio' in nome.lower():
        caminho = os.path.join(templates, nome)
        with open(caminho, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        print('ARQUIVO ENCONTRADO:', nome)
        print('=' * 60)
        print(conteudo)
        achou = True
        break

if not achou:
    print('Nao achei arquivo com "portfolio" no nome. Listando a pasta templates:')
    for nome in os.listdir(templates):
        print('-', nome)