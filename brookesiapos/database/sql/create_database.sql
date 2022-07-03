/*
 * Author: Adan Mercado
 * https://github.com/adanmercado/brookesiapos-server
 * Run this as: sqlite3 database_name.db < create_database.sql
*/

CREATE TABLE IF NOT EXISTS user_roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    address TEXT DEFAULT NULL,
    phone TEXT DEFAULT NULL,
    email TEXT DEFAULT NULL,
    username TEXT UNIQUE NOT NULL,
    password BLOB NOT NULL,
    role INTEGER NOT NULL,
    picture BLOB DEFAULT NULL,
    FOREIGN KEY(role) REFERENCES user_roles(id)
);


CREATE TABLE IF NOT EXISTS terminals (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    terminal_number INTEGER UNIQUE NOT NULL,
    name TEXT UNIQUE NOT NULL,
    uuid TEXT UNIQUE NOT NULL,
    last_ip TEXT DEFAULT NULL
);


CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    terminal_id INTEGER NOT NULL,
    login_datetime TEXT NOT NULL,
    logout_datetime TEXT DEFAULT NULL,
    is_active INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(terminal_id) REFERENCES terminals(id)
);


CREATE TABLE IF NOT EXISTS drawer (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    session_id INTEGER NOT NULL,
    init_amount REAL NOT NULL DEFAULT 0.0,
    cash_amount REAL NOT NULL DEFAULT 0.0,
    card_amount REAL NOT NULL DEFAULT 0.0,
    cash_in REAL NOT NULL DEFAULT 0.0,
    cash_out REAL NOT NULL DEFAULT 0.0,
    FOREIGN KEY(session_id) REFERENCES sessions(id)
);


CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    salesman TEXT DEFAULT NULL,
    address TEXT DEFAULT NULL,
    phone TEXT DEFAULT NULL,
    email TEXT DEFAULT NULL,
    picture BLOB DEFAULT NULL
);


CREATE TABLE IF NOT EXISTS providers (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    address TEXT DEFAULT NULL,
    phone TEXT DEFAULT NULL,
    email TEXT DEFAULT NULL,
    picture BLOB DEFAULT NULL
);


CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    description TEXT DEFAULT NULL
);


CREATE TABLE IF NOT EXISTS measures (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    symbol TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS taxes (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    tax_value REAL NOT NULL
);


CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    barcode TEXT NOT NULL,
    description TEXT NOT NULL,
    cost_price REAL NOT NULL,
    sale_price REAL NOT NULL,
    profit_percent REAL NOT NULL,
    profit_amount REAL NOT NULL,
    taxes TEXT DEFAULT '',
    current_stock REAL NOT NULL DEFAULT 0.0,
    min_stock REAL NOT NULL DEFAULT 0.0,
    measure INTEGER NOT NULL DEFAULT 1,
    category INTEGER NOT NULL DEFAULT 1,
    provider INTEGER NOT NULL DEFAULT 1,
    is_available INTEGER DEFAULT 1,
    picture BLOB DEFAULT NULL,
    FOREIGN KEY(measure) REFERENCES measures(id),
    FOREIGN KEY(category) REFERENCES categories(id),
    FOREIGN KEY(provider) REFERENCES providers(id)
);


CREATE TABLE IF NOT EXISTS transaction_states (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS transaction_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    type INTEGER NOT NULL,
    status INTEGER NOT NULL,
    datetime TEXT NOT NULL,
    session_id INTEGER NOT NULL,
    client_id INTEGER NOT NULL,
    subtotal REAL NOT NULL,
    total REAL NOT NULL,
    discount REAL NOT NULL,
    qty REAL NOT NULL,
    profit REAL NOT NULL,
    taxes TEXT NOT NULL,
    pay_with REAL NOT NULL,
    change REAL NOT NULL,
    notes TEXT DEFAULT NULL,
    FOREIGN KEY(type) REFERENCES transaction_types(id),
    FOREIGN KEY(status) REFERENCES transaction_states(id),
    FOREIGN KEY(session_id) REFERENCES sessions(id),
    FOREIGN KEY(client_id) REFERENCES clients(id)
);

CREATE TABLE IF NOT EXISTS transaction_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    transaction_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    qty REAL NOT NULL,
    price REAL NOT NULL,
    total REAL NOT NULL,
    FOREIGN KEY(transaction_id) REFERENCES transactions(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
);