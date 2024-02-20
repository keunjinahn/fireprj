CREATE TABLE `fire_repeater_tbl` (
`repeater_idx` char(11) NOT NULL,
`customer_idx` smallint(5) unsigned zerofill NOT NULL, 
`receiver_id` tinyint(2) unsigned zerofill NOT NULL, 
`system_id` tinyint(2) unsigned zerofill NOT NULL DEFAULT 00, 
`repeater_id` tinyint(2) unsigned zerofill NOT NULL, 
PRIMARY KEY (`repeater_idx`),
UNIQUE KEY `repeater_idx_UNIQUE` (`repeater_idx`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci