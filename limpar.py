import os

base = os.path.dirname(os.path.abspath(__file__))
remover = ['update_mobile.py', 'corrigir_mobile.py', 'fix_final.py', 
           'fix_definitivo.py', 'diag_dashboard.py', 'diagnostico.py', 'limpar.py']

for f in remover:
    path = os.path.join(base, f)
    if os.path.exists(path):
        os.remove(path)
        print(f"Apagado: {f}")

print("\nLimpeza concluida!")