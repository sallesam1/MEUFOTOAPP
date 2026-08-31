import os

base = os.path.dirname(os.path.abspath(__file__))
css_path = os.path.join(base, 'static', 'css', 'style.css')

adicao = """

/* ETIQUETAS ANTES/DEPOIS POR CIMA DA FOTO - CORRECAO DEFINITIVA */
.grid .card > div[style*="display:flex"] > div {
    position: relative;
    display: inline-block;
}
.grid .card > div[style*="display:flex"] > div > p {
    position: absolute;
    top: 8px;
    left: 8px;
    background: rgba(0,0,0,.75);
    color: #fff;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 700;
    z-index: 5;
    margin: 0;
}
.grid .card > div[style*="display:flex"] > div:last-child > p {
    left: auto;
    right: 8px;
}
"""

with open(css_path, 'r', encoding='utf-8') as f:
    conteudo = f.read()

if 'CORRECAO DEFINITIVA' not in conteudo:
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(conteudo + adicao)
    print('OK! Etiquetas corrigidas.')
else:
    print('CSS ja corrigido.')