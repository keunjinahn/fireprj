-- --------------------------------------------------------
-- 호스트:                          localhost
-- 서버 버전:                        11.2.2-MariaDB - mariadb.org binary distribution
-- 서버 OS:                        Win64
-- HeidiSQL 버전:                  12.3.0.6589
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- fireprjdb 데이터베이스 구조 내보내기
CREATE DATABASE IF NOT EXISTS `fireprjdb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `fireprjdb`;

-- 테이블 fireprjdb.customer_tbl 구조 내보내기
CREATE TABLE IF NOT EXISTS `customer_tbl` (
  `customer_idx` smallint(5) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(45) NOT NULL,
  `customer_tel` varchar(12) NOT NULL,
  `customer_address` varchar(45) NOT NULL,
  PRIMARY KEY (`customer_idx`),
  UNIQUE KEY `customer_idx_UNIQUE` (`customer_idx`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 테이블 데이터 fireprjdb.customer_tbl:~2 rows (대략적) 내보내기
INSERT INTO `customer_tbl` (`customer_idx`, `customer_name`, `customer_tel`, `customer_address`) VALUES
	(00001, '1', '1', '1'),
	(00002, '2', '2', '2');

-- 테이블 fireprjdb.event_log_tbl 구조 내보내기
CREATE TABLE IF NOT EXISTS `event_log_tbl` (
  `event_log_idx` bigint(20) NOT NULL AUTO_INCREMENT,
  `fk_customer_idx` smallint(5) unsigned zerofill NOT NULL,
  `event_id` tinyint(3) unsigned zerofill NOT NULL,
  `receiver_type` tinyint(2) unsigned zerofill NOT NULL,
  `receiver_id` tinyint(2) unsigned zerofill NOT NULL,
  `system_id` tinyint(2) unsigned zerofill NOT NULL DEFAULT 00,
  `repeater_id` tinyint(2) unsigned zerofill NOT NULL,
  `sensor_id` tinyint(2) unsigned zerofill NOT NULL,
  `sensor_value` smallint(2) unsigned zerofill NOT NULL DEFAULT 00,
  `inout_id` tinyint(2) unsigned zerofill NOT NULL DEFAULT 00,
  `event_datetime` datetime NOT NULL,
  PRIMARY KEY (`event_log_idx`),
  UNIQUE KEY `event_log_idx_UNIQUE` (`event_log_idx`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 테이블 데이터 fireprjdb.event_log_tbl:~3 rows (대략적) 내보내기
INSERT INTO `event_log_tbl` (`event_log_idx`, `fk_customer_idx`, `event_id`, `receiver_type`, `receiver_id`, `system_id`, `repeater_id`, `sensor_id`, `sensor_value`, `inout_id`, `event_datetime`) VALUES
	(1, 00001, 001, 01, 01, 00, 01, 01, 01, 00, '2024-02-21 18:14:53'),
	(2, 00002, 002, 02, 02, 00, 02, 02, 00, 00, '2024-02-21 20:33:23'),
	(3, 00001, 001, 01, 01, 01, 01, 01, 01, 00, '2024-02-23 00:00:00');

-- 테이블 fireprjdb.event_tbl 구조 내보내기
CREATE TABLE IF NOT EXISTS `event_tbl` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event_idx` char(12) NOT NULL,
  `fk_customer_idx` smallint(5) unsigned zerofill NOT NULL,
  `receiver_type` tinyint(2) unsigned zerofill NOT NULL,
  `event_type` tinyint(2) unsigned zerofill NOT NULL,
  `event_id` tinyint(3) unsigned zerofill NOT NULL,
  `sensor_id` tinyint(2) unsigned zerofill NOT NULL DEFAULT 00,
  `event_desc` varchar(100) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 테이블 데이터 fireprjdb.event_tbl:~2 rows (대략적) 내보내기
INSERT INTO `event_tbl` (`id`, `event_idx`, `fk_customer_idx`, `receiver_type`, `event_type`, `event_id`, `sensor_id`, `event_desc`) VALUES
	(1, '01-01-001-00', 00001, 01, 01, 001, 00, '1'),
	(2, '01-01-002-00', 00001, 01, 01, 002, 00, '1');

-- 테이블 fireprjdb.fire_receiver_tbl 구조 내보내기
CREATE TABLE IF NOT EXISTS `fire_receiver_tbl` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `receiver_idx` char(11) NOT NULL,
  `fk_customer_idx` smallint(5) unsigned zerofill NOT NULL,
  `receiver_type` tinyint(2) unsigned zerofill NOT NULL,
  `receiver_id` tinyint(2) unsigned zerofill NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 테이블 데이터 fireprjdb.fire_receiver_tbl:~1 rows (대략적) 내보내기
INSERT INTO `fire_receiver_tbl` (`id`, `receiver_idx`, `fk_customer_idx`, `receiver_type`, `receiver_id`) VALUES
	(1, '1', 00001, 01, 01);

-- 테이블 fireprjdb.fire_repeater_tbl 구조 내보내기
CREATE TABLE IF NOT EXISTS `fire_repeater_tbl` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `repeater_idx` char(11) NOT NULL,
  `fk_customer_idx` smallint(5) unsigned zerofill NOT NULL,
  `receiver_id` tinyint(2) unsigned zerofill NOT NULL,
  `system_id` tinyint(2) unsigned zerofill NOT NULL DEFAULT 00,
  `repeater_id` tinyint(2) unsigned zerofill NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 테이블 데이터 fireprjdb.fire_repeater_tbl:~1 rows (대략적) 내보내기
INSERT INTO `fire_repeater_tbl` (`id`, `repeater_idx`, `fk_customer_idx`, `receiver_id`, `system_id`, `repeater_id`) VALUES
	(1, '1', 00001, 01, 00, 01);

-- 테이블 fireprjdb.fire_sensor_tbl 구조 내보내기
CREATE TABLE IF NOT EXISTS `fire_sensor_tbl` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sensor_idx` char(17) NOT NULL,
  `fk_customer_idx` smallint(5) unsigned zerofill NOT NULL,
  `receiver_id` tinyint(2) unsigned zerofill NOT NULL,
  `system_id` tinyint(2) unsigned zerofill NOT NULL DEFAULT 00,
  `repeater_id` tinyint(2) unsigned zerofill NOT NULL,
  `sensor_id` tinyint(2) unsigned zerofill NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 테이블 데이터 fireprjdb.fire_sensor_tbl:~3 rows (대략적) 내보내기
INSERT INTO `fire_sensor_tbl` (`id`, `sensor_idx`, `fk_customer_idx`, `receiver_id`, `system_id`, `repeater_id`, `sensor_id`) VALUES
	(1, '1', 00001, 01, 00, 01, 01),
	(2, '2', 00001, 01, 00, 01, 02),
	(3, '3', 00001, 01, 00, 01, 03);

-- 테이블 fireprjdb.user_tbl 구조 내보내기
CREATE TABLE IF NOT EXISTS `user_tbl` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(10) NOT NULL,
  `user_pwd` varchar(10) NOT NULL,
  `user_name` varchar(45) NOT NULL,
  `user_status` tinyint(1) NOT NULL DEFAULT 1,
  `user_role` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 테이블 데이터 fireprjdb.user_tbl:~1 rows (대략적) 내보내기
INSERT INTO `user_tbl` (`id`, `user_id`, `user_pwd`, `user_name`, `user_status`, `user_role`) VALUES
	(1, '1', '1', '1', 1, 1);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
