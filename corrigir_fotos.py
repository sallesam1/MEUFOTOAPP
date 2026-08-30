import os

pasta = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'antes-depois')

if not os.path.exists(pasta):
    print("ERRO: pasta nao encontrada em", pasta)
    exit()

corrigidos = 0
for nome in os.listdir(pasta):
    novo = nome
    # 1) remove a extensao duplicada: .png.png -> .png
    if novo.lower().endswith('.png.png'):
        novo = novo[:-4]
    # 2) corrige o erro de digitação: executivoo -> executivo
    if novo.lower().startswith('executivoo-'):
        novo = 'executivo-' + novo[len('executivoo-'):]
    if novo != nome:
        origem = os.path.join(pasta, nome)
        destino = os.path.join(pasta, novo)
        os.rename(origem, destino)
        print("CORRIGIDO:", nome, "->", novo)
        corrigidos += 1

if corrigidos == 0:
    print("Nenhum arquivo precisou de correcao. Tudo certo!")
else:
    print("Total de arquivos corrigidos:", corrigidos)
print("PRONTO! Agora e so recarregar a pagina com Ctrl+Shift+R")