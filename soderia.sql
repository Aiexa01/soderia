-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: soderia
-- ------------------------------------------------------
-- Server version	8.0.45

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'Administrador'),(2,'Encargado de Atencion al Cliente'),(5,'Encargado de Stock'),(4,'Repartidor'),(3,'Tecnico');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add client',7,'add_client'),(26,'Can change client',7,'change_client'),(27,'Can delete client',7,'delete_client'),(28,'Can view client',7,'view_client'),(29,'Can add role meta',8,'add_rolemeta'),(30,'Can change role meta',8,'change_rolemeta'),(31,'Can delete role meta',8,'delete_rolemeta'),(32,'Can view role meta',8,'view_rolemeta'),(33,'Can add camioneta',9,'add_camioneta'),(34,'Can change camioneta',9,'change_camioneta'),(35,'Can delete camioneta',9,'delete_camioneta'),(36,'Can view camioneta',9,'view_camioneta'),(37,'Can add pedido',10,'add_pedido'),(38,'Can change pedido',10,'change_pedido'),(39,'Can delete pedido',10,'delete_pedido'),(40,'Can view pedido',10,'view_pedido'),(41,'Can add pedido estado',11,'add_pedidoestado'),(42,'Can change pedido estado',11,'change_pedidoestado'),(43,'Can delete pedido estado',11,'delete_pedidoestado'),(44,'Can view pedido estado',11,'view_pedidoestado'),(45,'Can add producto',12,'add_producto'),(46,'Can change producto',12,'change_producto'),(47,'Can delete producto',12,'delete_producto'),(48,'Can view producto',12,'view_producto'),(49,'Can add pedido detalle',13,'add_pedidodetalle'),(50,'Can change pedido detalle',13,'change_pedidodetalle'),(51,'Can delete pedido detalle',13,'delete_pedidodetalle'),(52,'Can view pedido detalle',13,'view_pedidodetalle'),(53,'Can add stock camioneta',14,'add_stockcamioneta'),(54,'Can change stock camioneta',14,'change_stockcamioneta'),(55,'Can delete stock camioneta',14,'delete_stockcamioneta'),(56,'Can view stock camioneta',14,'view_stockcamioneta'),(57,'Can add stock movimiento',15,'add_stockmovimiento'),(58,'Can change stock movimiento',15,'change_stockmovimiento'),(59,'Can delete stock movimiento',15,'delete_stockmovimiento'),(60,'Can view stock movimiento',15,'view_stockmovimiento'),(61,'Can add barrio',16,'add_barrio'),(62,'Can change barrio',16,'change_barrio'),(63,'Can delete barrio',16,'delete_barrio'),(64,'Can view barrio',16,'view_barrio'),(65,'Can add zona',17,'add_zona'),(66,'Can change zona',17,'change_zona'),(67,'Can delete zona',17,'delete_zona'),(68,'Can view zona',17,'view_zona'),(69,'Can add datos personales',18,'add_datospersonales'),(70,'Can change datos personales',18,'change_datospersonales'),(71,'Can delete datos personales',18,'delete_datospersonales'),(72,'Can view datos personales',18,'view_datospersonales'),(73,'Can add deposito',19,'add_deposito'),(74,'Can change deposito',19,'change_deposito'),(75,'Can delete deposito',19,'delete_deposito'),(76,'Can view deposito',19,'view_deposito'),(77,'Can add stock deposito',20,'add_stockdeposito'),(78,'Can change stock deposito',20,'change_stockdeposito'),(79,'Can delete stock deposito',20,'delete_stockdeposito'),(80,'Can view stock deposito',20,'view_stockdeposito'),(81,'Can add Consulta web',21,'add_consultaweb'),(82,'Can change Consulta web',21,'change_consultaweb'),(83,'Can delete Consulta web',21,'delete_consultaweb'),(84,'Can view Consulta web',21,'view_consultaweb');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$260000$lt0vIMARqz8uth1mtxtxzv$nLCA6psb029MoFrqlXUJMFjmwMO7SlD6i2uxq5kvhbE=','2026-02-17 20:22:57.270943',1,'admin','','','admin@gmail.com',1,1,'2026-02-17 20:22:49.326246'),(2,'pbkdf2_sha256$260000$aIzJxrU810VEpz1h9A7SSQ$svHJb5SEC3KTjXBCP60RZoNNwo/katxLRpknINK8ntg=','2026-04-09 21:40:38.061790',0,'marlene','Marlene Jerusalen','Altamirano','marlenejerusalen@gmail.com',0,1,'2026-02-17 20:37:24.996079'),(3,'pbkdf2_sha256$260000$XY8OMmFWM681kBirunfakS$CEA+3uxm5plHcbMoxHj3A/AyT+nmsQENrlXnEP96ywE=','2026-04-07 21:28:50.830168',0,'tomas','tomi','lopez','marlenejerusalen@gmail.com',0,1,'2026-04-01 19:16:06.465685'),(4,'pbkdf2_sha256$260000$wB1Sug5kUilqtmqZj5ZCoJ$iaImnOImdRXZdsjJljG6EmMu111KvjpOBkgjiBt4Gg8=','2026-04-07 21:32:52.582790',0,'rafa','rafael','Benavidez','rafa@gmail.com',0,1,'2026-04-07 21:32:33.362416');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (1,2,1),(2,3,3),(3,3,4),(4,4,5);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `barrio`
--

DROP TABLE IF EXISTS `barrio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `barrio` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(80) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `zona_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Proyecto_Soderia_barrio_nombre_zona_id_94bff9b2_uniq` (`nombre`,`zona_id`),
  KEY `Proyecto_Soderia_bar_zona_id_80e8fca8_fk_Proyecto_` (`zona_id`),
  CONSTRAINT `Proyecto_Soderia_bar_zona_id_80e8fca8_fk_Proyecto_` FOREIGN KEY (`zona_id`) REFERENCES `zona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `barrio`
--

LOCK TABLES `barrio` WRITE;
/*!40000 ALTER TABLE `barrio` DISABLE KEYS */;
/*!40000 ALTER TABLE `barrio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `camioneta`
--

DROP TABLE IF EXISTS `camioneta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `camioneta` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(120) NOT NULL,
  `patente` varchar(20) NOT NULL,
  `repartidor_id` int DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `estado` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `patente` (`patente`),
  KEY `Proyecto_Soderia_cam_repartidor_id_ec8030c4_fk_auth_user` (`repartidor_id`),
  CONSTRAINT `Proyecto_Soderia_cam_repartidor_id_ec8030c4_fk_auth_user` FOREIGN KEY (`repartidor_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `camioneta`
--

LOCK TABLES `camioneta` WRITE;
/*!40000 ALTER TABLE `camioneta` DISABLE KEYS */;
INSERT INTO `camioneta` VALUES (1,'Master 1','AD100MA',NULL,1,'DISPONIBLE'),(2,'Master 2','AD101MA',NULL,1,'DISPONIBLE'),(3,'Master 3','AD102MA',NULL,1,'DISPONIBLE'),(4,'Foton 1','AD200FO',3,1,'DISPONIBLE'),(5,'Foton 2','AD201FO',NULL,1,'DISPONIBLE'),(6,'Sprinter 1','AD300SP',NULL,1,'DISPONIBLE'),(7,'Sprinter 2','AD301SP',NULL,1,'DISPONIBLE'),(8,'Sprinter 3','AD302SP',NULL,1,'DISPONIBLE');
/*!40000 ALTER TABLE `camioneta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `camioneta_zonas`
--

DROP TABLE IF EXISTS `camioneta_zonas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `camioneta_zonas` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `camioneta_id` bigint NOT NULL,
  `zona_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Proyecto_Soderia_camione_camioneta_id_zona_id_d4a402bd_uniq` (`camioneta_id`,`zona_id`),
  KEY `Proyecto_Soderia_cam_zona_id_0a42be23_fk_Proyecto_` (`zona_id`),
  CONSTRAINT `Proyecto_Soderia_cam_camioneta_id_a5d70442_fk_Proyecto_` FOREIGN KEY (`camioneta_id`) REFERENCES `camioneta` (`id`),
  CONSTRAINT `Proyecto_Soderia_cam_zona_id_0a42be23_fk_Proyecto_` FOREIGN KEY (`zona_id`) REFERENCES `zona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `camioneta_zonas`
--

LOCK TABLES `camioneta_zonas` WRITE;
/*!40000 ALTER TABLE `camioneta_zonas` DISABLE KEYS */;
/*!40000 ALTER TABLE `camioneta_zonas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `client`
--

DROP TABLE IF EXISTS `client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `client` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `telefono` varchar(30) NOT NULL,
  `email` varchar(254) DEFAULT NULL,
  `direccion` varchar(200) NOT NULL,
  `referencias` longtext,
  `activo` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` datetime(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `tipo_cliente` varchar(20) NOT NULL,
  `tipo_documento` varchar(10) NOT NULL,
  `numero_documento` varchar(30) NOT NULL,
  `barrio_id` bigint DEFAULT NULL,
  `zona_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_documento` (`numero_documento`),
  KEY `fk_client_barrio` (`barrio_id`),
  KEY `fk_client_zona` (`zona_id`),
  CONSTRAINT `fk_client_barrio` FOREIGN KEY (`barrio_id`) REFERENCES `barrio` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_client_zona` FOREIGN KEY (`zona_id`) REFERENCES `zona` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client`
--

LOCK TABLES `client` WRITE;
/*!40000 ALTER TABLE `client` DISABLE KEYS */;
INSERT INTO `client` VALUES (1,'Ana Gomez','3875001001','','Av. Belgrano 1250','',1,'2026-03-11 12:34:24.975391','2026-03-11 12:34:24.975436','PERSONA','DNI','30100001',NULL,6),(2,'Luis Fernandez','3875001002','','Caseros 842','',1,'2026-03-11 12:34:24.983923','2026-03-11 12:34:24.983945','PERSONA','DNI','30100002',NULL,6),(3,'Maria Lopez','3875001003','','Dean Funes 1145','',1,'2026-03-11 12:34:24.992912','2026-03-11 12:34:24.992944','PERSONA','DNI','30100003',NULL,6),(4,'Carlos Ruiz','3875001004','','Alvarado 1678','',1,'2026-03-11 12:34:25.000472','2026-03-11 12:34:25.000496','PERSONA','DNI','30100004',NULL,6),(5,'Sofia Herrera','3875001005','','Mitre 932','',1,'2026-03-11 12:34:25.008422','2026-03-11 12:34:25.008446','PERSONA','DNI','30100005',NULL,6),(6,'Javier Sosa','3875001006','','España 1451','',1,'2026-03-11 12:34:25.016987','2026-03-11 12:34:25.017010','PERSONA','DNI','30100006',NULL,6),(7,'Lucia Torres','3875001007','','Leguizamon 621','',1,'2026-03-11 12:34:25.025639','2026-03-11 12:34:25.025663','PERSONA','DNI','30100007',NULL,6),(8,'Pablo Diaz','3875001008','','San Martin 1733','',1,'2026-03-11 12:34:25.033906','2026-03-11 09:35:29.349766','PERSONA','DNI','30100008',NULL,6),(9,'Valeria Cruz','3875001009','','20 de Febrero 518','',1,'2026-03-11 12:34:25.041697','2026-03-11 12:34:25.041720','PERSONA','DNI','30100009',NULL,6),(10,'Diego Navarro','3875001010','','Urquiza 1389','',1,'2026-03-11 12:34:25.050706','2026-03-11 12:34:25.050732','PERSONA','DNI','30100010',NULL,6),(11,'Paula Molina','3875001011','','Ituzaingo 744','',1,'2026-03-11 12:34:25.060158','2026-03-11 12:34:25.060189','PERSONA','DNI','30100011',NULL,6),(12,'Martin Vega','3875001012','','Corrientes 1610','',1,'2026-03-11 12:34:25.068479','2026-03-11 12:34:25.068502','PERSONA','DNI','30100012',NULL,6),(13,'Julieta Pereyra','3875001013','','Florida 980','',1,'2026-03-11 12:34:25.075754','2026-03-11 12:34:25.075777','PERSONA','DNI','30100013',NULL,6),(14,'Nicolas Castillo','3875001014','','Zabala 420','',1,'2026-03-11 12:34:25.083289','2026-03-11 12:34:25.083311','PERSONA','DNI','30100014',NULL,6),(15,'Camila Romero','3875001015','','Balcarce 1555','',1,'2026-03-11 12:34:25.091383','2026-03-11 12:34:25.091405','PERSONA','DNI','30100015',NULL,6),(16,'Federico Ramos','3875001016','','Ameghino 890','',1,'2026-03-11 12:34:25.111422','2026-03-11 12:34:25.111445','PERSONA','DNI','30100016',NULL,6),(17,'Micaela Vargas','3875001017','','Pellegrini 1332','',1,'2026-03-11 12:34:25.125349','2026-03-11 12:34:25.125379','PERSONA','DNI','30100017',NULL,6),(18,'Gonzalo Medina','3875001018','','Alsina 705','',1,'2026-03-11 12:34:25.133957','2026-03-11 12:34:25.133988','PERSONA','DNI','30100018',NULL,6),(19,'Florencia Acosta','3875001019','','Rivadavia 1499','',1,'2026-03-11 12:34:25.141775','2026-03-11 12:34:25.141798','PERSONA','DNI','30100019',NULL,6),(20,'Sebastian Ibarra','3875001020','','San Juan 812','',1,'2026-03-11 12:34:25.149758','2026-03-11 12:34:25.149780','PERSONA','DNI','30100020',NULL,6),(21,'Gabriela Silva','3875001021','','Tucuman 1246','',1,'2026-03-11 12:34:25.157747','2026-03-11 12:34:25.157770','PERSONA','DNI','30100021',NULL,6),(22,'Matias Arias','3875001022','','Mendoza 975','',1,'2026-03-11 12:34:25.165154','2026-03-11 12:34:25.165177','PERSONA','DNI','30100022',NULL,6),(23,'Noelia Cardozo','3875001023','','La Rioja 1418','',1,'2026-03-11 12:34:25.173914','2026-03-11 12:34:25.173939','PERSONA','DNI','30100023',NULL,6),(24,'Leandro Correa','3875001024','','Vicente Lopez 633','',1,'2026-03-11 12:34:25.182092','2026-03-11 12:34:25.182120','PERSONA','DNI','30100024',NULL,6),(25,'Rocio Figueroa','3875001025','','Catamarca 1564','',1,'2026-03-11 12:34:25.190482','2026-03-11 12:34:25.190514','PERSONA','DNI','30100025',NULL,6),(26,'Emanuel Aguirre','3875001026','','Santiago del Estero 845','',1,'2026-03-11 12:34:25.197986','2026-03-11 12:34:25.198012','PERSONA','DNI','30100026',NULL,6),(27,'Brenda Paz','3875001027','','Jujuy 1290','',1,'2026-03-11 12:34:25.206065','2026-03-11 12:34:25.206089','PERSONA','DNI','30100027',NULL,6),(28,'Facundo Salas','3875001028','','Olavarria 560','',1,'2026-03-11 12:34:25.213426','2026-03-11 12:34:25.213447','PERSONA','DNI','30100028',NULL,6),(29,'Daniela Toledo','3875001029','','Adolfo Guemes 1711','',1,'2026-03-11 12:34:25.221016','2026-03-11 12:34:25.221038','PERSONA','DNI','30100029',NULL,6),(30,'Ignacio Rojas','3875001030','','Entre Rios 1188','',1,'2026-03-11 12:34:25.228374','2026-03-11 12:34:25.228397','PERSONA','DNI','30100030',NULL,6),(31,'Claribel Perez','0387155385199','marlenejerusalen@gmail.com','Arenales 1789','Esta a la vuelta de la cancha',0,'2026-04-01 19:08:11.254153','2026-04-01 19:08:11.254177','PERSONA','DNI','45358896',NULL,1);
/*!40000 ALTER TABLE `client` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `datos_personales`
--

DROP TABLE IF EXISTS `datos_personales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `datos_personales` (
  `id_datos_personales` int NOT NULL AUTO_INCREMENT,
  `tipo_documento` varchar(10) DEFAULT NULL,
  `numero_documento` varchar(20) DEFAULT NULL,
  `user_id` int NOT NULL,
  `direccion` varchar(200) DEFAULT NULL,
  `telefono` varchar(30) DEFAULT NULL,
  `localidad` varchar(100) DEFAULT NULL,
  `provincia` varchar(100) DEFAULT NULL,
  `codigo_postal` varchar(10) DEFAULT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `creado_en` datetime DEFAULT CURRENT_TIMESTAMP,
  `actualizado_en` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_datos_personales`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `numero_documento` (`numero_documento`),
  CONSTRAINT `fk_datos_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `datos_personales`
--

LOCK TABLES `datos_personales` WRITE;
/*!40000 ALTER TABLE `datos_personales` DISABLE KEYS */;
INSERT INTO `datos_personales` VALUES (1,NULL,'45489658',3,NULL,NULL,NULL,NULL,NULL,NULL,'2026-04-01 16:16:06','2026-04-01 16:16:06'),(2,NULL,'46987456',4,NULL,NULL,NULL,NULL,NULL,NULL,'2026-04-07 18:32:33','2026-04-07 18:32:33');
/*!40000 ALTER TABLE `datos_personales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deposito`
--

DROP TABLE IF EXISTS `deposito`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deposito` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(120) NOT NULL,
  `direccion` varchar(200) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` datetime(6) DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` datetime(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deposito`
--

LOCK TABLES `deposito` WRITE;
/*!40000 ALTER TABLE `deposito` DISABLE KEYS */;
INSERT INTO `deposito` VALUES (1,'Deposito Central','',1,'2026-04-07 21:41:11.293721','2026-04-07 21:41:11.293734');
/*!40000 ALTER TABLE `deposito` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(16,'Proyecto_Soderia','barrio'),(9,'Proyecto_Soderia','camioneta'),(7,'Proyecto_Soderia','client'),(21,'Proyecto_Soderia','consultaweb'),(18,'Proyecto_Soderia','datospersonales'),(19,'Proyecto_Soderia','deposito'),(10,'Proyecto_Soderia','pedido'),(13,'Proyecto_Soderia','pedidodetalle'),(11,'Proyecto_Soderia','pedidoestado'),(12,'Proyecto_Soderia','producto'),(8,'Proyecto_Soderia','rolemeta'),(14,'Proyecto_Soderia','stockcamioneta'),(20,'Proyecto_Soderia','stockdeposito'),(15,'Proyecto_Soderia','stockmovimiento'),(17,'Proyecto_Soderia','zona'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-02-10 16:51:47.762383'),(2,'auth','0001_initial','2026-02-10 16:51:48.588024'),(3,'contenttypes','0002_remove_content_type_name','2026-02-10 16:51:48.713365'),(4,'auth','0002_alter_permission_name_max_length','2026-02-10 16:51:48.784632'),(5,'auth','0003_alter_user_email_max_length','2026-02-10 16:51:48.804257'),(6,'auth','0004_alter_user_username_opts','2026-02-10 16:51:48.812624'),(7,'auth','0005_alter_user_last_login_null','2026-02-10 16:51:48.872936'),(8,'auth','0006_require_contenttypes_0002','2026-02-10 16:51:48.878497'),(9,'auth','0007_alter_validators_add_error_messages','2026-02-10 16:51:48.888204'),(10,'auth','0008_alter_user_username_max_length','2026-02-10 16:51:48.963066'),(11,'auth','0009_alter_user_last_name_max_length','2026-02-10 16:51:49.036673'),(12,'auth','0010_alter_group_name_max_length','2026-02-10 16:51:49.054796'),(13,'auth','0011_update_proxy_permissions','2026-02-10 16:51:49.064829'),(14,'auth','0012_alter_user_first_name_max_length','2026-02-10 16:51:49.137074'),(31,'admin','0001_initial','2026-02-10 16:53:17.632083'),(32,'admin','0002_logentry_remove_auto_add','2026-02-10 16:53:17.645451'),(33,'admin','0003_logentry_add_action_flag_choices','2026-02-10 16:53:17.658167'),(34,'sessions','0001_initial','2026-02-10 16:53:17.704973'),(36,'Proyecto_Soderia','0001_initial','2026-02-17 20:13:07.079433'),(37,'Proyecto_Soderia','0002_remove_camioneta_is_deposito','2026-02-17 20:17:19.372568'),(38,'Proyecto_Soderia','0003_deposito_stockdeposito','2026-02-17 20:20:31.542008'),(39,'Proyecto_Soderia','0004_alter_datospersonales_options','2026-02-17 20:56:46.748918'),(40,'Proyecto_Soderia','0005_auto_20260409_1850','2026-04-09 21:51:31.179856');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('137px21l22k20sp48e5wme1jc4e834gg','.eJxVzLEOAiEQBNB_oTYEFkGwtPcbyO4tyKmB5LirjP-uJFdoO29mXiLitpa49bTEmcVZGHH4zQinR6oD-I711uTU6rrMJEdF7trltXF6Xvbu30HBXsYaKSQy1ivvPRjgExOFzECOAIcG_TXnnD6aoGzOyjok0AguKw_i_QHv1jei:1w8131:V_Q2KE4d5sK24ocniwIJl5-6kZ7gywsuvIlB-eaWCEs','2026-04-15 19:16:15.645284'),('9w4t1uqpghnkr33859ebs8bxvbkcc049','.eJxVjE0OwiAYBe_C2hD-CtSle89AHvAhVUOT0q6Md9cmXej2zcx7sYBtrWHrtIQpszOT7PS7RaQHtR3kO9pt5mlu6zJFviv8oJ1f50zPy-H-HVT0-q3HoqVPZQCRSxKgrJVQJTkPbRUJncoIrwBrjIEWFlE4KtJFD2vjwN4fBCU4gA:1vsRaz:UOSOvdSQEsaJPFug8Fq2YoZD7DvsI7QiYXTfERlIuZQ','2026-03-03 20:22:57.279439'),('bjpjoxr5j41s67e5i7cciov7xjdqx8hx','.eJxVjMsOwiAQRf-FtSEwvIpL934DYRiQqoGktCvjv2uTLnR7zzn3xULc1hq2kZcwEzszYKffDWN65LYDusd26zz1ti4z8l3hBx382ik_L4f7d1DjqN_aOKtTNAILobDTVEAZMFicktoZV5CUzhaEB688aqW9koQJMgmQGTV7fwDL2Dc-:1wAx78:wSh_hNnOdztbyjZOMMuIc8JDr-udjcizKgqbD3BpM-8','2026-04-23 21:40:38.066500'),('lbkw3c52izx64nmf986cp53escajbmiq','.eJxVjEEOwiAQRe_C2pCWDlNw6d4zkIEZpGpoUtqV8e7apAvd_vfef6lA21rC1mQJE6uzAnX63SKlh9Qd8J3qbdZprusyRb0r-qBNX2eW5-Vw_w4KtfKtTew6cZTYikGIKOAR0yhsgXoG5pwTx5gBs_E59wMb8CTOosMRaFDvDw5SONQ:1wAE2W:Z-xOnmcaoIfvH_BcCnhRj13uUGXUEsUGrPM4KfxWQp0','2026-04-21 21:32:52.587955'),('p6pd532pdcovpdrruds6sjjk96hrcim2','.eJxVzLEOAiEQBNB_oTYEFkGwtPcbyO4tyKmB5LirjP-uJFdoO29mXiLitpa49bTEmcVZGHH4zQinR6oD-I711uTU6rrMJEdF7trltXF6Xvbu30HBXsYaKSQy1ivvPRjgExOFzECOAIcG_TXnnD6aoGzOyjok0AguKw_i_QHv1jei:1wADyc:9KmsBU6GksaPpLlSNPl4ZmhwcST-Fu8rbEuHhznSRf0','2026-04-21 21:28:50.833812');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido`
--

DROP TABLE IF EXISTS `pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `estado` varchar(20) NOT NULL,
  `total` decimal(10,2) NOT NULL DEFAULT '0.00',
  `forma_pago` varchar(60) NOT NULL,
  `pago_monto` decimal(10,2) DEFAULT NULL,
  `pago_motivo` varchar(200) NOT NULL,
  `pago_fecha` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `camioneta_id` bigint DEFAULT NULL,
  `cliente_id` bigint NOT NULL,
  `creado_por_id` int DEFAULT NULL,
  `numero_pedido` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_pedido` (`numero_pedido`),
  KEY `Proyecto_Soderia_pedido_creado_por_id_5190ff8f_fk_auth_user_id` (`creado_por_id`),
  KEY `idx_pedido_cliente` (`cliente_id`),
  KEY `idx_pedido_camioneta` (`camioneta_id`),
  KEY `idx_pedido_fecha` (`created_at`),
  CONSTRAINT `Proyecto_Soderia_ped_camioneta_id_22e99f62_fk_Proyecto_` FOREIGN KEY (`camioneta_id`) REFERENCES `camioneta` (`id`),
  CONSTRAINT `Proyecto_Soderia_ped_cliente_id_1e089eb4_fk_Proyecto_` FOREIGN KEY (`cliente_id`) REFERENCES `client` (`id`),
  CONSTRAINT `Proyecto_Soderia_pedido_creado_por_id_5190ff8f_fk_auth_user_id` FOREIGN KEY (`creado_por_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido`
--

LOCK TABLES `pedido` WRITE;
/*!40000 ALTER TABLE `pedido` DISABLE KEYS */;
INSERT INTO `pedido` VALUES (1,'PAGADO',9600.00,'efectivo',NULL,'',NULL,'2026-03-11 13:05:57.177323','2026-04-01 19:32:17.261689',4,27,2,NULL),(2,'PAGADO',4200.00,'efectivo',4200.00,'','2026-04-07 21:16:02.348193','2026-03-11 13:07:24.655118','2026-04-07 21:16:02.348329',NULL,15,2,NULL),(3,'PAGADO',6400.00,'transferencia',6400.00,'','2026-04-07 21:25:54.380577','2026-04-07 21:25:04.684767','2026-04-07 21:25:54.380635',4,27,2,NULL),(4,'ENTREGADO',5400.00,'efectivo',NULL,'',NULL,'2026-04-07 21:27:10.828892','2026-04-07 21:37:58.813463',NULL,1,2,NULL),(5,'PAGADO',5400.00,'efectivo',5400.00,'','2026-04-07 21:38:53.031363','2026-04-07 21:38:48.893190','2026-04-07 21:38:53.031431',NULL,27,3,NULL),(6,'PAGADO',162000.00,'efectivo',162000.00,'','2026-04-07 21:49:06.660677','2026-04-07 21:48:04.236390','2026-04-07 21:49:06.660737',4,27,2,NULL),(7,'PAGADO',5400.00,'efectivo',5400.00,'','2026-04-07 22:01:22.703484','2026-04-07 21:50:57.294538','2026-04-07 22:01:22.703635',4,1,2,NULL),(8,'PAGADO',9600.00,'efectivo',9600.00,'estaba roto','2026-04-07 22:13:51.161479','2026-04-07 22:01:49.812036','2026-04-07 22:13:51.161557',4,27,2,NULL);
/*!40000 ALTER TABLE `pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidodetalle`
--

DROP TABLE IF EXISTS `pedidodetalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidodetalle` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cantidad` int NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `pedido_id` bigint NOT NULL,
  `producto_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Proyecto_Soderia_ped_producto_id_19273601_fk_Proyecto_` (`producto_id`),
  KEY `fk_pdd_pedido` (`pedido_id`),
  CONSTRAINT `fk_pdd_pedido` FOREIGN KEY (`pedido_id`) REFERENCES `pedido` (`id`) ON DELETE CASCADE,
  CONSTRAINT `Proyecto_Soderia_ped_pedido_id_f409282a_fk_Proyecto_` FOREIGN KEY (`pedido_id`) REFERENCES `pedido` (`id`),
  CONSTRAINT `Proyecto_Soderia_ped_producto_id_19273601_fk_Proyecto_` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidodetalle`
--

LOCK TABLES `pedidodetalle` WRITE;
/*!40000 ALTER TABLE `pedidodetalle` DISABLE KEYS */;
INSERT INTO `pedidodetalle` VALUES (1,3,3200.00,1,6),(2,2,2100.00,2,8),(3,2,3200.00,3,6),(4,1,5400.00,4,7),(5,1,5400.00,5,7),(6,30,5400.00,6,7),(7,1,5400.00,7,7),(8,3,3200.00,8,6);
/*!40000 ALTER TABLE `pedidodetalle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidoestado`
--

DROP TABLE IF EXISTS `pedidoestado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidoestado` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `estado` varchar(20) NOT NULL,
  `motivo` varchar(200) NOT NULL,
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `pedido_id` bigint NOT NULL,
  `usuario_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Proyecto_Soderia_ped_usuario_id_c8b5882a_fk_auth_user` (`usuario_id`),
  KEY `idx_pe_pedido` (`pedido_id`),
  CONSTRAINT `Proyecto_Soderia_ped_pedido_id_3dc18d5f_fk_Proyecto_` FOREIGN KEY (`pedido_id`) REFERENCES `pedido` (`id`),
  CONSTRAINT `Proyecto_Soderia_ped_usuario_id_c8b5882a_fk_auth_user` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidoestado`
--

LOCK TABLES `pedidoestado` WRITE;
/*!40000 ALTER TABLE `pedidoestado` DISABLE KEYS */;
INSERT INTO `pedidoestado` VALUES (1,'CREADO','','2026-03-11 13:05:57.193167',1,2),(2,'ASIGNADO','','2026-03-11 13:06:11.053877',1,2),(3,'CREADO','','2026-03-11 13:07:24.667162',2,2),(4,'ASIGNADO','','2026-04-01 19:29:27.656167',1,2),(5,'EN_REPARTO','','2026-04-01 19:29:55.893138',1,2),(6,'ENTREGADO','','2026-04-01 19:32:12.746082',1,2),(7,'PAGADO','','2026-04-01 19:32:17.267603',1,2),(8,'PAGADO','','2026-04-07 21:16:02.353049',2,2),(9,'CREADO','','2026-04-07 21:25:04.698595',3,2),(10,'ASIGNADO','','2026-04-07 21:25:21.825940',3,2),(11,'EN_REPARTO','','2026-04-07 21:25:46.869429',3,2),(12,'PAGADO','','2026-04-07 21:25:54.385864',3,2),(13,'CREADO','','2026-04-07 21:27:10.840631',4,2),(14,'ASIGNADO','','2026-04-07 21:31:23.537092',4,2),(15,'ENTREGADO','','2026-04-07 21:37:58.819319',4,3),(16,'CREADO','','2026-04-07 21:38:48.905454',5,3),(17,'PAGADO','','2026-04-07 21:38:53.035709',5,3),(18,'CREADO','','2026-04-07 21:48:04.249257',6,2),(19,'ASIGNADO','','2026-04-07 21:48:10.343100',6,2),(20,'EN_REPARTO','','2026-04-07 21:48:36.474976',6,3),(21,'ENTREGADO','','2026-04-07 21:49:01.965553',6,3),(22,'PAGADO','','2026-04-07 21:49:06.665041',6,3),(23,'CREADO','','2026-04-07 21:50:57.309302',7,2),(24,'ASIGNADO','','2026-04-07 21:51:00.530902',7,2),(25,'EN_REPARTO','','2026-04-07 21:51:06.685916',7,2),(26,'ENTREGADO','','2026-04-07 21:51:14.180499',7,2),(27,'PAGADO','','2026-04-07 22:01:22.708652',7,3),(28,'CREADO','','2026-04-07 22:01:49.824486',8,2),(29,'ASIGNADO','','2026-04-07 22:01:54.630203',8,2),(30,'DEVUELTO','esta roto','2026-04-07 22:04:23.307317',8,3),(31,'EN_REPARTO','','2026-04-07 22:11:20.270759',8,2),(32,'DEVUELTO','','2026-04-07 22:12:25.173205',8,3),(33,'DEVUELTO','','2026-04-07 22:13:00.091822',8,3),(34,'PAGADO','estaba roto','2026-04-07 22:13:51.166909',8,3);
/*!40000 ALTER TABLE `pedidoestado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(120) NOT NULL,
  `retornable` tinyint(1) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `capacidad_litros` decimal(6,2) NOT NULL,
  `deposito_envase` decimal(10,2) DEFAULT NULL,
  `requiere_envase` tinyint(1) NOT NULL,
  `tipo_envase` varchar(20) NOT NULL,
  `unidad_venta` varchar(20) NOT NULL,
  `max_por_camioneta` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
INSERT INTO `producto` VALUES (1,'Soda 1.5L',0,1800.00,1,1.50,NULL,0,'BOTELLA','UNIDAD',120),(2,'Soda 2L',0,2200.00,1,2.00,NULL,0,'BOTELLA','UNIDAD',100),(3,'Sifon Soda 1.25L',1,2500.00,1,1.25,3500.00,1,'SIFON','UNIDAD',120),(4,'Bidon Agua 12L',1,4200.00,1,12.00,6000.00,1,'BIDON','UNIDAD',40),(5,'Bidon Agua 20L',1,5800.00,1,20.00,8000.00,1,'BIDON','UNIDAD',30),(6,'Agua Mineral 500ml Pack x6',0,3200.00,1,0.50,NULL,0,'BOTELLA','PACK',80),(7,'Agua Mineral 1.5L Pack x6',0,5400.00,1,1.50,NULL,0,'BOTELLA','PACK',60),(8,'Agua Saborizada 1.5L',0,2100.00,1,1.50,NULL,0,'BOTELLA','UNIDAD',80),(9,'Gaseosa Cola 2.25L',0,3100.00,1,2.25,NULL,0,'BOTELLA','UNIDAD',70),(10,'Gaseosa Lima Limon 2.25L',0,3050.00,1,2.25,NULL,0,'BOTELLA','UNIDAD',70);
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stockcamioneta`
--

DROP TABLE IF EXISTS `stockcamioneta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stockcamioneta` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cantidad_actual` int NOT NULL,
  `camioneta_id` bigint NOT NULL,
  `producto_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_stock_cam_prod` (`camioneta_id`,`producto_id`),
  KEY `Proyecto_Soderia_sto_producto_id_0a4ccd7a_fk_Proyecto_` (`producto_id`),
  CONSTRAINT `Proyecto_Soderia_sto_camioneta_id_96f7b0ba_fk_Proyecto_` FOREIGN KEY (`camioneta_id`) REFERENCES `camioneta` (`id`),
  CONSTRAINT `Proyecto_Soderia_sto_producto_id_0a4ccd7a_fk_Proyecto_` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stockcamioneta`
--

LOCK TABLES `stockcamioneta` WRITE;
/*!40000 ALTER TABLE `stockcamioneta` DISABLE KEYS */;
INSERT INTO `stockcamioneta` VALUES (1,300,4,5),(2,63,4,7),(3,7,4,8),(4,4,4,1),(5,4,4,3),(6,4,4,4),(7,3,4,6),(8,10,5,7);
/*!40000 ALTER TABLE `stockcamioneta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stockdeposito`
--

DROP TABLE IF EXISTS `stockdeposito`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stockdeposito` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cantidad_actual` int NOT NULL,
  `producto_id` bigint NOT NULL,
  `deposito_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_stock_dep_prod_new` (`deposito_id`,`producto_id`),
  KEY `fk_stockdeposito_producto` (`producto_id`),
  CONSTRAINT `fk_stockdeposito_deposito` FOREIGN KEY (`deposito_id`) REFERENCES `deposito` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_stockdeposito_producto` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stockdeposito`
--

LOCK TABLES `stockdeposito` WRITE;
/*!40000 ALTER TABLE `stockdeposito` DISABLE KEYS */;
INSERT INTO `stockdeposito` VALUES (1,6,7,1),(2,96,6,1),(3,93,8,1),(4,496,4,1),(5,0,5,1),(6,296,3,1),(7,96,1,1),(8,10,2,1);
/*!40000 ALTER TABLE `stockdeposito` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stockmovimiento`
--

DROP TABLE IF EXISTS `stockmovimiento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stockmovimiento` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tipo` varchar(20) NOT NULL,
  `cantidad` int NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `camioneta_id` bigint NOT NULL,
  `pedido_id` bigint DEFAULT NULL,
  `producto_id` bigint NOT NULL,
  `usuario_id` int DEFAULT NULL,
  `deposito_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Proyecto_Soderia_sto_camioneta_id_e75a7d45_fk_Proyecto_` (`camioneta_id`),
  KEY `Proyecto_Soderia_sto_pedido_id_a6b3dbc7_fk_Proyecto_` (`pedido_id`),
  KEY `Proyecto_Soderia_sto_producto_id_9d1df325_fk_Proyecto_` (`producto_id`),
  KEY `Proyecto_Soderia_sto_usuario_id_bbffe6d5_fk_auth_user` (`usuario_id`),
  KEY `fk_stockmov_deposito` (`deposito_id`),
  CONSTRAINT `fk_stockmov_deposito` FOREIGN KEY (`deposito_id`) REFERENCES `deposito` (`id`) ON DELETE SET NULL,
  CONSTRAINT `Proyecto_Soderia_sto_camioneta_id_e75a7d45_fk_Proyecto_` FOREIGN KEY (`camioneta_id`) REFERENCES `camioneta` (`id`),
  CONSTRAINT `Proyecto_Soderia_sto_pedido_id_a6b3dbc7_fk_Proyecto_` FOREIGN KEY (`pedido_id`) REFERENCES `pedido` (`id`),
  CONSTRAINT `Proyecto_Soderia_sto_producto_id_9d1df325_fk_Proyecto_` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`),
  CONSTRAINT `Proyecto_Soderia_sto_usuario_id_bbffe6d5_fk_auth_user` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stockmovimiento`
--

LOCK TABLES `stockmovimiento` WRITE;
/*!40000 ALTER TABLE `stockmovimiento` DISABLE KEYS */;
INSERT INTO `stockmovimiento` VALUES (1,'AJUSTE',300,'2026-04-07 21:45:38.468753',4,NULL,5,4,NULL),(2,'AJUSTE',60,'2026-04-07 21:46:12.754275',4,NULL,7,4,NULL),(3,'ENTREGA',1,'2026-04-07 21:51:14.194871',4,7,7,2,NULL),(4,'AJUSTE',3,'2026-04-07 22:03:24.056246',4,NULL,8,2,NULL),(5,'AJUSTE',4,'2026-04-07 22:03:47.016316',4,NULL,1,2,NULL),(6,'AJUSTE',4,'2026-04-07 22:03:47.035944',4,NULL,3,2,NULL),(7,'AJUSTE',4,'2026-04-07 22:03:47.068052',4,NULL,4,2,NULL),(8,'AJUSTE',4,'2026-04-07 22:03:47.086838',4,NULL,6,2,NULL),(9,'AJUSTE',4,'2026-04-07 22:03:47.100706',4,NULL,7,2,NULL),(10,'AJUSTE',4,'2026-04-07 22:03:47.114767',4,NULL,8,2,NULL),(11,'ENTREGA',2,'2026-04-07 22:04:23.313458',4,8,6,3,NULL),(12,'DEVOLUCION',1,'2026-04-07 22:04:23.317524',4,8,6,3,NULL),(13,'AJUSTE',10,'2026-04-07 22:08:35.631174',5,NULL,7,2,NULL);
/*!40000 ALTER TABLE `stockmovimiento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `web_inquiries`
--

DROP TABLE IF EXISTS `web_inquiries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `web_inquiries` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(120) NOT NULL,
  `email` varchar(254) NOT NULL,
  `telefono` varchar(30) NOT NULL,
  `mensaje` longtext NOT NULL,
  `estado` varchar(20) NOT NULL,
  `notas_internas` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `cliente_convertido_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `web_inquiries_cliente_convertido_id_162fbe1f_fk_client_id` (`cliente_convertido_id`),
  CONSTRAINT `web_inquiries_cliente_convertido_id_162fbe1f_fk_client_id` FOREIGN KEY (`cliente_convertido_id`) REFERENCES `client` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `web_inquiries`
--

LOCK TABLES `web_inquiries` WRITE;
/*!40000 ALTER TABLE `web_inquiries` DISABLE KEYS */;
INSERT INTO `web_inquiries` VALUES (1,'edmundo','marlenejerusalen@gmail.com','387-555-1129','soda de 1 l','NUEVA','','2026-04-09 21:52:19.610200','2026-04-09 21:52:19.610227',NULL);
/*!40000 ALTER TABLE `web_inquiries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `zona`
--

DROP TABLE IF EXISTS `zona`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `zona` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(40) NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zona`
--

LOCK TABLES `zona` WRITE;
/*!40000 ALTER TABLE `zona` DISABLE KEYS */;
INSERT INTO `zona` VALUES (1,'Centro',1),(2,'Norte',1),(3,'Sur',1),(4,'Este',1),(5,'Oeste',1),(6,'Salta Capital',1);
/*!40000 ALTER TABLE `zona` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-09 18:53:32
