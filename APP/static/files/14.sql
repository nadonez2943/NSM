CREATE DATABASE  IF NOT EXISTS `nsm_project` /*!40100 DEFAULT CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `nsm_project`;
-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: nsm_project
-- ------------------------------------------------------
-- Server version	8.0.30

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `board`
--

DROP TABLE IF EXISTS `board`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `board` (
  `bo_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `pj_id` int DEFAULT NULL,
  `role_id` int DEFAULT NULL,
  `bo_phase` int DEFAULT NULL,
  PRIMARY KEY (`bo_id`)
) ENGINE=InnoDB AUTO_INCREMENT=82 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `board`
--

LOCK TABLES `board` WRITE;
/*!40000 ALTER TABLE `board` DISABLE KEYS */;
INSERT INTO `board` VALUES (3,1,2,2,1),(4,2,2,1,1),(5,3,3,2,1),(6,2,3,1,1),(7,1,3,2,1),(8,4,1,3,1),(9,4,2,3,1),(10,4,3,3,1),(14,2,2,1,2),(15,3,2,1,3),(56,1,1,1,2),(58,2,1,2,2),(59,3,1,1,3),(61,1,1,2,3),(62,2,1,2,1),(63,1,1,1,1),(77,3,7,2,1),(78,1,7,2,1),(79,4,7,3,1),(80,5,7,2,1),(81,2,7,1,1);
/*!40000 ALTER TABLE `board` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `checks`
--

DROP TABLE IF EXISTS `checks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `checks` (
  `check_id` int NOT NULL AUTO_INCREMENT,
  `pj_id` int DEFAULT NULL,
  `ins_no` int DEFAULT NULL,
  `conNo` int DEFAULT NULL,
  `check_date` date DEFAULT NULL,
  `check_detail` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ins_date` date DEFAULT NULL,
  `ins_amount` int DEFAULT NULL,
  `ins_detail` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`check_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `checks`
--

LOCK TABLES `checks` WRITE;
/*!40000 ALTER TABLE `checks` DISABLE KEYS */;
/*!40000 ALTER TABLE `checks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contractor`
--

DROP TABLE IF EXISTS `contractor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contractor` (
  `contt_id` int NOT NULL AUTO_INCREMENT,
  `contt_name` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `contt_address` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `contt_tel` int DEFAULT NULL,
  `contt_email` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `contt_date` date DEFAULT NULL,
  `contt_start` date DEFAULT NULL,
  `contt_end` date DEFAULT NULL,
  PRIMARY KEY (`contt_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contractor`
--

LOCK TABLES `contractor` WRITE;
/*!40000 ALTER TABLE `contractor` DISABLE KEYS */;
INSERT INTO `contractor` VALUES (1,'บริษัท จำกัด ไม่จำกัด','Asguard',22212121,'hi5@email.com','2023-01-05','2023-01-22','2023-02-22');
/*!40000 ALTER TABLE `contractor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `division`
--

DROP TABLE IF EXISTS `division`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `division` (
  `dv_id` int NOT NULL AUTO_INCREMENT,
  `of_id` int DEFAULT NULL,
  `dv_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `dv_shname` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`dv_id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `division`
--

LOCK TABLES `division` WRITE;
/*!40000 ALTER TABLE `division` DISABLE KEYS */;
INSERT INTO `division` VALUES (1,1,'กองวิชาการวิทยาศาสตร์','วท.'),(2,1,'กองวิชาการเทคโนโลยิและนวัตกรรม','วน.'),(3,1,'กองวิชาการประวิติวิทยาศาสตร์และภูมิปัญญาไทย','วภ.'),(4,1,'ศูนย์บริหารคลังตัวอย่างและฐานข้อมูลพิพิธภัณฑ์วิทยาศาสตร์','ศว.'),(5,2,'กองวิชาการพฤกษศาสตร์','วพ.'),(6,2,'กองวิชาการสัตววิทยา','วส.'),(7,2,'กองนิเวศวิทยา','นว.'),(8,2,'ศูนย์บริหารคลังตัวอย่างทางธรรมชาติวิทยาศาสตร์และสัตว์สตัฟฟ์','ศธ.'),(9,3,'กองออกแบบและผลิต','กอ.'),(10,3,'กองเทคโนโลยีดิจิทัล','กท.'),(11,3,'กองกายภาพและสิ่งแวดล้อม','กส.'),(12,4,'กองยุทศาสตร์และความเสี่ยงองค์กร','กย.'),(13,4,'กองแผนและงบประมาณ','กผ.'),(14,4,'กองติดตามและประเมิณผล','กป.'),(15,5,'กองวิจัยและบริการวิชาการ','วบ.'),(16,5,'กองสื่อสารวิทยาศาสตร์','สว.'),(17,5,'กองส่งเสริมการเรียนรู้','สร.'),(18,6,'กองสารสนเทศการตลาด','กต.'),(19,6,'กองพัฒนาธุรกิจ','กธ.'),(20,6,'กองความร่วมมือและวิเทศสัมพันธ์','กว.'),(21,7,'กองคาราวานวิทยาศาสตร์','กค.'),(22,7,'กองจัตุรัสวิทยาศาสตร์','จว.'),(23,7,'กองส่งเสริมพัมนาทักษะอนาคต','สท.'),(24,8,'กองตรวจสอบด้านบัญชีการเงิน','ตง.'),(25,8,'กองตรวจสอบด้านปฏิบัติการและดิจิทัล','ตป.'),(26,9,'กองโครงการพิเศษ','คพ.'),(27,9,'กองสื่อสารองค์กร','สส.'),(28,9,'กองคณะกรรมการและการกำกับดูแลที่ดี','คก.'),(29,9,'กองกฎหมาย','กม.'),(30,10,'กองกลาง','กก.'),(31,10,'กองทรัพยากรบุคคล','กบ.'),(32,10,'กองการเงินและบันชี','กง.'),(33,10,'กองการพัสดุ','กพ.'),(34,11,'กองจัดระบบบริการผู้เข้าชม','จช.'),(35,11,'กองอาสาสมัคร','อส.'),(36,11,'กองบริการลูกค้าสัมพันธ์','บค.');
/*!40000 ALTER TABLE `division` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `events` (
  `ev_id` int NOT NULL AUTO_INCREMENT,
  `pj_id` int DEFAULT NULL,
  `ev_name` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ev_phase` int DEFAULT NULL,
  `ev_date` date DEFAULT NULL,
  `ev_detail` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ev_time` time DEFAULT NULL,
  PRIMARY KEY (`ev_id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events`
--

LOCK TABLES `events` WRITE;
/*!40000 ALTER TABLE `events` DISABLE KEYS */;
INSERT INTO `events` VALUES (1,1,'ประชุมครั้งที่ 1',1,'2022-09-24',' มี','15:30:00'),(2,2,'ประชุม 2',1,'2022-11-05','เรื่องงบประมาณ','12:00:00'),(3,3,'ประชุม 3 ',1,'2022-08-09','สังสรรค์','13:00:00'),(4,3,'ประชุม 4',2,'2022-09-11','เรื่องบริษัท','10:30:00'),(5,2,'ประชุม 5',2,'2022-10-06','เรื่องอะไรดี','15:00:00'),(8,1,'ประชุม 8',1,'2029-04-05','ยู้ฮู','14:30:00'),(23,2,'zdfg',1,'2022-09-20','arag','07:00:00'),(24,2,'afg',1,'2022-09-20','asfdgs',NULL),(25,2,'sdag',2,'2022-09-29','afgadfg',NULL),(26,2,'ประชุม',3,'2022-09-14','การเงิน','12:00:00'),(27,3,'ประชุมใหม่',3,'2022-10-05','การประชุม','12:00:00'),(31,4,'1',1,'2022-10-20','12','15:00:00'),(32,4,'2',1,'2022-10-27','21','11:00:00'),(33,4,'3',1,'2022-10-27','123','04:00:00'),(34,4,'4',2,'2022-10-06','51','01:00:00'),(35,4,'5',3,'2022-10-27','42','05:00:00');
/*!40000 ALTER TABLE `events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login` (
  `login_id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `login_dateTime` datetime(6) DEFAULT NULL,
  `logout_dateTime` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login`
--

LOCK TABLES `login` WRITE;
/*!40000 ALTER TABLE `login` DISABLE KEYS */;
/*!40000 ALTER TABLE `login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `manager`
--

DROP TABLE IF EXISTS `manager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `manager` (
  `mn_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `pj_id` int DEFAULT NULL,
  PRIMARY KEY (`mn_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `manager`
--

LOCK TABLES `manager` WRITE;
/*!40000 ALTER TABLE `manager` DISABLE KEYS */;
INSERT INTO `manager` VALUES (1,1,1),(2,1,2),(3,1,3),(4,1,4),(5,1,5),(6,1,6),(7,1,7);
/*!40000 ALTER TABLE `manager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `office`
--

DROP TABLE IF EXISTS `office`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `office` (
  `of_id` int NOT NULL,
  `of_name` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `of_shname` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`of_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `office`
--

LOCK TABLES `office` WRITE;
/*!40000 ALTER TABLE `office` DISABLE KEYS */;
INSERT INTO `office` VALUES (1,'สำนักงานวิชาการพิพิธภัณฑ์วิทยาศาสตร์แห่งชาติ','สพว.'),(2,'สำนักงานวิชาการพิพิธภัณฑ์ธรรมชาติวิทยา','สพธ.'),(3,'สำนักวิศวกรรมและการผลิตสื่อ','สวส.'),(4,'สำนักนโยบายและยุทศาสตร์','สนย.'),(5,'ศูนย์พัฒนาความตระหนักด้านวิทยาศาสตร์แห่งชาติ','ศพช.'),(6,'สำนักพัฒนาธุรกิจและเครือข่าย','สธค.'),(7,'สำนักวิทยาศาสตร์สู่ชุมชน','สวช.'),(8,'สำนักตรวจสอบภายใน','สตน.'),(9,'สำนักผู้อำนวยการ','สอก.'),(10,'สำนักบริการกลาง','สบก.'),(11,'สำนักบริการผู้เข้าชม','สบช.');
/*!40000 ALTER TABLE `office` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pacel`
--

DROP TABLE IF EXISTS `pacel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pacel` (
  `pac_id` int NOT NULL AUTO_INCREMENT,
  `pj_id` int DEFAULT NULL,
  `pac_detail` varchar(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `pac_date` date DEFAULT NULL,
  PRIMARY KEY (`pac_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pacel`
--

LOCK TABLES `pacel` WRITE;
/*!40000 ALTER TABLE `pacel` DISABLE KEYS */;
INSERT INTO `pacel` VALUES (1,1,'ขออนุมัติประกาศเผยแพร่แผนการจัดซื้อจัดจ้าง อนุมัติ ','2022-05-19');
/*!40000 ALTER TABLE `pacel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `path`
--

DROP TABLE IF EXISTS `path`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `path` (
  `path_id` int NOT NULL AUTO_INCREMENT,
  `pj_id` int DEFAULT NULL,
  `path_phase` int DEFAULT NULL,
  `path_path` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `path_name` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `path_detail` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`path_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `path`
--

LOCK TABLES `path` WRITE;
/*!40000 ALTER TABLE `path` DISABLE KEYS */;
/*!40000 ALTER TABLE `path` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `process`
--

DROP TABLE IF EXISTS `process`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `process` (
  `pc_id` int NOT NULL AUTO_INCREMENT,
  `pj_id` int DEFAULT NULL,
  `stdraft_id` int DEFAULT '1',
  `stcon_id` int DEFAULT '1',
  `stex_id` int DEFAULT '1',
  `contt_id` int DEFAULT NULL,
  `startproject_date` date DEFAULT NULL,
  `endproject_date` date DEFAULT NULL,
  `start_draft` date DEFAULT NULL,
  `end_draft_date` date DEFAULT NULL,
  `end_draft_time` time DEFAULT NULL,
  `draftapp_status` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `PMcheck` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  PRIMARY KEY (`pc_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `process`
--

LOCK TABLES `process` WRITE;
/*!40000 ALTER TABLE `process` DISABLE KEYS */;
INSERT INTO `process` VALUES (1,1,6,4,4,1,'2022-12-11',NULL,'2022-10-12',NULL,NULL,'yes',NULL),(2,2,6,2,1,1,'2022-11-10',NULL,'2022-10-11',NULL,NULL,'yes',NULL),(3,3,4,4,2,1,'2022-06-15',NULL,'2022-07-30',NULL,NULL,NULL,NULL),(4,4,6,6,4,2,'2022-10-06',NULL,'2022-10-10',NULL,NULL,'yes',NULL),(5,5,1,1,1,NULL,'2022-10-12',NULL,NULL,NULL,NULL,NULL,NULL),(6,6,4,1,1,NULL,'2022-10-17',NULL,'2022-10-17',NULL,NULL,'',NULL),(7,7,3,1,1,NULL,'2022-10-18',NULL,'2022-10-18','0000-00-00','00:00:00','yes','wait');
/*!40000 ALTER TABLE `process` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects` (
  `pj_id` int NOT NULL AUTO_INCREMENT,
  `pj_refNumber` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `of_id` int DEFAULT NULL,
  `dv_id` int DEFAULT NULL,
  `pj_type` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `pj_name` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `pj_amount` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  `pj_detail` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `pj_financeAmount` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  `pj_budgetSource` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `pj_budgetYears` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`pj_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects`
--

LOCK TABLES `projects` WRITE;
/*!40000 ALTER TABLE `projects` DISABLE KEYS */;
INSERT INTO `projects` VALUES (1,'ดก1222',1,5,'จัดซื้อ','จัดซื้อเครื่องทำอากาศ','200000','เครื่องทำอากาศสำหรับภายในสำนักงาน','2000','ใต้ดิน','2050'),(2,'สก2121',2,4,'จัดซื้อ','จัดซื้อเครื่องปริ้นท์','10000000','เครื่องปริ้นท์รุ่นใหม่ภายในองค์กรณ์','60000','นอกอวกาศ','2045'),(3,'มน5554',3,3,'จัดจ้าง','ติดตั้งคอมพิวเตอร์','574684','คอมพิวเตอร์จาก JIB','6251','บนพื้นโลก','2022'),(4,'sdgag',4,12,'จัดซื้อ','dfgsdfgh','13246',NULL,'1565','5864','2022'),(6,'sdfsd',2,5,'จัดซื้อ','sdfsd','521','sdf','85','ลงทุน','2565'),(7,'test1',1,1,'จัดจ้าง','tt','5000','tttt','5000','ดำเนินการ','2565');
/*!40000 ALTER TABLE `projects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `status_consider`
--

DROP TABLE IF EXISTS `status_consider`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `status_consider` (
  `stcon_id` int NOT NULL AUTO_INCREMENT,
  `stcon_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `stcon_percent` float DEFAULT NULL,
  PRIMARY KEY (`stcon_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_consider`
--

LOCK TABLES `status_consider` WRITE;
/*!40000 ALTER TABLE `status_consider` DISABLE KEYS */;
INSERT INTO `status_consider` VALUES (1,'-',0),(2,'กองพัสดุกำลังดำเนินการ',20),(3,'ดำเนินการพิจารณาผล',40),(4,'กองพัสดุกำลังดำเนินงาน',60),(5,'รออุทร',80),(6,'เสร็จสิ้น',100);
/*!40000 ALTER TABLE `status_consider` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `status_draft`
--

DROP TABLE IF EXISTS `status_draft`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `status_draft` (
  `stdraft_id` int NOT NULL AUTO_INCREMENT,
  `stdraft_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `stdraft_percent` float DEFAULT NULL,
  PRIMARY KEY (`stdraft_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_draft`
--

LOCK TABLES `status_draft` WRITE;
/*!40000 ALTER TABLE `status_draft` DISABLE KEYS */;
INSERT INTO `status_draft` VALUES (1,'รอกำหนดคณะกรรมการร่าง TOR',0),(2,'ดำเนินการร่าง TOR และราคากลาง',25),(3,'ดำเนินการขออนุมัติ TOR',50),(4,'TOR ได้รับอนุมัติ',75),(5,'เสร็จสิ้นกระบวนการร่าง TOR และราคากลาง',100);
/*!40000 ALTER TABLE `status_draft` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `status_examine`
--

DROP TABLE IF EXISTS `status_examine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `status_examine` (
  `stex_id` int NOT NULL AUTO_INCREMENT,
  `stex_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `stex_percent` float DEFAULT NULL,
  PRIMARY KEY (`stex_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_examine`
--

LOCK TABLES `status_examine` WRITE;
/*!40000 ALTER TABLE `status_examine` DISABLE KEYS */;
INSERT INTO `status_examine` VALUES (1,'-',0),(2,'ดำเนินการตรวจรับ',33.33),(3,'สรุปผล บัญทึกข้อมูล',66.67),(4,'เสร็จสิ้น',100);
/*!40000 ALTER TABLE `status_examine` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_role`
--

DROP TABLE IF EXISTS `tbl_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tbl_role` (
  `role_id` int NOT NULL AUTO_INCREMENT,
  `role_name` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_role`
--

LOCK TABLES `tbl_role` WRITE;
/*!40000 ALTER TABLE `tbl_role` DISABLE KEYS */;
INSERT INTO `tbl_role` VALUES (1,'ประธาน'),(2,'กรรมการ'),(3,'เลขาธิการ');
/*!40000 ALTER TABLE `tbl_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_fullname` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_email` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_password` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_role` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `tel` int DEFAULT NULL,
  `of_id` int DEFAULT NULL,
  `dv_id` int DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'user1','พงศกร จันทร์สว่าง','aa@email.com','123','user',2122333,1,2),(2,'user2','นฤดล เจริญรุ่งเรือง','bb@email.com','123','user',6145216,3,10),(3,'user3','พีรพล พาร์คเกอร์','cc@email.com','123','user',5412356,4,12),(4,'user4','ปาริฉัตร นาราทิพย์','dd@email.com','123','user',23134643,10,30),(5,'user5','บำเพ็ญเพียร ภาวนา','ee@email.com','123','user',9874644,5,17);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-10-19  1:37:45
