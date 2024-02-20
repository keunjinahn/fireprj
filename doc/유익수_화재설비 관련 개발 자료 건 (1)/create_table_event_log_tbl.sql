CREATE TABLE `event_log_tbl` (
`event_log_idx` bigint(20) NOT NULL AUTO_INCREMENT, 
`customer_idx` smallint(5) unsigned zerofill NOT NULL,
`event_id` tinyint(3) unsigned zerofill NOT NULL, 
`receiver_type` tinyint(2) unsigned zerofill NOT NULL, 
`receiver_id` tinyint(2) unsigned zerofill NOT NULL, 
`system_id` tinyint(2) unsigned zerofill NOT NULL DEFAULT 0, 
`repeater_id` tinyint(2) unsigned zerofill NOT NULL, 
`sensor_id` tinyint(2) unsigned zerofill NOT NULL, 
`sensor_value` smallint(2) zerofill NOT NULL, 
`inout_id` tinyint(2) unsigned zerofill NOT NULL DEFAULT 0, 
`event_datetime` datetime NOT NULL, 
PRIMARY KEY (`event_log_idx`),
UNIQUE KEY `event_log_idx_UNIQUE` (`event_log_idx`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci