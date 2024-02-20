CREATE TABLE `event_tbl` (
`event_idx` char(12) NOT NULL,
`receiver_type` tinyint(2) unsigned zerofill NOT NULL, 
`event_type` tinyint(2) unsigned zerofill NOT NULL, 
`event_id` tinyint(3) unsigned zerofill NOT NULL, 
`sensor_id` tinyint(2) unsigned zerofill NOT NULL DEFAULT 00, 
`event_desc` varchar(100) NOT NULL, 
PRIMARY KEY (`event_idx`),
UNIQUE KEY `event_idx_UNIQUE` (`event_idx`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci