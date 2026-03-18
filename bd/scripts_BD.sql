PRAGMA foreign_keys = ON;

-- Tabela de produtos
CREATE TABLE produto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    categoria TEXT NOT NULL,
    url_foto TEXT,
    preco REAL NOT NULL
);

-- Tabela de pedidos
CREATE TABLE pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    preco_total REAL
);

-- Tabela intermediária (produtos dentro do pedido)
CREATE TABLE pedido_produto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER,
    produto_id INTEGER,
    quantidade INTEGER NOT NULL,

    FOREIGN KEY (pedido_id) REFERENCES pedido(id) ON DELETE CASCADE,
    FOREIGN KEY (produto_id) REFERENCES produto(id)
);

-- Tabela de feedback
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER,
    produto_id INTEGER,
    nome_cliente TEXT,
    descricao TEXT,
    categoria TEXT
    sentimento_final TEXT,

    FOREIGN KEY (pedido_id) REFERENCES pedido(id),
    FOREIGN KEY (produto_id) REFERENCES produto(id)
);

-- Tabela de feedback temporária (sem referência a pedido)
CREATE TABLE feedback_temporario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_cliente TEXT,
    descricao TEXT,
    sentimento_final TEXT,
    categoria TEXT,
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    produto_id INTEGER,
    FOREIGN KEY (produto_id) REFERENCES produto(id)
);