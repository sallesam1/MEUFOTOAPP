import os
from supabase_storage import upload_bytes

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

def migrar():
    if not os.path.exists(UPLOAD_FOLDER):
        print("Pasta uploads nao encontrada.")
        return
    arquivos = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
    total = len(arquivos)
    ok = 0
    for nome in arquivos:
        caminho = os.path.join(UPLOAD_FOLDER, nome)
        try:
            with open(caminho, 'rb') as f:
                dados = f.read()
            upload_bytes(dados, nome, 'image/jpeg')
            ok += 1
            print("OK: " + nome)
        except Exception as e:
            print("ERRO: " + nome + " -> " + str(e))
    print("")
    print("Concluido: " + str(ok) + " de " + str(total) + " fotos enviadas para a nuvem.")

if __name__ == '__main__':
    migrar()