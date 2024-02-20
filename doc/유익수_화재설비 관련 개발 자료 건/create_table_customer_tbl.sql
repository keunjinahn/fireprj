CREATE TABLE `customer_tbl` (
  `customer_idx` smallint(5) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(45) NOT NULL,
  `customer_tel` varchar(12) NOT NULL,
  `customer_address` varchar(45) NOT NULL,
  PRIMARY KEY (`customer_idx`),
  UNIQUE KEY `customer_idx_UNIQUE` (`customer_idx`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci