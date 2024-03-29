CREATE TABLE `str_id` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`str` VARCHAR(16) NOT NULL COLLATE 'utf8mb4_general_ci',
	PRIMARY KEY (`id`) USING BTREE,
	UNIQUE INDEX `str` (`str`) USING BTREE
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
;
CREATE TABLE `market_data` (
	`symbol_id` INT(11) NOT NULL,
	`time` DATETIME NOT NULL,
	`open` DOUBLE NOT NULL,
	`high` DOUBLE NOT NULL,
	`low` DOUBLE NOT NULL,
	`close` DOUBLE NOT NULL,
	`volume` DOUBLE NOT NULL,
	`updated` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
	PRIMARY KEY (`symbol_id`, `time`) USING BTREE,
	CONSTRAINT `market_data_ibfk_1` FOREIGN KEY (`symbol_id`) REFERENCES `str_id` (`id`) ON UPDATE RESTRICT ON DELETE CASCADE
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
;


CREATE TABLE `ref_currency4` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`symbol` VARCHAR(16) NOT NULL COLLATE 'utf8mb4_general_ci',
	`prec` TINYINT(2) NULL DEFAULT NULL COMMENT 'Precision',
	`is_stable_coin` BIT(1) NULL DEFAULT NULL,
	`is_fiat` BIT(1) NULL DEFAULT NULL,
	`start_timestamp` TIMESTAMP(6) GENERATED ALWAYS AS ROW START,
   `end_timestamp` TIMESTAMP(6) GENERATED ALWAYS AS ROW END,
   PERIOD FOR SYSTEM_TIME(start_timestamp, end_timestamp),
	PRIMARY KEY (`id`) USING BTREE,
	UNIQUE INDEX `symbol` (`symbol`) USING BTREE
)
COLLATE='utf8mb4_general_ci'
ENGINE=INNODB
WITH SYSTEM VERSIONING
;



