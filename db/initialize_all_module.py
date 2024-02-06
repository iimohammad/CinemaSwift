import database_manager
import models

db = database_manager.DatabaseManager()

db.connect()

# Define SQL statements for creating tables
create_users_table_query = """
CREATE TABLE IF NOT EXISTS `users` (
  `id` VARCHAR(255) NOT NULL,
  `user_name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `birthday` DATE NULL,
  `phone` VARCHAR(255) NULL,
  `password` VARCHAR(255) NOT NULL,
  `last_login` TIMESTAMP NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `user_name_UNIQUE` (`user_name` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE

);


"""

# Execute the query
db.execute_query(create_users_table_query)

create_tables_queries = """
    CREATE TABLE IF NOT EXISTS `admins` (
  `id` VARCHAR(255) NOT NULL,
  `user_name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `birthday` DATE NULL,
  `phone` VARCHAR(45) NULL,
  `admin_type` VARCHAR(7) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `last_login` TIMESTAMP NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `user_name_UNIQUE` (`user_name` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE
  );

"""

db.execute_query(create_tables_queries)

create_tables_queries = """
    CREATE TABLE IF NOT EXISTS `subscriptions` (
  `id` INT NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `discount_number` INT NOT NULL,
  `discount_value` INT NOT NULL,
  `drink_number` INT NOT NULL,
  PRIMARY KEY (`id`)
  );

"""

db.execute_query(create_tables_queries)

create_tables_queries = """
   CREATE TABLE IF NOT EXISTS `userssubscriptions` (
  `user_id` VARCHAR(255) NOT NULL,
  `subscription_id` INT NOT NULL,
  `start_date` DATETIME NOT NULL,
  PRIMARY KEY (`user_id`),

  FOREIGN KEY (user_id) REFERENCES users (id),
  FOREIGN KEY (subscription_id) REFERENCES subscriptions (id)
  );

"""

db.execute_query(create_tables_queries)

create_tables_queries = """
CREATE TABLE IF NOT EXISTS `films` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `age_rating` INT NOT NULL,
  `duration` INT NOT NULL,
  `point` DECIMAL(3,1) NOT NULL,
  PRIMARY KEY (`id`)
  );
"""
db.execute_query(create_tables_queries)

create_tables_queries = """
CREATE TABLE IF NOT EXISTS `comments` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `film_id` INT NOT NULL,
  `user_id` VARCHAR(255) NOT NULL,
  `text` MEDIUMTEXT NOT NULL,
  `parent_comment` INT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`film_id`) REFERENCES `films` (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  FOREIGN KEY (`parent_comment`) REFERENCES `comments` (`id`)
);
"""
db.execute_query(create_tables_queries)

create_tables_queries = """
CREATE TABLE IF NOT EXISTS `filmspoints` (
  `film_id` INT NOT NULL,
  `user_id` VARCHAR(255) NOT NULL,
  `point` INT NOT NULL,
  PRIMARY KEY (`film_id`,`user_id`),
  FOREIGN KEY (`film_id`) REFERENCES `films` (`id`)ON DELETE CASCADE,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)ON DELETE CASCADE
);
"""
db.execute_query(create_tables_queries)

create_tables_queries = """
CREATE TABLE IF NOT EXISTS `bankaccounts` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(255) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `balance` INT NOT NULL,
  `cvv2` INT NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
);
"""

db.execute_query(create_tables_queries)

create_tables_queries = """
CREATE TABLE IF NOT EXISTS `wallets` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(255) NOT NULL UNIQUE,
  `balance` INT NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
);
"""
db.execute_query(create_tables_queries)

create_tables_queries = """
CREATE TABLE IF NOT EXISTS `screens` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `film_id` INT NOT NULL,
  `number_of_sans` INT NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`film_id`) REFERENCES `films` (`id`)
);
"""
db.execute_query(create_tables_queries)

create_tables_queries = """
CREATE TABLE IF NOT EXISTS `sessions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `screen_id` INT NOT NULL,
  `start_time` DATEtiME NOT NULL,
  `capacity` INT NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`screen_id`) REFERENCES `screens` (`id`)
);
"""
db.execute_query(create_tables_queries)

create_tables_queries = """
CREATE TABLE IF NOT EXISTS `seats` (
  `id` INT  AUTO_INCREMENT,
  `session_id` INT NOT NULL,
  `status` VARCHAR(10) NOT NULL,
  `number` int NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`session_id`) REFERENCES `sessions` (`id`) ON DELETE CASCADE
);
"""
db.execute_query(create_tables_queries)

create_tables_queries = """
CREATE TABLE IF NOT EXISTS `freedrinks` (
  `id` INT AUTO_INCREMENT,
  `user_id` VARCHAR(255) NOT NULL ,
  `date` DATETIME NOT NULL,
  `number` INT NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
);

"""
db.execute_query(create_tables_queries)

create_tables_queries = """
CREATE TABLE IF NOT EXISTS `refundrolls` (
  `id` INT AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL ,
  `percent_value` INT NOT NULL,
  PRIMARY KEY (`id`)
);
"""
db.execute_query(create_tables_queries)
db.disconnect()
