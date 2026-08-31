import os

base = os.path.dirname(os.path.abspath(__file__))
tpl = os.path.join(base, 'templates', 'portfolio.html')

with open(tpl, 'r', encoding='utf-8') as f:
    conteudo = f.read()

novo = conteudo.replace('http://localhost:5000/p/', '{{ request.host_url }}p/')

if novo != conteudo:
    with open(tpl, 'w', encoding='utf-8') as f:
        f.write(novo)
    print('OK! Links corrigidos para usar o endereco do site.')
else:
    print('Nenhum link localhost encontrado.')