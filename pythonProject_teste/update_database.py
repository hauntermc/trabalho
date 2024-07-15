import sqlite3


def update_database():
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()

    try:
        # Verifique se as colunas já existem antes de tentar adicioná-las novamente
        cursor.execute('PRAGMA table_info(produtos)')
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]

        if 'quantidade' not in column_names:
            cursor.execute('ALTER TABLE produtos ADD COLUMN quantidade INTEGER')
            print('Coluna quantidade adicionada com sucesso.')

        if 'fornecedor' not in column_names:
            cursor.execute('ALTER TABLE produtos ADD COLUMN fornecedor TEXT')
            print('Coluna fornecedor adicionada com sucesso.')

        if 'data' not in column_names:
            cursor.execute('ALTER TABLE produtos ADD COLUMN data DATE')
            print('Coluna data adicionada com sucesso.')

        conn.commit()
    except sqlite3.Error as e:
        print(f'Erro ao adicionar colunas: {e}')
    finally:
        conn.close()


if __name__ == '__main__':
    update_database()
