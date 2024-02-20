CREATE TABLE `fire_sensor_tbl` (
`sensor_idx` char(17) NOT NULL, 
`customer_idx` smallint(5) unsigned zerofill NOT NULL, 
`receiver_id` tinyint(2) unsigned zerofill NOT NULL, 
`system_id` tinyint(2) unsigned zerofill NOT NULL DEFAULT 00, 
`repeater_id` tinyint(2) unsigned zerofill NOT NULL, 
`sensor_id` tinyint(2) unsigned zerofill NOT NULL, 
PRIMARY KEY (`sensor_idx`),
UNIQUE KEY `sensor_idx_UNIQUE` (`sensor_idx`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci