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
	`str_id` INT(11) NOT NULL,
	`open_price` DOUBLE NOT NULL,
	`close_price` DOUBLE NOT NULL,
	`low_price` DOUBLE NOT NULL,
	`high_price` DOUBLE NOT NULL,
	`time` TIMESTAMP NOT NULL,
	PRIMARY KEY (`str_id`, `time`) USING BTREE,
	CONSTRAINT `market_data_ibfk_1` FOREIGN KEY (`str_id`) REFERENCES `str_id` (`id`) ON UPDATE RESTRICT ON DELETE CASCADE
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
;

INSERT INTO str_id (symbol)
VALUES ('AAPL')
ON DUPLICATE KEY UPDATE id = LAST_INSERT_ID(id);

INSERT INTO market_data (symbol_id, open_price, close_price, low_price, high_price, time)
VALUES (LAST_INSERT_ID(), 100.0, 105.0, 99.0, 110.0, '2023-03-14 12:00:00');



