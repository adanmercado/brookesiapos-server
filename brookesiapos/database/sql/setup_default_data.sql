/*
 * Author: Adan Mercado
 * https://github.com/adanmercado/brookesiapos-server
 * Run this as: sqlite3 database_name.db < setup_default_data.sql
*/

INSERT INTO user_roles(name) VALUES('Administrator'), ('Supervisor'), ('Cashier');


INSERT INTO users(name, username, password, role) VALUES('Brookesia POS Administrator', 'brookesia', '24b4699ff6e696904210b8243142e5705d38b3a8a8f5ea34d09ae222a634a412', 1);


INSERT INTO clients(name) VALUES('General');


INSERT INTO providers(name) VALUES('General');


INSERT INTO categories(name) VALUES('General');


INSERT INTO measures(name, symbol) VALUES('Piece', 'Pz'), ('Meter', 'M'), ('Liter', 'L'), ('Kilogram', 'Kg');


INSERT INTO taxes(name, tax_value) VALUES('None', '0.0');


INSERT INTO transaction_states(name) VALUES('Finished'), ('Pending'), ('Canceled');


INSERT INTO transaction_types(name) VALUES('Sale');