-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 28, 2026 at 02:49 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `actbayan`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts`
--

CREATE TABLE `accounts` (
  `account_id` int(11) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `middle_name` varchar(50) NOT NULL,
  `dob` date NOT NULL,
  `profile_photo` varchar(255) DEFAULT '',
  `id_proof_path` varchar(255) DEFAULT NULL,
  `account_status` varchar(20) DEFAULT 'Pending',
  `house_no` varchar(100) DEFAULT NULL,
  `street_name` varchar(100) DEFAULT NULL,
  `province` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `barangay` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts`
--

INSERT INTO `accounts` (`account_id`, `first_name`, `last_name`, `middle_name`, `dob`, `profile_photo`, `id_proof_path`, `account_status`, `house_no`, `street_name`, `province`, `city`, `barangay`) VALUES
(1, 'LGU', 'Official', '', '1990-01-01', '', NULL, 'Verified', NULL, NULL, NULL, NULL, NULL),
(2, 'System', 'Admin', '', '1990-01-01', '', NULL, 'Verified', NULL, NULL, NULL, NULL, NULL),
(10, 'Ferdinand Jr', 'Eusebio', 'Dela Paz', '2005-05-05', 'static/uploads/profile_10_1787150189.jpeg', 'static/uploads/id_proofs/Corporate-ID-3-e1526258986105.jpg', 'Verified', '0327', 'Zone 4', 'Bulacan', 'San Miguel', 'Partida'),
(11, 'Fred Rick', 'Santiago', 'Bascos', '2005-03-26', 'static/uploads/profile_11_1787150889.jpeg', 'static/uploads/id_proofs/Corporate-ID-3-e1526258986105.jpg', 'Verified', '111', 'Calamansi', 'Nueva Ecija', 'General Mamerto Natividad', 'Bravo'),
(15, 'Fred Rick', 'Santiago', '', '2010-09-05', NULL, 'static/uploads/id_proofs/IMG_20260417_094131_044~2.jpg', 'Verified', 'NA', 'NA', 'Nueva Ecija', 'Llanera', 'San Francisco'),
(16, 'Lee', 'Pineda', 'Gon', '2005-01-24', NULL, 'static/uploads/id_proofs/1e72af62-7a42-4a7a-8820-0326671e2cab.jpg', 'Verified', 'Blk 1', 'Mabini', 'Bulacan', 'San Miguel', 'Buga'),
(17, 'Markly Harrison', 'Magbuhos', '', '2005-08-12', 'static/uploads/profile_17_1787551175.jpeg', 'static/uploads/id_proofs/images (8).jpeg', 'Verified', '123', 'Ipil St. ', 'Nueva Ecija', 'General Mamerto Natividad', 'Mataas na Kahoy'),
(18, 'Juan', 'Dela cruz', 'Milo', '2006-01-19', NULL, 'static/uploads/id_proofs/real id adult cdl-1.jpeg', 'Pending', '0992', 'Zone4', 'Albay', 'Jovellar', 'Magsaysay Pob'),
(19, 'joe', 'MaMa', '', '2011-08-24', 'static/uploads/profile_19_1787554606.jpeg', 'static/uploads/id_proofs/real id adult cdl-1.jpeg', 'Verified', 'isid', 'jeje', 'Antique', 'Culasi', 'Bita'),
(20, 'Markly', 'Magbuhos', '', '2011-08-27', NULL, NULL, 'Incomplete', '474', 'Ipil St. ', 'Nueva Ecija', 'General Mamerto Natividad', 'Mataas na Kahoy'),
(22, 'Anastasia ', 'Dela Cruz', 'Narsiso', '2006-02-14', 'static/uploads/profile_22_1787846506.jpeg', NULL, 'Incomplete', '0992', 'Zone 5', 'Nueva Ecija', 'General Mamerto Natividad', 'Panacsac');

-- --------------------------------------------------------

--
-- Table structure for table `activity_logs`
--

CREATE TABLE `activity_logs` (
  `al_id` int(11) NOT NULL,
  `report_id` int(11) DEFAULT NULL,
  `action` varchar(255) DEFAULT NULL,
  `made_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `announcements`
--

CREATE TABLE `announcements` (
  `ann_id` int(11) NOT NULL,
  `account_id` int(11) DEFAULT NULL,
  `ann_title` varchar(254) DEFAULT NULL,
  `ann_desc` text DEFAULT NULL,
  `submitted_at` datetime DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `announcements`
--

INSERT INTO `announcements` (`ann_id`, `account_id`, `ann_title`, `ann_desc`, `submitted_at`, `category`) VALUES
(1, 1, 'WANTED: Lester', 'Lester Romero was accused of a serious crime today. If you see him, please contact us. His alleged actions are deeply concerning.', '2026-07-20 18:42:17', 'General'),
(2, 1, 'Incoming Typhoon', 'Hello Fellow Residents,\r\n\r\nI am writing to you today with an urgent announcement regarding an impending natural phenomenon. We have received confirmation that a typhoon is headed directly towards our city, and its arrival is imminent. We urge all citizens to take this warning seriously and to prepare yourselves and your properties accordingly.\r\n\r\nYour safety is our utmost priority. Please ensure that all your valuable belongings are secured, and take all necessary precautions to protect your homes and loved ones. We understand that such events can be unsettling, and we want to assure you that the local government unit is working tirelessly to mitigate any potential risks and to provide support to our community.\r\n\r\nTo facilitate immediate assistance during this critical period, we have established an emergency hotline. This line will be operational 24/7, and we encourage you to call us without hesitation should you face any emergency situations or require immediate aid. We have a dedicated team ready to respond to your calls and to dispatch necessary resources.\r\n\r\nFurthermore, in light of the potential dangers posed by the typhoon, we have made the decision to transition all educational institutions to an online learning mode with immediate effect. This measure is being implemented to ensure the safety of our students and faculty, and we kindly request your cooperation in making this transition as smooth as possible. Further details regarding online learning protocols will be disseminated through respective school administrations.\r\n\r\nWe appreciate your understanding and cooperation during this challenging time. By working together, we can ensure the safety and well-being of everyone in our beloved city.\r\n\r\nThank you very much,\r\n\r\n-LGU Officials', '2026-08-24 14:07:08', 'Safety');

-- --------------------------------------------------------

--
-- Table structure for table `contacts`
--

CREATE TABLE `contacts` (
  `contact_id` int(11) NOT NULL,
  `account_id` int(11) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone_number` varchar(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contacts`
--

INSERT INTO `contacts` (`contact_id`, `account_id`, `email`, `phone_number`) VALUES
(1, 1, 'lgu@actbayan.gov.ph', '09222222222'),
(2, 2, 'admin@actbayan.gov.ph', '09111111111'),
(10, 10, 'ijiayreusebio@gmail.com', '09506348554'),
(11, 11, 'fredricksantiabs99@gmail.com', '09090909090'),
(14, 15, 'sanfrbs26@gmail.com', '09760692055'),
(15, 16, 'lee@gmail.com', '09365441563'),
(16, 17, 'markly@gmail.com', '09123123412'),
(17, 18, 'halomadlamgpipol@gmail.com', '09923456712'),
(18, 19, 'kahitano@gmail.com', '09123456789'),
(19, 20, 'markly1@gmail.com', '09121234567'),
(20, 22, 'Canva@gmail.com', '09946531875');

--
-- Triggers `contacts`
--
DELIMITER $$
CREATE TRIGGER `passcontact` AFTER INSERT ON `contacts` FOR EACH ROW BEGIN
    IF NEW.email IS NOT NULL THEN
        INSERT INTO usercreds(contact_id, emorph)
        VALUES (NEW.contact_id, NEW.email);
    END IF;

    IF NEW.phone_number IS NOT NULL THEN
        INSERT INTO usercreds(contact_id, emorph)
        VALUES (NEW.contact_id, NEW.phone_number);
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `credentials`
--

CREATE TABLE `credentials` (
  `cred_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `pass_id` int(11) DEFAULT NULL,
  `failed_attempts` int(11) DEFAULT NULL,
  `is_locked` varchar(100) DEFAULT NULL,
  `lock_duration` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `credentials`
--

INSERT INTO `credentials` (`cred_id`, `user_id`, `pass_id`, `failed_attempts`, `is_locked`, `lock_duration`) VALUES
(1, 1, 1, NULL, 'N', NULL),
(2, 2, 1, NULL, 'N', NULL),
(3, 3, 2, NULL, 'N', NULL),
(4, 4, 2, NULL, 'N', NULL),
(19, 19, 10, NULL, NULL, NULL),
(20, 20, 10, NULL, NULL, NULL),
(21, 21, 11, NULL, NULL, NULL),
(22, 22, 11, NULL, NULL, NULL),
(27, 27, 14, NULL, NULL, NULL),
(28, 28, 14, NULL, NULL, NULL),
(29, 29, 15, NULL, NULL, NULL),
(30, 30, 15, NULL, NULL, NULL),
(31, 31, 16, NULL, NULL, NULL),
(32, 32, 16, NULL, NULL, NULL),
(33, 33, 17, NULL, NULL, NULL),
(34, 34, 17, NULL, NULL, NULL),
(35, 35, 18, NULL, NULL, NULL),
(36, 36, 18, NULL, NULL, NULL),
(37, 37, 19, NULL, NULL, NULL),
(38, 38, 19, NULL, NULL, NULL),
(39, 39, 20, NULL, NULL, NULL),
(40, 40, 20, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `feedbacks`
--

CREATE TABLE `feedbacks` (
  `feedback_id` int(11) NOT NULL,
  `account_id` int(11) DEFAULT NULL,
  `report_id` int(11) DEFAULT NULL,
  `feedback` text DEFAULT NULL,
  `uploaded_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `feedbacks`
--

INSERT INTO `feedbacks` (`feedback_id`, `account_id`, `report_id`, `feedback`, `uploaded_at`) VALUES
(1, 4, 1, 'lmao', '2026-07-14 23:29:54'),
(2, 6, 1, 'okay pu', '2026-07-20 12:13:33');

-- --------------------------------------------------------

--
-- Table structure for table `location`
--

CREATE TABLE `location` (
  `location_id` int(11) NOT NULL,
  `locname` varchar(254) DEFAULT NULL,
  `x` decimal(10,7) NOT NULL,
  `y` decimal(10,7) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `location`
--

INSERT INTO `location` (`location_id`, `locname`, `x`, `y`) VALUES
(1, 'Batuhan - Partida Road, San Miguel, Partida, Bulacan', 15.2023548, 121.0151596),
(2, 'Batuhan - Partida Road, San Miguel, Partida, Bulacan', 15.2024326, 121.0152243),
(4, 'Tramo Street, Cabanatuan, Nueva Ecija', 15.4453067, 120.9447569),
(5, 'Primavera Homes, Tramo Street, Cabanatuan, Nueva Ecija', 15.4453335, 120.9447505),
(6, 'Primavera Homes, Tramo Street, Cabanatuan, Nueva Ecija', 15.4453335, 120.9447505),
(7, 'General Mamerto Natividad, Mag-Asawang Sampaloc, Nueva Ecija', 15.6041223, 121.0504937),
(8, 'General Mamerto Natividad, Mag-Asawang Sampaloc, Nueva Ecija', 15.6031679, 121.0503244),
(9, 'General Mamerto Natividad, Mag-Asawang Sampaloc, Nueva Ecija', 15.6045570, 121.0520606),
(10, 'General Mamerto Natividad, Mag-Asawang Sampaloc, Nueva Ecija', 15.6054973, 121.0528767),
(11, 'General Mamerto Natividad, Mag-Asawang Sampaloc, Nueva Ecija', 15.6021648, 121.0498082),
(12, 'General Mamerto Natividad, Mag-Asawang Sampaloc, Nueva Ecija', 15.6050221, 121.0491443),
(13, 'General Mamerto Natividad, Mataas Na Kahoy, Nueva Ecija', 15.6098064, 121.0176801),
(14, 'General Mamerto Natividad, Talabutab Norte, Nueva Ecija', 15.6010333, 121.0782158),
(15, 'General Mamerto Natividad, Mataas Na Kahoy, Nueva Ecija', 15.6084758, 121.0194317),
(16, 'Acropolis North, Olympia Street, Cabanatuan, Nueva Ecija', 15.4495178, 120.9401655);

-- --------------------------------------------------------

--
-- Table structure for table `login_logs`
--

CREATE TABLE `login_logs` (
  `log_id` int(11) NOT NULL,
  `emorph` varchar(100) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `attempt_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `login_logs`
--

INSERT INTO `login_logs` (`log_id`, `emorph`, `status`, `attempt_time`) VALUES
(1, 'admin@actbayan.gov.ph', 'Success', '2026-07-14 17:24:41'),
(2, 'lgu@actbayan.gov.ph', 'Success', '2026-07-14 17:25:22'),
(3, 'lgu@actbayan.gov.ph', 'Success', '2026-07-14 17:37:43'),
(4, 'ijiayreusebio@gmail.com', 'Success', '2026-07-14 17:38:22'),
(5, 'ijiayreusebio@gmail.com', 'Success', '2026-07-14 17:43:14'),
(6, 'lgu@actbayan.gov.ph', 'Success', '2026-07-14 17:50:46'),
(7, 'admin@actbayan.gov.ph', 'Success', '2026-07-14 19:37:15'),
(8, 'admin@actbayan.gov.ph', 'Success', '2026-07-14 19:37:42'),
(9, 'ijiayreusebio@gmail.com', 'Success', '2026-07-14 20:04:22'),
(10, 'ijiayreusebio@gmail.com', 'Success', '2026-07-14 20:09:43'),
(11, 'admin@actbayan.gov.ph', 'Success', '2026-07-14 20:56:05'),
(12, 'ijiayreusebio@gmail.com', 'Success', '2026-07-14 20:57:14'),
(13, 'lgu@actbayan.gov.ph', 'Success', '2026-07-14 23:22:28'),
(14, 'ferdinandjreusebio@gmail.com', 'Success', '2026-07-14 23:25:22'),
(15, 'ferdinandjreusebio@gmail.com', 'Success', '2026-07-14 23:31:04'),
(16, 'ijiayreusebio@gmail.com', 'Success', '2026-07-20 09:44:29'),
(17, 'lgu@actbayan.gov.ph', 'Success', '2026-07-20 11:43:15'),
(18, 'admin@actbayan.gov.ph', 'Success', '2026-07-20 11:50:36'),
(19, 'sanfrbs26@gmail.com', 'Failed', '2026-07-20 11:52:03'),
(20, 'admin@actbayan.gov.ph', 'Success', '2026-07-20 11:52:05'),
(21, 'lgu@actbayan.gov.ph', 'Success', '2026-07-20 11:54:40'),
(22, 'admin@actbayan.gov.ph', 'Success', '2026-07-20 11:55:00'),
(23, 'lgu@actbayan.gov.ph', 'Success', '2026-07-20 12:01:11'),
(24, 'sanfrbs26@gmail.com', 'Success', '2026-07-20 12:12:41'),
(25, 'ijiayreusebio@gmail.com', 'Success', '2026-07-20 12:17:27'),
(26, 'lesterromero14@gamil.com', 'Failed', '2026-07-20 18:37:28'),
(27, 'lgu@actbayan.gov.ph', 'Success', '2026-07-20 18:38:34'),
(28, 'jayreusebio@gmail.com', 'Failed', '2026-07-20 18:43:29'),
(29, 'ijiayreusebio@gmail.com', 'Success', '2026-07-20 18:43:48'),
(30, 'lesterromero14@gmail.com', 'Failed', '2026-07-20 18:46:21'),
(31, 'lesterromero14@gmail.com', 'Failed', '2026-07-20 18:46:48'),
(32, 'lesterromero14@gmail.com', 'Failed', '2026-07-20 18:48:14'),
(33, 'lgu@actbayan.gov.ph', 'Success', '2026-07-20 18:55:09'),
(34, 'lesterandreimatiasromero@gmail.com', 'Success', '2026-07-20 18:57:35'),
(35, 'lesterandreimatiasromero@gmail.com', 'Success', '2026-07-20 18:58:50'),
(36, 'jayreusebio@gmail.com', 'Failed', '2026-07-20 19:00:29'),
(37, 'ijiayreusebio@gmail.com', 'Success', '2026-08-14 22:21:55'),
(38, 'ijiayreusebio@gmail.com', 'Success', '2026-08-14 23:39:20'),
(39, 'ijiayreusebio@gmail.com', 'Success', '2026-08-19 21:38:30'),
(40, 'ijiayreusebio@gmail.com', 'Success', '2026-08-19 21:39:24'),
(41, 'ijiayreusebio@gmail.com', 'Success', '2026-08-19 22:15:24'),
(42, 'admin@actbayan.gov.ph', 'Success', '2026-08-19 22:28:33'),
(43, 'ijiayreusebio@gmail.com', 'Failed', '2026-08-19 22:34:09'),
(44, 'ijiayreusebio@gmail.com', 'Failed', '2026-08-19 22:34:13'),
(45, 'lgu@actbayan.gov.ph', 'Success', '2026-08-19 22:38:13'),
(46, 'admin@actbayan.gov.ph', 'Success', '2026-08-19 22:57:32'),
(47, 'ladygaga@gmail.com', 'Failed (Banned)', '2026-08-19 23:19:24'),
(48, 'ladygaga@gmail.com', 'Success', '2026-08-19 23:19:40'),
(49, 'ladygaga@gmail.com', 'Failed (Banned)', '2026-08-19 23:19:57'),
(50, 'ladygaga@gmail.com', 'Failed', '2026-08-19 23:20:32'),
(51, 'lgu@actbayan.gov.ph', 'Success', '2026-08-20 10:29:07'),
(52, 'admin@actbayan.gov.ph', 'Success', '2026-08-20 10:36:47'),
(53, 'sanfrbs26@gmail.com', 'Success', '2026-08-20 10:58:44'),
(54, 'ijiayreusebio@gmail.com', 'Success', '2026-08-24 11:28:24'),
(55, 'lgu@actbayan.gov.ph', 'Success', '2026-08-24 13:50:17'),
(56, 'sanfrbs26@gmail.com', 'Success', '2026-08-24 13:53:26'),
(57, 'sanfrbs26@gmail.com', 'Success', '2026-08-24 13:56:37'),
(58, 'lee@gmail.com', 'Failed', '2026-08-24 13:57:37'),
(59, 'lee@gmail.com', 'Success', '2026-08-24 13:57:58'),
(60, 'ijiayreusebio@gmail.com', 'Success', '2026-08-24 13:59:06'),
(61, 'admin@actbayan.gov.ph', 'Success', '2026-08-24 14:16:05'),
(62, 'lgu@actbayan.gov.ph', 'Success', '2026-08-24 14:16:59'),
(63, 'sanfrbs26@gmail.com', 'Failed', '2026-08-27 21:55:57'),
(64, 'sanfrbs26@gmail.com', 'Success', '2026-08-27 21:56:07'),
(65, 'lee@gmail.com', 'Success', '2026-08-27 21:56:22'),
(66, 'markly@gmail.com', 'Success', '2026-08-27 21:57:45'),
(67, 'lgu@actbayan.gov.ph', 'Success', '2026-08-27 22:12:20'),
(68, 'admin@actbayan.gov.ph', 'Success', '2026-08-27 22:13:33'),
(69, 'markly1@gmail.com', 'Success', '2026-08-27 22:16:53'),
(70, 'markly@gmail.com', 'Success', '2026-08-27 22:17:31'),
(71, 'lgu@actbayan.gov.ph', 'Success', '2026-08-27 22:18:22'),
(72, 'markly@gmail.com', 'Success', '2026-08-27 22:21:20'),
(73, 'markly1@gmail.com', 'Success', '2026-08-27 22:24:00'),
(74, 'ijiayreusebio@gmail.com', 'Success', '2026-08-27 23:07:15'),
(75, 'ijiayreusebio@gmail.com', 'Success', '2026-08-27 23:12:10'),
(76, 'Canva@gmail.com', 'Success', '2026-08-28 00:02:11');

-- --------------------------------------------------------

--
-- Table structure for table `password`
--

CREATE TABLE `password` (
  `pass_id` int(11) NOT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `password`
--

INSERT INTO `password` (`pass_id`, `password`) VALUES
(1, '$2b$12$p7Dq/TMF5puHeg713vlV6ut7LphWkKyh/Q7tv.WhJOHFDiTwqPcIG'),
(2, '$2b$12$vfvJuUcIsRla4x/bbOXcd.UgYG9yHEsyU.XvGwpG8GeMNOSH8ANHG'),
(3, '$2b$12$IsXaWuj/.NFv3n9cvGqOMeuZAyDUgCOenZFyk5TKOW1QQacGqwXGS'),
(4, '$2b$12$HTv/BTCMiNuaFTqVQC/PuOCiAE6b9trpjI4q6EXyYXlgYP/g0JeFq'),
(5, '$2b$12$Qorx93u6N6f0u3pZ5oHGk.9R4nN5xErPjxQ9oA9M6U.OD7D1aeX9W'),
(6, '$2b$12$m540PNJNxKOe/HEdgi5S.OeCudtK4Nxa55VPfGofg7h0R7mT3HqOW'),
(7, '$2b$12$lWKgVAmycv3MnXo/MskEfOiDndc1JdSxJ/mopHnuMFjGNWLAEJyc.'),
(8, '$2b$12$1GkRuE1vu6.B7RyB/l2fROEf5tXJuGc92ugxoSmc3gj4Uq2gWkmuW'),
(9, '$2b$12$9JJooBToNDbMVtH8BQAqN.OKg88WwnZrEGB90SgDRXIQfGp4FWweW'),
(10, '$2b$12$p5iNKgp6Uj/GOgjSYK/w0uawWcNKWD2PyMzYS8RFRYdnmYDqRnPSO'),
(11, '$2b$12$VzQjqFFUf.fJFBvHzTGZxOd8F1AP/XPURCyURhS7T21nN5X9nEqoy'),
(12, '$2b$12$WFUaM/ptQSeaGtkPjmLxe.XqiY6YJvWoXsxUHxJ8kMLVeZOW10Tu.'),
(13, '$2b$12$Y09J1spCFz27kSR3791daeQzKDVm0FJ0fTg.5hp/QI5g8wE1RtiDW'),
(14, '$2b$12$6ZpbvhfsaWEPV6hEcQtVWuldiraH7/l3TAVpjilw.mLkkF4gPJlaS'),
(15, '$2b$12$cLdq/x7cQvMdSF2qeuT30OYrvjT5N8usLRjHUr8TLrmK6Sl6ECuf6'),
(16, '$2b$12$L7H5mK6qyVHZTu1TjYPdz.nzFPaPX1RArSiFD0Pr4.qZR5biWcMSm'),
(17, '$2b$12$f/ACjV7qjDvX5MfWQNOSmuXgkd4lOjNIJjkGymRizRCgHw0EFfhRe'),
(18, '$2b$12$MZwDsVbqtf5PM3tqP2CAUOOOy5mhS7oISe3vVUuFunZZaVodNo..O'),
(19, '$2b$12$tInvW0JMFWB2gIcYl3XMSOY1hTC0B7etJZTuYACj2MyQYfeBjdqGO'),
(20, '$2b$12$KAFrL1X21kCraF1DNIQa9u9Gi/KU.usCV2yhtvl93xk0mqWdiaE9q');

--
-- Triggers `password`
--
DELIMITER $$
CREATE TRIGGER `passpass` AFTER INSERT ON `password` FOR EACH ROW BEGIN
	UPDATE credentials
	SET pass_id = NEW.pass_id
	WHERE cred_id = (SELECT MAX(cred_id) FROM credentials); 
end
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `registration`
--

CREATE TABLE `registration` (
  `registration_id` int(11) NOT NULL,
  `email_address` varchar(50) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `phone_number` varchar(11) NOT NULL,
  `created_at` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `registration`
--

INSERT INTO `registration` (`registration_id`, `email_address`, `password`, `phone_number`, `created_at`) VALUES
(1, 'jayreusebio@gmail.com', '$2b$12$E.Rxw7dr3t2ypWo.ZCweUujg2XOthv1LA5C3LxYL6GzRSxP86hlx6', '09506348554', '2026-07-14'),
(2, 'ijayreusebio@gmail.com', '$2b$12$HUvmFcVCvawgHy0LGRxHQuoMBwgFE..8JkMn23jVtM.Ji1e8Fv1Lm', '09090909090', '2026-07-14'),
(14, 'ladygaga@gmail.com', '$2b$12$zYjy5cINHPAKMxBb2M0HKOUTtx6ViuFzJ/FgloM8khkLZ6jOo6FLy', '09654789632', '2026-08-19'),
(21, 'markly@msn.com', '$2b$12$5iy34TySLCoJ2hz8DZvBsOfYGyx1ufCaIkbHBHIsuGn8v9Pt5ECze', '09121234123', '2026-08-27');

-- --------------------------------------------------------

--
-- Table structure for table `reports`
--

CREATE TABLE `reports` (
  `report_id` int(11) NOT NULL,
  `account_id` int(11) NOT NULL,
  `location_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `status` varchar(50) DEFAULT 'Pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `verified_at` timestamp NULL DEFAULT NULL,
  `verified_by` int(11) DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL,
  `public_key` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reports`
--

INSERT INTO `reports` (`report_id`, `account_id`, `location_id`, `title`, `image_url`, `description`, `status`, `created_at`, `verified_at`, `verified_by`, `category`, `public_key`) VALUES
(4, 10, 5, 'Aftermath of the Massive Flood', 'static/uploads/concerns/concern_10_1787150457_flood-aftermath-scene-stockcake.jpg', 'Greetings, esteemed LGU officials! We are reaching out to you today with an urgent and heartfelt plea for assistance from the municipality of Peñaranda, Nueva Ecija. Our community is currently grappling with the devastating aftermath of a massive flood, an event that has profoundly impacted every facet of our daily lives and is significantly hindering our ability to recover and progress. The extensive damage and disruption caused by this natural disaster have left many of our residents in a precarious situation, making it incredibly challenging for us to move forward and rebuild. We desperately need your support and intervention to overcome these immense obstacles and pave the way for our community\'s recovery.', 'In Progress', '2026-08-19 14:40:57', NULL, NULL, 'Flooding', '32da69ca-b5ba-4aa1-957f-fb90d55a0c9a'),
(5, 11, 6, 'Massive Road Pots', 'static/uploads/concerns/concern_11_1787151179_broken-road-destruction-of-road-surface-photo.jpg', 'To the esteemed local government unit and our dearest Mayor of GMN,\r\n\r\nWe, the concerned citizens, are writing to you today with an urgent plea regarding the condition of our local road. The current state of this vital thoroughfare is causing significant distress and poses a serious threat to the safety of our community. The damage is extensive, making it not only difficult to traverse but also highly prone to unfortunate accidents. We implore your good office to intervene and provide the necessary assistance to resolve this pressing issue. Your immediate attention and support in this matter would be deeply appreciated, and we believe that with your help, we can make our roads safer for everyone. Thank you for your anticipated understanding and swift action.', 'Pending', '2026-08-19 14:52:59', NULL, NULL, 'Road', 'e2595970-dd24-4084-9929-100f5e45de81'),
(7, 16, 8, 'Flooding Issues on Main Road', 'static/uploads/concerns/concern_16_1787551223_inbound3228536767509443899.jpg', 'Flooded areas are becoming a hassle with waist deep waters running and can\'t pass by small cars', 'Pending', '2026-08-24 06:00:23', NULL, NULL, 'Flooding', 'b2eb3a2d-6ffa-4577-9792-042281a9d691'),
(8, 15, 9, 'Sirang Street light sa kanto', 'static/uploads/concerns/concern_15_1787551249_1000418396.jpg', 'May nakatumbang poste na ilaw sa kanto, nakakaharang sa daanan.', 'Pending', '2026-08-24 06:00:49', NULL, NULL, 'Lighting', '4c08c407-ee2b-4287-b91e-fca2d1ceb81a'),
(9, 10, 10, 'Tulong LGU', 'static/uploads/concerns/concern_10_1787551270_flood.jpg', 'Dear LGU can please help us to resolve the issue after the massive flood?', 'Pending', '2026-08-24 06:01:10', NULL, NULL, 'Flooding', '393b4bd0-34ee-47c9-8396-a965e5b1ba6b'),
(10, 15, 11, 'Baradong kanal sa kanto ng kamias', 'static/uploads/concerns/concern_15_1787551425_1000418397.jpg', 'Madaming basura na nakabara sa kalsada, kaya\'t ito ay nag dududlot ng baha sa daanan.', 'Pending', '2026-08-24 06:03:45', NULL, NULL, 'Flooding', '76206de4-22f7-4677-9480-cd984ebf46c7'),
(11, 16, 12, 'Fallen Tree on our yard', 'static/uploads/concerns/concern_16_1787551582_inbound7134643433103837327.jpg', 'Patulong po, nabagsak po ung puno dito sa tapat ng aming bahay', 'Pending', '2026-08-24 06:06:22', NULL, NULL, 'Safety', '078dcb4d-59b3-4656-9620-32faadc0e1c5'),
(12, 17, 13, 'Muddy and Slippery Bridge Approach Road', 'static/uploads/concerns/concern_17_1787551609_6769.jpg', 'Yung daan papunta/palabas ng tulay ay puro putik at madulas, lalo na pag umuulan. Yung slope papuntang bridge ay walang proper pavement o hagdan/grip kaya mahirap daanan ng motor at mga sasakyan. Delikado lalo na sa mga sumasakay ng motor dahil sa pagkadulas ng gulong sa putik.', 'Pending', '2026-08-24 06:06:49', NULL, NULL, 'Road', 'f3663f89-9b4d-4d6f-a48f-a3c706fcd519'),
(13, 15, 14, 'Dirty Poultry onTalabutab norte', 'static/uploads/concerns/concern_15_1787551662_1000418398.jpg', 'There was dirty poultry on talabutab norte, it causes foul smell, it needs to have action.', 'Pending', '2026-08-24 06:07:42', NULL, NULL, 'Safety', '317f1b10-8142-4e41-bc78-ca8c5de0047c'),
(14, 17, 15, 'Damaged Streetlight', 'static/uploads/concerns/concern_17_1787551924_6771.jpg', 'Kinakalawang at di na gumagana ang streetlight, nakaka apekto sa naglalakad lalo pag padilim na', 'Pending', '2026-08-24 06:12:04', NULL, NULL, 'Lighting', 'e4626b5d-f068-4662-887e-46e7d98dc307');

-- --------------------------------------------------------

--
-- Table structure for table `report_update`
--

CREATE TABLE `report_update` (
  `reportupd_id` int(11) NOT NULL,
  `account_id` int(11) DEFAULT NULL,
  `report_id` int(11) DEFAULT NULL,
  `image_url` text DEFAULT NULL,
  `description` text DEFAULT NULL,
  `submitted_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `report_update`
--

INSERT INTO `report_update` (`reportupd_id`, `account_id`, `report_id`, `image_url`, `description`, `submitted_at`) VALUES
(1, 1, 1, NULL, 'okay dear resident we are taking this actions of this report we may asssume you that we will take responsibility on this', '2026-07-14 17:51:40'),
(2, 1, 2, NULL, 'jkjvhv', '2026-07-20 11:44:24'),
(3, 1, 1, 'static/uploads/update_1_1784519388_waste.webp', 'still in progress but 50% are now clean, we expected to finish this problem by the end of OCTOBER', '2026-07-20 11:49:48'),
(4, 1, 1, 'static/uploads/update_1_1784520843_clean.webp', 'If you have any concerns or require further clarification regarding this matter, please do not hesitate to report it. Your feedback is valuable and we are here to address any questions or issues you may have, ensuring a comprehensive understanding and resolution.', '2026-07-20 12:14:03'),
(5, 1, 4, NULL, 'Thank you for submitting your report. We have successfully received and recorded the information you provided, and we want to assure you that your concern will be given proper attention.\r\n\r\nOur team will carefully review your report and take the necessary steps to determine the appropriate action regarding the matter. We appreciate your patience and cooperation while we work to address your concern.\r\n\r\nPlease make sure that the contact information you provided is accurate and accessible, as a member of our team may contact you for additional details, clarification, or updates regarding your report.\r\n\r\nThank you for bringing this matter to our attention. We will keep you informed of any developments and will contact you through your provided contact information once there is an update.', '2026-08-19 22:43:27');

-- --------------------------------------------------------

--
-- Table structure for table `role`
--

CREATE TABLE `role` (
  `role_id` int(11) NOT NULL,
  `role` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `role`
--

INSERT INTO `role` (`role_id`, `role`) VALUES
(1, 'resident'),
(2, 'lgu official'),
(3, 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `upvotes`
--

CREATE TABLE `upvotes` (
  `upvote_id` int(11) NOT NULL,
  `report_id` int(11) NOT NULL,
  `account_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `upvotes`
--

INSERT INTO `upvotes` (`upvote_id`, `report_id`, `account_id`) VALUES
(1, 1, 1),
(2, 1, 4),
(3, 2, 1),
(4, 9, 17);

-- --------------------------------------------------------

--
-- Table structure for table `usercreds`
--

CREATE TABLE `usercreds` (
  `user_id` int(11) NOT NULL,
  `contact_id` int(11) DEFAULT NULL,
  `emorph` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `usercreds`
--

INSERT INTO `usercreds` (`user_id`, `contact_id`, `emorph`) VALUES
(1, 1, 'lgu@actbayan.gov.ph'),
(2, 1, '09222222222'),
(3, 2, 'admin@actbayan.gov.ph'),
(4, 2, '09111111111'),
(19, 10, 'ijiayreusebio@gmail.com'),
(20, 10, '09506348554'),
(21, 11, 'fredricksantiabs99@gmail.com'),
(22, 11, '09090909090'),
(27, 14, 'sanfrbs26@gmail.com'),
(28, 14, '09760692055'),
(29, 15, 'lee@gmail.com'),
(30, 15, '09365441563'),
(31, 16, 'markly@gmail.com'),
(32, 16, '09123123412'),
(33, 17, 'halomadlamgpipol@gmail.com'),
(34, 17, '09923456712'),
(35, 18, 'kahitano@gmail.com'),
(36, 18, '09123456789'),
(37, 19, 'markly1@gmail.com'),
(38, 19, '09121234567'),
(39, 20, 'Canva@gmail.com'),
(40, 20, '09946531875');

--
-- Triggers `usercreds`
--
DELIMITER $$
CREATE TRIGGER `insertuser` AFTER INSERT ON `usercreds` FOR EACH ROW BEGIN
	INSERT INTO credentials (user_id) VALUES (NEW.user_id);
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `user_role`
--

CREATE TABLE `user_role` (
  `user_id` int(11) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_role`
--

INSERT INTO `user_role` (`user_id`, `role_id`) VALUES
(1, 2),
(2, 2),
(3, 3),
(4, 3),
(19, 1),
(20, 1),
(21, 1),
(22, 1),
(27, 1),
(28, 1),
(29, 1),
(30, 1),
(31, 1),
(32, 1),
(33, 1),
(34, 1),
(35, 1),
(36, 1),
(37, 1),
(38, 1),
(39, 1),
(40, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`account_id`);

--
-- Indexes for table `activity_logs`
--
ALTER TABLE `activity_logs`
  ADD PRIMARY KEY (`al_id`),
  ADD KEY `report_id` (`report_id`);

--
-- Indexes for table `announcements`
--
ALTER TABLE `announcements`
  ADD PRIMARY KEY (`ann_id`),
  ADD UNIQUE KEY `ann_title` (`ann_title`),
  ADD KEY `account_id` (`account_id`);

--
-- Indexes for table `contacts`
--
ALTER TABLE `contacts`
  ADD PRIMARY KEY (`contact_id`),
  ADD KEY `account_id` (`account_id`);

--
-- Indexes for table `credentials`
--
ALTER TABLE `credentials`
  ADD PRIMARY KEY (`cred_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `pass_id` (`pass_id`);

--
-- Indexes for table `feedbacks`
--
ALTER TABLE `feedbacks`
  ADD PRIMARY KEY (`feedback_id`),
  ADD KEY `account_id` (`account_id`),
  ADD KEY `report_id` (`report_id`);

--
-- Indexes for table `location`
--
ALTER TABLE `location`
  ADD PRIMARY KEY (`location_id`);

--
-- Indexes for table `login_logs`
--
ALTER TABLE `login_logs`
  ADD PRIMARY KEY (`log_id`);

--
-- Indexes for table `password`
--
ALTER TABLE `password`
  ADD PRIMARY KEY (`pass_id`);

--
-- Indexes for table `registration`
--
ALTER TABLE `registration`
  ADD PRIMARY KEY (`registration_id`),
  ADD UNIQUE KEY `email_address` (`email_address`);

--
-- Indexes for table `reports`
--
ALTER TABLE `reports`
  ADD PRIMARY KEY (`report_id`),
  ADD KEY `location_id` (`location_id`),
  ADD KEY `account_id` (`account_id`);

--
-- Indexes for table `report_update`
--
ALTER TABLE `report_update`
  ADD PRIMARY KEY (`reportupd_id`),
  ADD KEY `account_id` (`account_id`),
  ADD KEY `report_id` (`report_id`);

--
-- Indexes for table `role`
--
ALTER TABLE `role`
  ADD PRIMARY KEY (`role_id`);

--
-- Indexes for table `upvotes`
--
ALTER TABLE `upvotes`
  ADD PRIMARY KEY (`upvote_id`);

--
-- Indexes for table `usercreds`
--
ALTER TABLE `usercreds`
  ADD PRIMARY KEY (`user_id`),
  ADD KEY `contact_id` (`contact_id`);

--
-- Indexes for table `user_role`
--
ALTER TABLE `user_role`
  ADD KEY `user_id` (`user_id`),
  ADD KEY `role_id` (`role_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `activity_logs`
--
ALTER TABLE `activity_logs`
  MODIFY `al_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `announcements`
--
ALTER TABLE `announcements`
  MODIFY `ann_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `contacts`
--
ALTER TABLE `contacts`
  MODIFY `contact_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `credentials`
--
ALTER TABLE `credentials`
  MODIFY `cred_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `feedbacks`
--
ALTER TABLE `feedbacks`
  MODIFY `feedback_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `location`
--
ALTER TABLE `location`
  MODIFY `location_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `login_logs`
--
ALTER TABLE `login_logs`
  MODIFY `log_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=77;

--
-- AUTO_INCREMENT for table `password`
--
ALTER TABLE `password`
  MODIFY `pass_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `registration`
--
ALTER TABLE `registration`
  MODIFY `registration_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `reports`
--
ALTER TABLE `reports`
  MODIFY `report_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `report_update`
--
ALTER TABLE `report_update`
  MODIFY `reportupd_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `role`
--
ALTER TABLE `role`
  MODIFY `role_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `upvotes`
--
ALTER TABLE `upvotes`
  MODIFY `upvote_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `usercreds`
--
ALTER TABLE `usercreds`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `activity_logs`
--
ALTER TABLE `activity_logs`
  ADD CONSTRAINT `activity_logs_ibfk_1` FOREIGN KEY (`report_id`) REFERENCES `reports` (`report_id`);

--
-- Constraints for table `announcements`
--
ALTER TABLE `announcements`
  ADD CONSTRAINT `announcements_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`);

--
-- Constraints for table `contacts`
--
ALTER TABLE `contacts`
  ADD CONSTRAINT `contacts_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`);

--
-- Constraints for table `credentials`
--
ALTER TABLE `credentials`
  ADD CONSTRAINT `credentials_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `usercreds` (`user_id`),
  ADD CONSTRAINT `credentials_ibfk_2` FOREIGN KEY (`pass_id`) REFERENCES `password` (`pass_id`);

--
-- Constraints for table `feedbacks`
--
ALTER TABLE `feedbacks`
  ADD CONSTRAINT `feedbacks_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`),
  ADD CONSTRAINT `feedbacks_ibfk_2` FOREIGN KEY (`report_id`) REFERENCES `reports` (`report_id`);

--
-- Constraints for table `reports`
--
ALTER TABLE `reports`
  ADD CONSTRAINT `reports_ibfk_1` FOREIGN KEY (`location_id`) REFERENCES `location` (`location_id`),
  ADD CONSTRAINT `reports_ibfk_2` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`);

--
-- Constraints for table `report_update`
--
ALTER TABLE `report_update`
  ADD CONSTRAINT `report_update_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`),
  ADD CONSTRAINT `report_update_ibfk_2` FOREIGN KEY (`report_id`) REFERENCES `reports` (`report_id`);

--
-- Constraints for table `usercreds`
--
ALTER TABLE `usercreds`
  ADD CONSTRAINT `usercreds_ibfk_1` FOREIGN KEY (`contact_id`) REFERENCES `contacts` (`contact_id`);

--
-- Constraints for table `user_role`
--
ALTER TABLE `user_role`
  ADD CONSTRAINT `user_role_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `usercreds` (`user_id`),
  ADD CONSTRAINT `user_role_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `role` (`role_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
