CREATE SCHEMA IF NOT EXISTS `cinemaswift` ;
USE `cinemaswift`;

CREATE TABLE IF NOT EXISTS `cinemaswift`.`users` (
  `id` VARCHAR(255) NOT NULL,
  `user_name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `birthday` DATE NULL,
  `phone` VARCHAR(255) NULL,
  `subscription_type` VARCHAR(255) NULL,
  `password` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `user_name_UNIQUE` (`user_name` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE
  );

  CREATE TABLE IF NOT EXISTS `cinemaswift`.`admins` (
  `id` VARCHAR(255) NOT NULL,
  `user_name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `birthday` DATE NULL,
  `phone` VARCHAR(45) NULL,
  `subscription_type` VARCHAR(7) NOT NULL,
  `admin_type` VARCHAR(7) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `user_name_UNIQUE` (`user_name` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE
  );

  CREATE TABLE IF NOT EXISTS `cinemaswift`.`subscriptions` (
  `id` INT NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `discount_number` INT NOT NULL,
  `discount_value` INT NOT NULL,
  `drink_number` INT NOT NULL,
  PRIMARY KEY (`id`)
  );

  CREATE TABLE IF NOT EXISTS `cinemaswift`.`userssubscriptions` (
  `user_id` VARCHAR(255) NOT NULL,
  `subscription_id` INT NOT NULL,
  `start_date` DATETIME NOT NULL,
  PRIMARY KEY (`user_id`),
  FOREIGN KEY (user_id) REFERENCES users (id),
  FOREIGN KEY (subscription_id) REFERENCES subscriptions (id)
  );


  CREATE TABLE IF NOT EXISTS `cinemaswift`.`films` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `age_rating` INT NOT NULL,
  `duration` INT NOT NULL,
  `rate` DECIMAL NOT NULL,
  PRIMARY KEY (`id`)
  );

CREATE TABLE IF NOT EXISTS `cinemaswift`.`comments` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `film_id` INT NOT NULL,
  `user_id` VARCHAR(255) NOT NULL,
  `text` MEDIUMTEXT NOT NULL,
  `created_at` DATETIME NOT NULL,
  `parent_comment` INT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`film_id`) REFERENCES `films` (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  FOREIGN KEY (`parent_comment`) REFERENCES `comments` (`id`)
);

CREATE TABLE IF NOT EXISTS `cinemaswift`.`filmspoints` (
  `film_id` INT NOT NULL,
  `user_id` VARCHAR(255) NOT NULL,
  `point` INT NOT NULL,
  PRIMARY KEY (`film_id`,`user_id`),
  FOREIGN KEY (`film_id`) REFERENCES `films` (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
);

CREATE TABLE IF NOT EXISTS `cinemaswift`.`bankaccounts` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(255) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `balance` INT NOT NULL,
  `cvv2` INT NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
);


CREATE TABLE IF NOT EXISTS `cinemaswift`.`wallets` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(255) NOT NULL UNIQUE,
  `balance` INT NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
);


CREATE TABLE IF NOT EXISTS `cinemaswift`.`screens` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `film_id` INT NOT NULL,
  `number_of_sans` INT NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`film_id`) REFERENCES `films` (`id`)
);

CREATE TABLE IF NOT EXISTS `cinemaswift`.`sessions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `screen_id` INT NOT NULL,
  `start_time` DATEtiME NOT NULL,
  `capacity` INT NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`screen_id`) REFERENCES `screens` (`id`)
);

CREATE TABLE IF NOT EXISTS `cinemaswift`.`seats` (
  `id` INT  AUTO_INCREMENT,
  `sessions_id` INT NOT NULL,
  `status` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`sessions_id`) REFERENCES `sessions` (`id`)
);

CREATE TABLE IF NOT EXISTS `cinemaswift`.`freedrinks` (
  `id` INT AUTO_INCREMENT,
  `user_id` VARCHAR(255) NOT NULL ,
  `date` DATETIME NOT NULL,
  `number` INT NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
);

CREATE TABLE IF NOT EXISTS `cinemaswift`.`refundrolls` (
  `id` INT AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL ,
  `percent_value` INT NOT NULL,
  PRIMARY KEY (`id`)
);