import os

base = os.path.dirname(os.path.abspath(__file__))
css_path = os.path.join(base, 'static', 'css', 'style.css')

adicao = """

/* ETIQUETAS ANTES/DEPOIS SOBRE A FOTO */
[class*="antes"], [class*="depois"] {
    position: absolute;
    top: 10px;
    background: rgba(0,0,0,.75);
    color: #fff;
    padding: 4px 12px;
    border-radius: 4px;
    font-size: 13px;
    font-weight: 700;
    z-index: 5;
}
[class*="antes"] { left: 10px; }
[class*="depois"] { right: 10px; left: auto; }
[class*="card"], [class*="item"], [class*="pair"], [class*="wrap"] {
    position: relative;
}
"""

with open(css_path, 'r', encoding='utf-8') as f:
    conteudo = f.read()

if 'ETIQUETAS ANTES/DEPOIS' not in conteudo:
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(conteudo + adicao)
    print('OK! CSS atualizado com as etiquetas.')
else:
    print('CSS ja esta atualizado.')