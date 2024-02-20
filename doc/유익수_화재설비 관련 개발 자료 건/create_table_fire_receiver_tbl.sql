CREATE TABLE `fire_receiver_tbl` (
`receiver_idx` char(11) NOT NULL, 
`customer_idx` smallint(5) unsigned zerofill NOT NULL, 
`receiver_type` tinyint(2) unsigned zerofill NOT NULL, 
`receiver_id` tinyint(2) unsigned zerofill NOT NULL, 
PRIMARY KEY (`receiver_idx`),
UNIQUE KEY `receiver_idx_UNIQUE` (`receiver_idx`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci