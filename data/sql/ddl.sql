
CREATE TABLE 'unit' (
  'unit_id' INT NOT NULL AUTO_INCREMENT,
  'description' VARCHAR(20) NOT NULL,
  PRIMARY KEY ('unit_id'),
  UNIQUE INDEX 'description_UNIQUE' ('description' ASC));

CREATE TABLE 'institution_type' (
  'institution_type_id' INT NOT NULL AUTO_INCREMENT,
  'description' VARCHAR(45) NOT NULL,
  PRIMARY KEY ('institution_type_id'),
  UNIQUE INDEX 'description_UNIQUE' ('description' ASC));

CREATE TABLE 'manufacturer' (
  'manufacturer_id' INT NOT NULL AUTO_INCREMENT,
  'name' VARCHAR(45) NOT NULL,
  PRIMARY KEY ('manufacturer_id'),
  UNIQUE INDEX 'name_UNIQUE' ('name' ASC));

CREATE TABLE 'substance' (
  'substance_id' INT NOT NULL AUTO_INCREMENT,
  'description' VARCHAR(100) NOT NULL,
  PRIMARY KEY ('substance_id'),
  UNIQUE INDEX 'description_UNIQUE' ('description' ASC));

CREATE TABLE 'medicine' (
  'medicine_id' INT NOT NULL AUTO_INCREMENT,
  'manufacturer_id' INT NOT NULL,
  'name' VARCHAR(45) NOT NULL,
  'description' VARCHAR(100) NOT NULL,
  'substance_id' INT(11) NOT NULL,
  PRIMARY KEY ('medicine_id'),
  INDEX 'manufacturer_id_idx' ('manufacturer_id' ASC),
  CONSTRAINT 'manufacturer_id'
    FOREIGN KEY ('manufacturer_id')
    REFERENCES 'manufacturer' ('manufacturer_id')
    ON DELETE NO ACTION
    ON UPDATE NO ACTION),
  CONSTRAINT 'substance_id'
    FOREIGN KEY ('substance_id')
    REFERENCES 'substance' ('substance_id')
    ON DELETE NO ACTION;

CREATE TABLE 'user' (
  'user_id' INT NOT NULL AUTO_INCREMENT,
  'username' VARCHAR(45) NOT NULL,
  'institution_name' VARCHAR(100) NOT NULL,
  'institution_type' INT NOT NULL,
  'contact_person' VARCHAR(45) NOT NULL,
  'email_address' VARCHAR(45) NOT NULL,
  'phone_number' VARCHAR(45) NOT NULL,
  'mobile_number' VARCHAR(45) NOT NULL,
  PRIMARY KEY ('user_id'),
  UNIQUE INDEX 'username_UNIQUE' ('username' ASC),
  INDEX 'institutiion_type_id_idx' ('instituation_type' ASC),
  CONSTRAINT 'institutiion_type_id'
    FOREIGN KEY ('instituation_type')
    REFERENCES 'institution_type' ('institution_type_id')
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE TABLE 'stock' (
  'supplier_id' INT NOT NULL AUTO_INCREMENT,
  'medicine_id' INT NOT NULL,
  'gtin' BIGINT(11) NOT NULL,
  'amount_packages' VARCHAR(45) NOT NULL,
  'amount_units' VARCHAR(45) NOT NULL,
  'unit_size' VARCHAR(45) NOT NULL,
  'unit_id' INT NOT NULL,
  PRIMARY KEY ('supplier_id', 'medicine_id', 'gtin'),
  INDEX 'unit_id_idx' ('unit_id' ASC),
  INDEX 'medicine_id_idx' ('medicine_id' ASC),
  CONSTRAINT 'user_id'
    FOREIGN KEY ('supplier_id')
    REFERENCES 'user' ('user_id')
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT 'medicine_id'
    FOREIGN KEY ('medicine_id')
    REFERENCES 'medicine' ('medicine_id')
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT 'unit_id'
    FOREIGN KEY ('unit_id')
    REFERENCES 'unit' ('unit_id')
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
