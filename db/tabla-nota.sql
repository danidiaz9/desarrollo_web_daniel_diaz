-- Active: 1751401464644@@127.0.0.1@3306@tarea2
CREATE TABLE IF NOT EXISTS `tarea2`.`nota` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `actividad_id` INT NOT NULL,
  `nota` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_nota_actividad1_idx` (`actividad_id` ASC),
  CONSTRAINT `fk_nota_actividad1`
    FOREIGN KEY (`actividad_id`)
    REFERENCES `tarea2`.`actividad` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;