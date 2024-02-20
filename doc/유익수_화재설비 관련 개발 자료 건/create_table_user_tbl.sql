CREATE TABLE `user_tbl` (
`user_id` varchar(10) NOT NULL,
`user_pwd` varchar(10) NOT NULL,
`user_name` varchar(45) NOT NULL,
`user_status` tinyint(1) NOT NULL DEFAULT 1,
`user_role` tinyint(1) NOT NULL DEFAULT 1,
PRIMARY KEY (`user_id`),
UNIQUE KEY `user_id_UNIQUE` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci