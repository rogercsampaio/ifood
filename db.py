import sqlite3

DB_NAME = "bd/ifood_app.db"


# =========================
# CONEXÃO
# =========================
def get_connection():
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None


# 🔥 UTILIDADE: converter Row → dict
def rows_to_dicts(rows):
    return [dict(row) for row in rows]


# =========================
# CRIAÇÃO DE TABELAS
# =========================
def criar_tabelas():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS produto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            url_foto TEXT,
            preco REAL NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback_temporario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_cliente TEXT,
            descricao TEXT,
            sentimento_final TEXT,
            categoria TEXT,
            data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
            produto_id INTEGER,
            FOREIGN KEY (produto_id) REFERENCES produto(id)
        )
        """)

        conn.commit()
        conn.close()

        print("Tabelas criadas com sucesso.")

    except sqlite3.Error as e:
        print(f"Erro ao criar tabelas: {e}")


# =========================
# SCHEMA
# =========================
def get_schema_overview_grouped():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
        m.name AS tabela,
        p.name AS campo,
        p.type AS tipo
    FROM sqlite_master m
    JOIN pragma_table_info(m.name) p
    WHERE m.type = 'table'
    ORDER BY m.name, p.cid;
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    schema = {}

    for row in rows:
        tabela = row["tabela"]
        campo = row["campo"]
        tipo = row["tipo"]

        if tabela.startswith("sqlite_"):
            continue

        if tabela not in schema:
            schema[tabela] = {
                "qtd_campos": 0,
                "campos": []
            }

        schema[tabela]["campos"].append({
            "campo": campo,
            "tipo": tipo
        })

        schema[tabela]["qtd_campos"] += 1

    return {
        "qtd_total_tabelas": len(schema),
        "tabelas": schema
    }


# =========================
# LIMPAR BANCO
# =========================
def limpar_todas_tabelas():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name 
            FROM sqlite_master 
            WHERE type='table'
            AND name NOT LIKE 'sqlite_%';
        """)

        tabelas = cursor.fetchall()

        cursor.execute("PRAGMA foreign_keys = OFF;")

        for tabela in tabelas:
            cursor.execute(f"DELETE FROM {tabela['name']};")

        # reset autoincrement
        cursor.execute("DELETE FROM sqlite_sequence;")

        conn.commit()
        cursor.execute("PRAGMA foreign_keys = ON;")
        conn.close()

        print("Banco limpo com sucesso.")

    except sqlite3.Error as e:
        print(f"Erro ao limpar tabelas: {e}")


# =========================
# CRUD PRODUTOS
# =========================
def criar_produto(nome, categoria, url_foto, preco):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO produto (nome, categoria, url_foto, preco)
        VALUES (?, ?, ?, ?)
        """, (nome, categoria, url_foto, preco))

        conn.commit()
        conn.close()

        print(f"Produto '{nome}' criado com sucesso.")

    except sqlite3.Error as e:
        print(f"Erro ao criar produto: {e}")


def listar_produtos():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM produto")
        rows = cursor.fetchall()
        conn.close()

        return rows_to_dicts(rows)

    except sqlite3.Error as e:
        print(f"Erro ao listar produtos: {e}")
        return []


# =========================
# CRUD FEEDBACK
# =========================
def criar_feedback(nome_cliente, descricao, sentimento_final, categoria, produto_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO feedback_temporario
            (nome_cliente, descricao, sentimento_final, categoria, produto_id)
            VALUES (?, ?, ?, ?, ?)
        """, (nome_cliente, descricao, sentimento_final, categoria, produto_id))

        conn.commit()
        conn.close()

        print("Feedback cadastrado com sucesso.")

    except sqlite3.Error as e:
        print(f"Erro ao cadastrar feedback: {e}")


def listar_feedbacks():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM feedback_temporario
            ORDER BY data_hora DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        return rows_to_dicts(rows)

    except sqlite3.Error as e:
        print(f"Erro ao listar feedbacks: {e}")
        return []


def listar_feedbacks_com_produto():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                f.id,
                f.nome_cliente,
                f.descricao,
                f.sentimento_final,
                f.categoria,
                f.data_hora,
                p.nome AS produto
            FROM feedback_temporario f
            LEFT JOIN produto p
            ON f.produto_id = p.id
            ORDER BY f.data_hora DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        return rows_to_dicts(rows)

    except sqlite3.Error as e:
        print(f"Erro ao listar feedbacks: {e}")
        return []