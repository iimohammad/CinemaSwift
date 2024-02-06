import database_manager

db = database_manager.DatabaseManager()

db.connect()
create_table_subscriptions = """
CREATE TABLE IF NOT EXISTS subscriptions (
    id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    discount_number INT NOT NULL,
    discount_value INT NOT NULL,
    PRIMARY KEY (id)
);
"""
db.execute_query(create_table_subscriptions)

insertion_to_subscriptions = """
    INSERT INTO subscriptions (id, name, discount_number, discount_value) VALUES
    ('1', 'Golden', '0', '50'),
    ('2', 'Silver', '3', '20'),
    ('3', 'Bronze', '0', '0');
"""
db.execute_query(insertion_to_subscriptions)

create_table_users = """
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(255) NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    birthday DATE NULL,
    phone VARCHAR(255) NULL,
    subscription_type_id INT NOT NULL,
    password VARCHAR(255) NOT NULL,
    last_login TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_admin BOOLEAN,
    PRIMARY KEY (id),
    FOREIGN KEY (subscription_type_id) REFERENCES subscriptions (id),
    UNIQUE INDEX id_UNIQUE (id) VISIBLE,
    UNIQUE INDEX user_name_UNIQUE (user_name) VISIBLE,
    UNIQUE INDEX email_UNIQUE (email) VISIBLE
);
"""
db.execute_query(create_table_users)



create_table_userssubscriptions = """
CREATE TABLE IF NOT EXISTS userssubscriptions (
    user_id VARCHAR(255) NOT NULL,
    subscription_id INT NOT NULL,
    start_date DATETIME NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (subscription_id) REFERENCES subscriptions (id)
);
"""
db.execute_query(create_table_userssubscriptions)

create_table_films = """
CREATE TABLE IF NOT EXISTS films (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    age_rating INT NOT NULL,
    duration INT NOT NULL,
    point DECIMAL(3,1) NOT NULL,
    PRIMARY KEY (id)
);
"""
db.execute_query(create_table_films)

create_table_comments = """
CREATE TABLE IF NOT EXISTS comments (
  id INT NOT NULL AUTO_INCREMENT,
  film_id INT NOT NULL,
  user_id VARCHAR(255) NOT NULL,
  text MEDIUMTEXT NOT NULL,
  parent_comment INT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  FOREIGN KEY (film_id) REFERENCES films (id),
  FOREIGN KEY (user_id) REFERENCES users (id),
  FOREIGN KEY (parent_comment) REFERENCES comments (id)
);
"""
db.execute_query(create_table_comments)

create_table_filmspoints = """
CREATE TABLE IF NOT EXISTS filmspoints (
  film_id INT NOT NULL,
  user_id VARCHAR(255) NOT NULL,
  point INT NOT NULL,
  PRIMARY KEY (film_id, user_id),
  FOREIGN KEY (film_id) REFERENCES films (id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
"""
db.execute_query(create_table_filmspoints)


create_table_bankaccounts = """
CREATE TABLE IF NOT EXISTS bankaccounts (
  id INT NOT NULL AUTO_INCREMENT,
  user_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  balance INT NOT NULL,
  cvv2 INT NOT NULL,
  password VARCHAR(255) NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id) REFERENCES users (id)
);
"""
db.execute_query(create_table_bankaccounts)

create_table_wallets = """
CREATE TABLE IF NOT EXISTS wallets (
  id INT NOT NULL AUTO_INCREMENT,
  user_id VARCHAR(255) NOT NULL UNIQUE,
  balance INT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id) REFERENCES users (id)
);
"""
db.execute_query(create_table_wallets)

create_table_screens = """
CREATE TABLE IF NOT EXISTS screens (
  id INT NOT NULL AUTO_INCREMENT,
  film_id INT NOT NULL,
  number_of_sans INT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (film_id) REFERENCES films (id)
);
"""
db.execute_query(create_table_screens)

create_table_sessions = """
CREATE TABLE IF NOT EXISTS sessions (
  id INT NOT NULL AUTO_INCREMENT,
  screen_id INT NOT NULL,
  start_time DATETIME NOT NULL,
  capacity INT NOT NULL,
  ticket_price INT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (screen_id) REFERENCES screens (id)
);
"""
db.execute_query(create_table_sessions)

create_table_seats = """
CREATE TABLE IF NOT EXISTS seats (
  id INT AUTO_INCREMENT,
  session_id INT NOT NULL,
  status VARCHAR(10) NOT NULL,
  number INT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE
);
"""
db.execute_query(create_table_seats)

create_table_refundrolls = """
CREATE TABLE IF NOT EXISTS refundrolls (
  id INT AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  percent_value INT NOT NULL,
  PRIMARY KEY (id)
);
"""
db.execute_query(create_table_refundrolls)

create_table_tickets = """
CREATE TABLE IF NOT EXISTS tickets (
  id INT AUTO_INCREMENT,
  user_id VARCHAR(255),
  seat_id INT NOT NULL,
  price DECIMAL(10,1) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id) REFERENCES users (id),
  FOREIGN KEY (seat_id) REFERENCES `seats` (id)
);
"""
db.execute_query(create_table_tickets)
db.disconnect()