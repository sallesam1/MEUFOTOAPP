# criar_tabelas.py - cria as tabelas no Supabase
from app import app, db

with app.app_context():
    db.create_all()
    print('TABELAS CRIADAS NO SUPABASE COM SUCESSO!')