-- Written for mariadb

DROP TABLE IF EXISTS monsters;
CREATE TABLE monsters (
  id int unsigned NOT NULL AUTO_INCREMENT UNIQUE,
  session int unsigned NOT NULL,
  idx int unsigned NOT NULL CHECK (idx < 3),
  PRIMARY KEY (id)
) AUTO_INCREMENT 0;

DROP TABLE IF EXISTS parts;
CREATE TABLE parts (
  id int unsigned NOT NULL AUTO_INCREMENT UNIQUE,
  session int unsigned NOT NULL,
  monsteruid int unsigned NOT NULL,
  hp int unsigned NOT NULL DEFAULT 999,
  idx int unsigned NOT NULL,
  PRIMARY KEY (id)
) AUTO_INCREMENT 0;

DROP TABLE IF EXISTS sessions;
CREATE TABLE sessions (
  id int unsigned NOT NULL AUTO_INCREMENT UNIQUE,
  idstring varchar(45) NOT NULL UNIQUE,
  playercount int unsigned DEFAULT 0 CHECK (playercount <= 4),
  monstercount int unsigned DEFAULT 0 CHECK (monstercount <= 3),
  PRIMARY KEY (id)
) AUTO_INCREMENT 0;