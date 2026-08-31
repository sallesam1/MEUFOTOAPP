import os
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine, MetaData, text

LOCAL_DB = os.path.join('instance', 'meufotoapp.db')
NUVEM_DB = os.environ.get('DATABASE_URL')

if not NUVEM_DB:
    print('ERRO: variável DATABASE_URL não encontrada no .env')
    exit()

local_engine = create_engine('sqlite:///' + LOCAL_DB)
nuvem_engine = create_engine(NUVEM_DB)

local_conn = local_engine.connect()
nuvem_conn = nuvem_engine.connect()

meta_local = MetaData()
meta_local.reflect(bind=local_engine)
meta_nuvem = MetaData()
meta_nuvem.reflect(bind=nuvem_engine)

ordem = ['user', 'galeria', 'photo', 'selection', 'watermark',
         'portfolio_photo', 'pose_photo', 'app_settings',
         'pose_selection', 'plan']

tabelas_copiadas = []
for nome in ordem:
    if nome not in meta_local.tables:
        print(f'AVISO: tabela "{nome}" não existe no banco local, pulando.')
        continue
    if nome not in meta_nuvem.tables:
        print(f'AVISO: tabela "{nome}" não existe no Supabase, pulando.')
        continue

    tabela_local = meta_local.tables[nome]
    tabela_nuvem = meta_nuvem.tables[nome]

    # Só copia as colunas que existem NOS DOIS bancos
    colunas_comuns = [c for c in tabela_local.columns.keys()
                      if c in tabela_nuvem.columns.keys()]

    dest_count = nuvem_conn.execute(text(f'SELECT COUNT(*) FROM "{nome}"')).scalar()
    if dest_count and dest_count > 0:
        print(f'Tabela {nome}: já tem {dest_count} registros no Supabase - pulando para nao duplicar.')
        continue

    linhas = local_conn.execute(tabela_local.select()).fetchall()
    if not linhas:
        print(f'Tabela {nome}: 0 registros (vazia)')
        continue

    dados = []
    for r in linhas:
        d = dict(r._mapping)
        # Mantém apenas as colunas comuns
        d = {k: v for k, v in d.items() if k in colunas_comuns}
        dados.append(d)

    nuvem_conn.execute(tabela_nuvem.insert(), dados)

    try:
        if 'id' in colunas_comuns:
            nuvem_conn.execute(text(
                f"SELECT setval(pg_get_serial_sequence('{nome}', 'id'), "
                f"(SELECT COALESCE(MAX(id), 1) FROM \"{nome}\"))"
            ))
    except Exception:
        pass

    nuvem_conn.commit()
    tabelas_copiadas.append((nome, len(dados)))
    print(f'Tabela {nome}: {len(dados)} registros copiados!')

print()
print('=' * 50)
print('MIGRAÇÃO CONCLUÍDA!')
for nome, qtd in tabelas_copiadas:
    print(f'  - {nome}: {qtd} registros')
print('=' * 50)