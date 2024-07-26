from sqlalchemy import create_engine, text

# Substitua 'path_to_your_db.db' pelo caminho do seu banco de dados
engine = create_engine('sqlite:///estoque.db')

with engine.connect() as conn:
    duplicates = conn.execute(text("""
        SELECT nome, COUNT(*) as count
        FROM materiais
        GROUP BY nome
        HAVING count > 1
    """)).fetchall()

    for row in duplicates:
        nome = row[0]  # Acessa o primeiro elemento da tupla (nome)
        conn.execute(text(f"""
            DELETE FROM materiais
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM materiais
                WHERE nome = :nome
            )
            AND nome = :nome
        """), {'nome': nome})
