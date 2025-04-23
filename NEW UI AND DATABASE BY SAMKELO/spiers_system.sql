/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.7.2-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: spiers_system
-- ------------------------------------------------------
-- Server version	11.7.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `operations`
--

DROP TABLE IF EXISTS `operations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `operations` (
  `operation_id` int(11) NOT NULL AUTO_INCREMENT,
  `technician_id` varchar(50) NOT NULL,
  `location` varchar(100) DEFAULT NULL,
  `action` varchar(50) NOT NULL,
  `barcode` varchar(50) DEFAULT NULL,
  `new_location` varchar(100) DEFAULT NULL,
  `source` varchar(50) DEFAULT NULL,
  `destination` varchar(100) DEFAULT NULL,
  `battery_condition` varchar(50) DEFAULT NULL,
  `photo_path` varchar(255) DEFAULT NULL,
  `reaction` text DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`operation_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operations`
--

LOCK TABLES `operations` WRITE;
/*!40000 ALTER TABLE `operations` DISABLE KEYS */;
INSERT INTO `operations` VALUES
(1,'testuser','New Battery Section','Receive','ert784t7385y432',NULL,'Supplier',NULL,NULL,'photo_20250421_235424.jpg','I feel good about Receive because it’s new.','2025-04-22 04:54:53'),
(2,'testuser','Old Battery Section','Receive','89868809-0-',NULL,'Supplier',NULL,NULL,'photo_20250422_002502.jpg','I feel 9 about Receive because it’s rewarding.','2025-04-22 05:26:05'),
(3,'','','','',NULL,NULL,NULL,NULL,NULL,NULL,'2025-04-22 05:44:39'),
(4,'','','','',NULL,NULL,NULL,NULL,NULL,NULL,'2025-04-22 05:48:51'),
(5,'testuser','Old Battery Section','Ship','576890',NULL,NULL,'Dealership B',NULL,'photo_20250422_011440.jpg','I feel good about Ship because it’s happy.','2025-04-22 06:14:56'),
(6,'testuser','Old Battery Section','Receive','erwq25643',NULL,'Supplier',NULL,NULL,'photo_20250423_105704.jpg','I feel good about Receive because it’s easy.','2025-04-23 15:57:23'),
(7,'testuser','Old Battery Section','Move','r345392456754e','Old Battery Section',NULL,NULL,NULL,'photo_20250423_111800.jpg','I feel good about Move because it’s easy.','2025-04-23 16:18:16'),
(8,'testuser','Old Battery Section','Receive','24356754',NULL,'Supplier',NULL,NULL,'photo_20250423_121958.jpg','I feel good about Receive because it’s new.','2025-04-23 17:20:17'),
(9,'testuser','Old Battery Section','Receive','75992436',NULL,'Supplier',NULL,NULL,'photo_20250423_124753.jpg','I feel Tired about Receive because it’s cold.','2025-04-23 17:48:08');
/*!40000 ALTER TABLE `operations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
('tech01','32250170a0dca92d53ec9624f336ca24bb5e26d7f36d6d3f44f4c9d5286d38'),
('testuser','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2025-04-23 14:52:56
