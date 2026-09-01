from supabase import create_client
from supabase_config import SUPABASE_URL, SUPABASE_KEY

# Conecta no Supabase
cliente = create_client(SUPABASE_URL, SUPABASE_KEY)

# Tenta buscar os dados da tabela de clientes
resposta = cliente.table("clientes").select("*").execute()

print("CONEXÃO OK! O Supabase respondeu.")
print("Número de clientes na tabela:", len(resposta.data))