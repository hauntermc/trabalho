from sqlalchemy import create_engine, text

# Substitua 'path_to_your_db.db' pelo caminho do seu banco de dados
engine = create_engine('sqlite:///estoque.db')

with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT nome, COUNT(*) as count
        FROM materiais
        GROUP BY nome
        HAVING count > 1
    """))
    duplicates = result.fetchall()
    for row in duplicates:
        print(row)
