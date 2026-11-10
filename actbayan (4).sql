-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 10, 2026 at 01:44 PM
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
-- Table structure for table `access_attempt`
--

CREATE TABLE `access_attempt` (
  `attempt_id` int(11) NOT NULL,
  `cred_id` int(11) DEFAULT NULL,
  `credential_used` varchar(100) DEFAULT NULL,
  `attempted_at` datetime DEFAULT NULL,
  `action` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `access_attempt`
--

INSERT INTO `access_attempt` (`attempt_id`, `cred_id`, `credential_used`, `attempted_at`, `action`) VALUES
(1, 3, 'admin@actbayan.gov.ph', '2026-07-14 17:24:41', 'Success'),
(2, 1, 'lgu@actbayan.gov.ph', '2026-07-14 17:25:22', 'Success'),
(3, 1, 'lgu@actbayan.gov.ph', '2026-07-14 17:37:43', 'Success'),
(4, 19, 'ijiayreusebio@gmail.com', '2026-07-14 17:38:22', 'Success'),
(5, 19, 'ijiayreusebio@gmail.com', '2026-07-14 17:43:14', 'Success'),
(6, 1, 'lgu@actbayan.gov.ph', '2026-07-14 17:50:46', 'Success'),
(7, 3, 'admin@actbayan.gov.ph', '2026-07-14 19:37:15', 'Success'),
(8, 3, 'admin@actbayan.gov.ph', '2026-07-14 19:37:42', 'Success'),
(9, 19, 'ijiayreusebio@gmail.com', '2026-07-14 20:04:22', 'Success'),
(10, 19, 'ijiayreusebio@gmail.com', '2026-07-14 20:09:43', 'Success'),
(11, 3, 'admin@actbayan.gov.ph', '2026-07-14 20:56:05', 'Success'),
(12, 19, 'ijiayreusebio@gmail.com', '2026-07-14 20:57:14', 'Success'),
(13, 1, 'lgu@actbayan.gov.ph', '2026-07-14 23:22:28', 'Success'),
(14, NULL, 'ferdinandjreusebio@gmail.com', '2026-07-14 23:25:22', 'Success'),
(15, NULL, 'ferdinandjreusebio@gmail.com', '2026-07-14 23:31:04', 'Success'),
(16, 19, 'ijiayreusebio@gmail.com', '2026-07-20 09:44:29', 'Success'),
(17, 1, 'lgu@actbayan.gov.ph', '2026-07-20 11:43:15', 'Success'),
(18, 3, 'admin@actbayan.gov.ph', '2026-07-20 11:50:36', 'Success'),
(19, 27, 'sanfrbs26@gmail.com', '2026-07-20 11:52:03', 'Failed'),
(20, 3, 'admin@actbayan.gov.ph', '2026-07-20 11:52:05', 'Success'),
(21, 1, 'lgu@actbayan.gov.ph', '2026-07-20 11:54:40', 'Success'),
(22, 3, 'admin@actbayan.gov.ph', '2026-07-20 11:55:00', 'Success'),
(23, 1, 'lgu@actbayan.gov.ph', '2026-07-20 12:01:11', 'Success'),
(24, 27, 'sanfrbs26@gmail.com', '2026-07-20 12:12:41', 'Success'),
(25, 19, 'ijiayreusebio@gmail.com', '2026-07-20 12:17:27', 'Success'),
(26, NULL, 'lesterromero14@gamil.com', '2026-07-20 18:37:28', 'Failed'),
(27, 1, 'lgu@actbayan.gov.ph', '2026-07-20 18:38:34', 'Success'),
(28, NULL, 'jayreusebio@gmail.com', '2026-07-20 18:43:29', 'Failed'),
(29, 19, 'ijiayreusebio@gmail.com', '2026-07-20 18:43:48', 'Success'),
(30, NULL, 'lesterromero14@gmail.com', '2026-07-20 18:46:21', 'Failed'),
(31, NULL, 'lesterromero14@gmail.com', '2026-07-20 18:46:48', 'Failed'),
(32, NULL, 'lesterromero14@gmail.com', '2026-07-20 18:48:14', 'Failed'),
(33, 1, 'lgu@actbayan.gov.ph', '2026-07-20 18:55:09', 'Success'),
(34, NULL, 'lesterandreimatiasromero@gmail.com', '2026-07-20 18:57:35', 'Success'),
(35, NULL, 'lesterandreimatiasromero@gmail.com', '2026-07-20 18:58:50', 'Success'),
(36, NULL, 'jayreusebio@gmail.com', '2026-07-20 19:00:29', 'Failed'),
(37, 19, 'ijiayreusebio@gmail.com', '2026-08-14 22:21:55', 'Success'),
(38, 19, 'ijiayreusebio@gmail.com', '2026-08-14 23:39:20', 'Success'),
(39, 19, 'ijiayreusebio@gmail.com', '2026-08-19 21:38:30', 'Success'),
(40, 19, 'ijiayreusebio@gmail.com', '2026-08-19 21:39:24', 'Success'),
(41, 19, 'ijiayreusebio@gmail.com', '2026-08-19 22:15:24', 'Success'),
(42, 3, 'admin@actbayan.gov.ph', '2026-08-19 22:28:33', 'Success'),
(43, 19, 'ijiayreusebio@gmail.com', '2026-08-19 22:34:09', 'Failed'),
(44, 19, 'ijiayreusebio@gmail.com', '2026-08-19 22:34:13', 'Failed'),
(45, 1, 'lgu@actbayan.gov.ph', '2026-08-19 22:38:13', 'Success'),
(46, 3, 'admin@actbayan.gov.ph', '2026-08-19 22:57:32', 'Success'),
(47, NULL, 'ladygaga@gmail.com', '2026-08-19 23:19:24', 'Failed (Banned)'),
(48, NULL, 'ladygaga@gmail.com', '2026-08-19 23:19:40', 'Success'),
(49, NULL, 'ladygaga@gmail.com', '2026-08-19 23:19:57', 'Failed (Banned)'),
(50, NULL, 'ladygaga@gmail.com', '2026-08-19 23:20:32', 'Failed'),
(51, 1, 'lgu@actbayan.gov.ph', '2026-08-20 10:29:07', 'Success'),
(52, 3, 'admin@actbayan.gov.ph', '2026-08-20 10:36:47', 'Success'),
(53, 27, 'sanfrbs26@gmail.com', '2026-08-20 10:58:44', 'Success'),
(54, 19, 'ijiayreusebio@gmail.com', '2026-08-24 11:28:24', 'Success'),
(55, 1, 'lgu@actbayan.gov.ph', '2026-08-24 13:50:17', 'Success'),
(56, 27, 'sanfrbs26@gmail.com', '2026-08-24 13:53:26', 'Success'),
(57, 27, 'sanfrbs26@gmail.com', '2026-08-24 13:56:37', 'Success'),
(58, 29, 'lee@gmail.com', '2026-08-24 13:57:37', 'Failed'),
(59, 29, 'lee@gmail.com', '2026-08-24 13:57:58', 'Success'),
(60, 19, 'ijiayreusebio@gmail.com', '2026-08-24 13:59:06', 'Success'),
(61, 3, 'admin@actbayan.gov.ph', '2026-08-24 14:16:05', 'Success'),
(62, 1, 'lgu@actbayan.gov.ph', '2026-08-24 14:16:59', 'Success'),
(63, 27, 'sanfrbs26@gmail.com', '2026-08-27 21:55:57', 'Failed'),
(64, 27, 'sanfrbs26@gmail.com', '2026-08-27 21:56:07', 'Success'),
(65, 29, 'lee@gmail.com', '2026-08-27 21:56:22', 'Success'),
(66, 31, 'markly@gmail.com', '2026-08-27 21:57:45', 'Success'),
(67, 1, 'lgu@actbayan.gov.ph', '2026-08-27 22:12:20', 'Success'),
(68, 3, 'admin@actbayan.gov.ph', '2026-08-27 22:13:33', 'Success'),
(69, 37, 'markly1@gmail.com', '2026-08-27 22:16:53', 'Success'),
(70, 31, 'markly@gmail.com', '2026-08-27 22:17:31', 'Success'),
(71, 1, 'lgu@actbayan.gov.ph', '2026-08-27 22:18:22', 'Success'),
(72, 31, 'markly@gmail.com', '2026-08-27 22:21:20', 'Success'),
(73, 37, 'markly1@gmail.com', '2026-08-27 22:24:00', 'Success'),
(74, 19, 'ijiayreusebio@gmail.com', '2026-08-27 23:07:15', 'Success'),
(75, 19, 'ijiayreusebio@gmail.com', '2026-08-27 23:12:10', 'Success'),
(76, 39, 'Canva@gmail.com', '2026-08-28 00:02:11', 'Success'),
(77, 27, 'sanfrbs26@gmail.com', '2026-11-05 14:30:51', 'Success'),
(78, 27, 'sanfrbs26@gmail.com', '2026-11-05 14:59:59', 'Logout'),
(79, 1, 'lgu@actbayan.gov.ph', '2026-11-05 15:00:08', 'Success'),
(80, 1, 'lgu@actbayan.gov.ph', '2026-11-05 15:01:42', 'Logout'),
(81, 27, 'sanfrbs26@gmail.com', '2026-11-05 15:01:50', 'Success'),
(82, NULL, 'justineleepineda04@gmail.com', '2026-11-05 15:06:27', 'Failed'),
(83, NULL, 'leepineda.neust@gmail.com', '2026-11-05 15:06:47', 'Failed'),
(84, NULL, 'justineleepineda04@gmail.com', '2026-11-05 15:07:02', 'Failed'),
(85, NULL, 'leepineda.neust@gmail.com', '2026-11-05 15:07:15', 'Failed'),
(86, 27, 'sanfrbs26@gmail.com', '2026-11-05 15:16:10', 'Logout'),
(87, 1, 'lgu@actbayan.gov.ph', '2026-11-05 15:16:22', 'Success'),
(88, 1, 'lgu@actbayan.gov.ph', '2026-11-05 15:16:59', 'Logout'),
(89, 27, 'sanfrbs26@gmail.com', '2026-11-05 15:17:05', 'Success'),
(90, 27, 'sanfrbs26@gmail.com', '2026-11-05 15:39:42', 'Logout'),
(91, 1, 'lgu@actbayan.gov.ph', '2026-11-05 15:39:53', 'Success'),
(92, 1, 'lgu@actbayan.gov.ph', '2026-11-05 16:16:36', 'Success'),
(93, 1, 'lgu@actbayan.gov.ph', '2026-11-05 16:30:03', 'Success'),
(94, 1, 'lgu@actbayan.gov.ph', '2026-11-05 16:30:58', 'Logout'),
(95, 27, 'sanfrbs26@gmail.com', '2026-11-05 16:31:09', 'Success'),
(96, 27, 'sanfrbs26@gmail.com', '2026-11-05 16:31:31', 'Logout'),
(97, 1, 'lgu@actbayan.gov.ph', '2026-11-05 16:31:41', 'Success'),
(98, 1, 'lgu@actbayan.gov.ph', '2026-11-05 16:40:35', 'Logout'),
(99, 1, 'lgu@actbayan.gov.ph', '2026-11-05 16:41:21', 'Success'),
(100, 1, 'lgu@actbayan.gov.ph', '2026-11-05 16:55:06', 'Logout'),
(101, NULL, 'admin@gmail.com', '2026-11-05 16:55:13', 'Failed'),
(102, 3, 'admin@actbayan.gov.ph', '2026-11-05 16:55:20', 'Success'),
(103, 3, 'admin@actbayan.gov.ph', '2026-11-05 17:06:20', 'Logout'),
(104, 27, 'sanfrbs26@gmail.com', '2026-11-05 17:06:27', 'Success'),
(105, 27, 'sanfrbs26@gmail.com', '2026-11-05 17:13:01', 'Success'),
(106, 27, 'sanfrbs26@gmail.com', '2026-11-05 17:23:36', 'Success'),
(107, 27, 'sanfrbs26@gmail.com', '2026-11-05 17:29:52', 'Logout'),
(108, 27, 'sanfrbs26@gmail.com', '2026-11-05 17:30:35', 'Success'),
(109, 27, 'sanfrbs26@gmail.com', '2026-11-05 18:17:27', 'Logout'),
(110, 1, 'lgu@actbayan.gov.ph', '2026-11-05 18:17:36', 'Success'),
(111, 1, 'lgu@actbayan.gov.ph', '2026-11-05 18:19:19', 'Logout'),
(112, 27, 'sanfrbs26@gmail.com', '2026-11-05 18:19:30', 'Success'),
(113, 27, 'sanfrbs26@gmail.com', '2026-11-05 18:24:27', 'Logout'),
(114, 1, 'lgu@actbayan.gov.ph', '2026-11-05 18:24:40', 'Failed'),
(115, 1, 'lgu@actbayan.gov.ph', '2026-11-05 18:24:49', 'Success'),
(116, 1, 'lgu@actbayan.gov.ph', '2026-11-05 18:30:15', 'Logout'),
(117, 27, 'sanfrbs26@gmail.com', '2026-11-05 18:30:24', 'Success'),
(118, 27, 'sanfrbs26@gmail.com', '2026-11-06 09:17:48', 'Success'),
(119, 27, 'sanfrbs26@gmail.com', '2026-11-06 09:20:37', 'Logout'),
(120, 1, 'lgu@actbayan.gov.ph', '2026-11-06 09:20:47', 'Success'),
(121, 1, 'lgu@actbayan.gov.ph', '2026-11-06 09:21:22', 'Logout'),
(122, 3, 'admin@actbayan.gov.ph', '2026-11-06 09:21:30', 'Success'),
(123, 3, 'admin@actbayan.gov.ph', '2026-11-06 09:23:06', 'Logout'),
(124, 27, 'sanfrbs26@gmail.com', '2026-11-06 09:26:46', 'Success'),
(125, 27, 'sanfrbs26@gmail.com', '2026-11-06 09:30:36', 'Logout'),
(126, 27, 'sanfrbs26@gmail.com', '2026-11-06 12:54:20', 'Success'),
(127, 27, 'sanfrbs26@gmail.com', '2026-11-06 13:26:44', 'Success'),
(128, 27, 'sanfrbs26@gmail.com', '2026-11-06 13:28:51', 'Success'),
(129, 27, 'sanfrbs26@gmail.com', '2026-11-06 13:30:52', 'Success'),
(130, 27, 'sanfrbs26@gmail.com', '2026-11-06 14:10:23', 'Logout'),
(131, 3, 'admin@actbayan.gov.ph', '2026-11-06 14:10:32', 'Success');

-- --------------------------------------------------------

--
-- Table structure for table `accounts`
--

CREATE TABLE `accounts` (
  `account_id` int(11) NOT NULL,
  `contact_id` int(11) DEFAULT NULL,
  `address_id` int(11) DEFAULT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `middle_initial` varchar(10) DEFAULT NULL,
  `dob` date NOT NULL,
  `id_path` text DEFAULT NULL,
  `selfie_path` text DEFAULT NULL,
  `category` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts`
--

INSERT INTO `accounts` (`account_id`, `contact_id`, `address_id`, `first_name`, `last_name`, `middle_initial`, `dob`, `id_path`, `selfie_path`, `category`) VALUES
(1, 1, 1, 'LGU', 'Official', '', '1990-01-01', NULL, NULL, NULL),
(2, 2, 2, 'System', 'Admin', '', '1990-01-01', NULL, NULL, NULL),
(10, 10, 10, 'Ferdinand Jr', 'Eusebio', 'D', '2005-05-05', NULL, NULL, NULL),
(11, 11, 11, 'Fred Rick', 'Santiago', 'B', '2005-03-26', NULL, NULL, NULL),
(15, 14, 15, 'Fred Rick', 'Santiago', '', '2010-09-05', NULL, NULL, NULL),
(16, 15, 16, 'Lee', 'Pineda', 'G', '2005-01-24', NULL, NULL, NULL),
(17, 16, 17, 'Markly Harrison', 'Magbuhos', '', '2005-08-12', NULL, NULL, NULL),
(18, 17, 18, 'Juan', 'Dela cruz', 'M', '2006-01-19', NULL, NULL, NULL),
(19, 18, 19, 'joe', 'MaMa', '', '2011-08-24', NULL, NULL, NULL),
(20, 19, 20, 'Markly', 'Magbuhos', '', '2011-08-27', NULL, NULL, NULL),
(22, 22, 24, 'Lee', 'Gonzales', 'P', '2005-04-04', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `activity_media`
--

CREATE TABLE `activity_media` (
  `activity_id` int(11) NOT NULL,
  `path` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `activity_media`
--

INSERT INTO `activity_media` (`activity_id`, `path`) VALUES
(3, 'static/uploads/update_1_1784519388_waste.webp'),
(4, 'static/uploads/update_1_1784520843_clean.webp'),
(9, 'static/uploads/update_15_1793862091_Screenshot_577.png');

-- --------------------------------------------------------

--
-- Table structure for table `address`
--

CREATE TABLE `address` (
  `address_id` int(11) NOT NULL,
  `house_no` varchar(100) DEFAULT NULL,
  `street` varchar(100) DEFAULT NULL,
  `brgyorsubd` varchar(100) DEFAULT NULL,
  `cityormunicipality` varchar(100) DEFAULT NULL,
  `province` varchar(100) DEFAULT NULL,
  `postalcode` varchar(20) DEFAULT NULL,
  `country` varchar(100) DEFAULT 'Philippines'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `address`
--

INSERT INTO `address` (`address_id`, `house_no`, `street`, `brgyorsubd`, `cityormunicipality`, `province`, `postalcode`, `country`) VALUES
(1, NULL, NULL, NULL, NULL, NULL, NULL, 'Philippines'),
(2, NULL, NULL, NULL, NULL, NULL, NULL, 'Philippines'),
(10, '0327', 'Zone 4', 'Partida', 'San Miguel', 'Bulacan', NULL, 'Philippines'),
(11, '111', 'Calamansi', 'Bravo', 'General Mamerto Natividad', 'Nueva Ecija', NULL, 'Philippines'),
(15, 'NA', 'NA', 'San Francisco', 'Llanera', 'Nueva Ecija', NULL, 'Philippines'),
(16, 'Blk 1', 'Mabini', 'Buga', 'San Miguel', 'Bulacan', NULL, 'Philippines'),
(17, '123', 'Ipil St. ', 'Mataas na Kahoy', 'General Mamerto Natividad', 'Nueva Ecija', NULL, 'Philippines'),
(18, '0992', 'Zone4', 'Magsaysay Pob', 'Jovellar', 'Albay', NULL, 'Philippines'),
(19, 'isid', 'jeje', 'Bita', 'Culasi', 'Antique', NULL, 'Philippines'),
(20, '474', 'Ipil St. ', 'Mataas na Kahoy', 'General Mamerto Natividad', 'Nueva Ecija', NULL, 'Philippines'),
(22, '0992', 'Zone 5', 'Panacsac', 'General Mamerto Natividad', 'Nueva Ecija', NULL, 'Philippines'),
(24, 'Blk 1 Lot 5', 'Esmering Street', 'Pulong Singkamas', 'General Mamerto Natividad', 'Nueva Ecija', NULL, 'Philippines');

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
  `email` varchar(100) DEFAULT NULL,
  `phone_number` varchar(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contacts`
--

INSERT INTO `contacts` (`contact_id`, `email`, `phone_number`) VALUES
(1, 'lgu@actbayan.gov.ph', '09222222222'),
(2, 'admin@actbayan.gov.ph', '09111111111'),
(10, 'ijiayreusebio@gmail.com', '09506348554'),
(11, 'fredricksantiabs99@gmail.com', '09090909090'),
(14, 'sanfrbs26@gmail.com', '09760692055'),
(15, 'lee@gmail.com', '09365441563'),
(16, 'markly@gmail.com', '09123123412'),
(17, 'halomadlamgpipol@gmail.com', '09923456712'),
(18, 'kahitano@gmail.com', '09123456789'),
(19, 'markly1@gmail.com', '09121234567'),
(20, 'Canva@gmail.com', '09946531875'),
(22, 'bedrockdawn@gmail.com', '09567334559');

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
  `last_failed_at` datetime DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `last_active_on` datetime DEFAULT NULL,
  `is_locked` varchar(100) DEFAULT NULL,
  `is_banned` tinyint(1) DEFAULT 0,
  `ban_duration` int(11) DEFAULT NULL,
  `lock_duration` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `credentials`
--

INSERT INTO `credentials` (`cred_id`, `user_id`, `pass_id`, `last_failed_at`, `is_active`, `last_active_on`, `is_locked`, `is_banned`, `ban_duration`, `lock_duration`) VALUES
(1, 1, 1, '2026-11-05 18:24:40', 0, '2026-11-06 09:21:22', 'N', 0, NULL, NULL),
(2, 2, 1, NULL, 1, NULL, 'N', 0, NULL, NULL),
(3, 3, 2, NULL, 1, '2026-11-06 14:10:32', 'N', 0, NULL, NULL),
(4, 4, 2, NULL, 1, NULL, 'N', 0, NULL, NULL),
(19, 19, 10, '2026-08-19 22:34:13', 1, '2026-08-27 23:12:10', NULL, 0, NULL, NULL),
(20, 20, 10, NULL, 1, NULL, NULL, 0, NULL, NULL),
(21, 21, 11, NULL, 1, NULL, NULL, 0, NULL, NULL),
(22, 22, 11, NULL, 1, NULL, NULL, 0, NULL, NULL),
(27, 27, 14, '2026-08-27 21:55:57', 0, '2026-11-06 14:10:23', NULL, 0, NULL, NULL),
(28, 28, 14, NULL, 1, NULL, NULL, 0, NULL, NULL),
(29, 29, 15, '2026-08-24 13:57:37', 1, '2026-08-27 21:56:22', NULL, 0, NULL, NULL),
(30, 30, 15, NULL, 1, NULL, NULL, 0, NULL, NULL),
(31, 31, 16, NULL, 1, '2026-08-27 22:21:20', NULL, 0, NULL, NULL),
(32, 32, 16, NULL, 1, NULL, NULL, 0, NULL, NULL),
(33, 33, 17, NULL, 1, NULL, NULL, 0, NULL, NULL),
(34, 34, 17, NULL, 1, NULL, NULL, 0, NULL, NULL),
(35, 35, 18, NULL, 1, NULL, NULL, 0, NULL, NULL),
(36, 36, 18, NULL, 1, NULL, NULL, 0, NULL, NULL),
(37, 37, 19, NULL, 1, '2026-08-27 22:24:00', NULL, 0, NULL, NULL),
(38, 38, 19, NULL, 1, NULL, NULL, 0, NULL, NULL),
(39, 39, 20, NULL, 1, '2026-08-28 00:02:11', NULL, 0, NULL, NULL),
(40, 40, 20, NULL, 1, NULL, NULL, 0, NULL, NULL),
(43, 43, 21, NULL, 1, NULL, 'N', 0, NULL, NULL),
(44, 44, 21, NULL, 1, NULL, NULL, 0, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `location`
--

CREATE TABLE `location` (
  `location_id` int(11) NOT NULL,
  `x` decimal(10,7) NOT NULL,
  `y` decimal(10,7) NOT NULL,
  `locname` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `location`
--

INSERT INTO `location` (`location_id`, `x`, `y`, `locname`) VALUES
(1, 15.2023548, 121.0151596, NULL),
(2, 15.2024326, 121.0152243, NULL),
(4, 15.4453067, 120.9447569, NULL),
(5, 15.4453335, 120.9447505, NULL),
(6, 15.4453335, 120.9447505, NULL),
(7, 15.6041223, 121.0504937, NULL),
(8, 15.6031679, 121.0503244, NULL),
(9, 15.6045570, 121.0520606, NULL),
(10, 15.6054973, 121.0528767, NULL),
(11, 15.6021648, 121.0498082, NULL),
(12, 15.6050221, 121.0491443, NULL),
(13, 15.6098064, 121.0176801, NULL),
(14, 15.6010333, 121.0782158, NULL),
(15, 15.6084758, 121.0194317, NULL),
(16, 15.4495178, 120.9401655, NULL),
(17, 15.4443120, 120.9436710, 'Cabanatuan, Nueva Ecija'),
(18, 15.4440988, 120.9448171, 'Cabanatuan, Nueva Ecija');

-- --------------------------------------------------------

--
-- Table structure for table `password`
--

CREATE TABLE `password` (
  `pass_id` int(11) NOT NULL,
  `password_hash` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `password`
--

INSERT INTO `password` (`pass_id`, `password_hash`) VALUES
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
(20, '$2b$12$KAFrL1X21kCraF1DNIQa9u9Gi/KU.usCV2yhtvl93xk0mqWdiaE9q'),
(21, '$2b$12$S1EykR04cd5veueDQOFQ/OWFqgwEOGr51pdk09n/QoEVDYVT4ZaaS');

--
-- Triggers `password`
--
DELIMITER $$
CREATE TRIGGER `passpass` AFTER INSERT ON `password` FOR EACH ROW BEGIN
    UPDATE credentials
    SET pass_id = NEW.pass_id
    WHERE cred_id = (SELECT MAX(cred_id) FROM (SELECT cred_id FROM credentials) AS temp);
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `registration`
--

CREATE TABLE `registration` (
  `registration_id` int(11) NOT NULL,
  `email_address` varchar(50) NOT NULL,
  `phone_number` varchar(11) NOT NULL,
  `password_hash` varchar(255) DEFAULT NULL,
  `created_at` date NOT NULL DEFAULT current_timestamp(),
  `verified_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `registration`
--

INSERT INTO `registration` (`registration_id`, `email_address`, `phone_number`, `password_hash`, `created_at`, `verified_at`) VALUES
(1, 'jayreusebio@gmail.com', '09506348554', '$2b$12$E.Rxw7dr3t2ypWo.ZCweUujg2XOthv1LA5C3LxYL6GzRSxP86hlx6', '2026-07-14', NULL),
(2, 'ijayreusebio@gmail.com', '09090909090', '$2b$12$HUvmFcVCvawgHy0LGRxHQuoMBwgFE..8JkMn23jVtM.Ji1e8Fv1Lm', '2026-07-14', NULL),
(14, 'ladygaga@gmail.com', '09654789632', '$2b$12$zYjy5cINHPAKMxBb2M0HKOUTtx6ViuFzJ/FgloM8khkLZ6jOo6FLy', '2026-08-19', NULL),
(21, 'markly@msn.com', '09121234123', '$2b$12$5iy34TySLCoJ2hz8DZvBsOfYGyx1ufCaIkbHBHIsuGn8v9Pt5ECze', '2026-08-27', NULL),
(23, 'earlzhane123@gmail.com', '09666308045', '$2b$12$AMk5iOF5cRy6bL/ISCkgf.TZhBYov1gvrMEVgutKy0qdqCJLtGtue', '2026-11-10', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `reports`
--

CREATE TABLE `reports` (
  `report_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `location_id` int(11) NOT NULL,
  `description` text DEFAULT NULL,
  `status` varchar(50) DEFAULT 'Pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `last_activity` timestamp NULL DEFAULT NULL,
  `public_key` varchar(255) DEFAULT NULL,
  `upvote_count` int(11) NOT NULL DEFAULT 0,
  `category` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reports`
--

INSERT INTO `reports` (`report_id`, `title`, `location_id`, `description`, `status`, `created_at`, `last_activity`, `public_key`, `upvote_count`, `category`) VALUES
(4, 'Aftermath of the Massive Flood', 5, 'Greetings, esteemed LGU officials! We are reaching out to you today with an urgent and heartfelt plea for assistance from the municipality of Peñaranda, Nueva Ecija. Our community is currently grappling with the devastating aftermath of a massive flood, an event that has profoundly impacted every facet of our daily lives and is significantly hindering our ability to recover and progress. The extensive damage and disruption caused by this natural disaster have left many of our residents in a precarious situation, making it incredibly challenging for us to move forward and rebuild. We desperately need your support and intervention to overcome these immense obstacles and pave the way for our community\'s recovery.', 'In Progress', '2026-08-19 14:40:57', '2026-08-19 22:43:27', '32da69ca-b5ba-4aa1-957f-fb90d55a0c9a', 0, NULL),
(5, 'Massive Road Pots', 6, 'To the esteemed local government unit and our dearest Mayor of GMN,\r\n\r\nWe, the concerned citizens, are writing to you today with an urgent plea regarding the condition of our local road. The current state of this vital thoroughfare is causing significant distress and poses a serious threat to the safety of our community. The damage is extensive, making it not only difficult to traverse but also highly prone to unfortunate accidents. We implore your good office to intervene and provide the necessary assistance to resolve this pressing issue. Your immediate attention and support in this matter would be deeply appreciated, and we believe that with your help, we can make our roads safer for everyone. Thank you for your anticipated understanding and swift action.', 'Pending', '2026-08-19 14:52:59', '2026-08-19 14:52:59', 'e2595970-dd24-4084-9929-100f5e45de81', 0, NULL),
(7, 'Flooding Issues on Main Road', 8, 'Flooded areas are becoming a hassle with waist deep waters running and can\'t pass by small cars', 'Pending', '2026-08-24 06:00:23', '2026-08-24 06:00:23', 'b2eb3a2d-6ffa-4577-9792-042281a9d691', 0, NULL),
(8, 'Sirang Street light sa kanto', 9, 'May nakatumbang poste na ilaw sa kanto, nakakaharang sa daanan.', 'Pending', '2026-08-24 06:00:49', '2026-08-24 06:00:49', '4c08c407-ee2b-4287-b91e-fca2d1ceb81a', 0, NULL),
(9, 'Tulong LGU', 10, 'Dear LGU can please help us to resolve the issue after the massive flood?', 'Pending', '2026-08-24 06:01:10', '2026-08-24 06:01:10', '393b4bd0-34ee-47c9-8396-a965e5b1ba6b', 1, NULL),
(10, 'Baradong kanal sa kanto ng kamias', 11, 'Madaming basura na nakabara sa kalsada, kaya\'t ito ay nag dududlot ng baha sa daanan.', 'Pending', '2026-08-24 06:03:45', '2026-08-24 06:03:45', '76206de4-22f7-4677-9480-cd984ebf46c7', 1, NULL),
(11, 'Fallen Tree on our yard', 12, 'Patulong po, nabagsak po ung puno dito sa tapat ng aming bahay', 'Pending', '2026-08-24 06:06:22', '2026-08-24 06:06:22', '078dcb4d-59b3-4656-9620-32faadc0e1c5', 0, NULL),
(12, 'Muddy and Slippery Bridge Approach Road', 13, 'Yung daan papunta/palabas ng tulay ay puro putik at madulas, lalo na pag umuulan. Yung slope papuntang bridge ay walang proper pavement o hagdan/grip kaya mahirap daanan ng motor at mga sasakyan. Delikado lalo na sa mga sumasakay ng motor dahil sa pagkadulas ng gulong sa putik.', 'Pending', '2026-08-24 06:06:49', '2026-08-24 06:06:49', 'f3663f89-9b4d-4d6f-a48f-a3c706fcd519', 2, NULL),
(13, 'Dirty Poultry onTalabutab norte', 14, 'There was dirty poultry on talabutab norte, it causes foul smell, it needs to have action.', 'Pending', '2026-08-24 06:07:42', '2026-08-24 06:07:42', '317f1b10-8142-4e41-bc78-ca8c5de0047c', 1, NULL),
(14, 'Damaged Streetlight', 15, 'Kinakalawang at di na gumagana ang streetlight, nakaka apekto sa naglalakad lalo pag padilim na', 'Pending', '2026-08-24 06:12:04', '2026-08-24 06:12:04', 'e4626b5d-f068-4662-887e-46e7d98dc307', 1, NULL),
(15, 'GLKADGJLKALK', 17, 'iiykgjvjdtjcgj', 'In Progress', '2026-11-05 06:59:19', '2026-11-05 08:30:37', '96c182eb-91ab-4a00-ab36-a1254f225212', 2, NULL),
(16, 'Putol na kahoy', 18, 'MLDFADSKFKMLS', 'Pending', '2026-11-05 10:31:48', '2026-11-05 10:31:48', '269db4ca-b6cf-4bee-8e5f-53582501b47f', 0, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `reports_media`
--

CREATE TABLE `reports_media` (
  `report_id` int(11) NOT NULL,
  `path` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reports_media`
--

INSERT INTO `reports_media` (`report_id`, `path`) VALUES
(4, 'static/uploads/concerns/concern_10_1787150457_flood-aftermath-scene-stockcake.jpg'),
(5, 'static/uploads/concerns/concern_11_1787151179_broken-road-destruction-of-road-surface-photo.jpg'),
(7, 'static/uploads/concerns/concern_16_1787551223_inbound3228536767509443899.jpg'),
(8, 'static/uploads/concerns/concern_15_1787551249_1000418396.jpg'),
(9, 'static/uploads/concerns/concern_10_1787551270_flood.jpg'),
(10, 'static/uploads/concerns/concern_15_1787551425_1000418397.jpg'),
(11, 'static/uploads/concerns/concern_16_1787551582_inbound7134643433103837327.jpg'),
(12, 'static/uploads/concerns/concern_17_1787551609_6769.jpg'),
(13, 'static/uploads/concerns/concern_15_1787551662_1000418398.jpg'),
(14, 'static/uploads/concerns/concern_17_1787551924_6771.jpg'),
(15, 'static/uploads/concerns/concern_15_1793861959_0_Screenshot_540.png'),
(16, 'static/uploads/concerns/concern_15_1793874708_0_Screenshot_580.png'),
(16, 'static/uploads/concerns/concern_15_1793874708_1_Screenshot_573.png'),
(16, 'static/uploads/concerns/concern_15_1793874708_2_Screenshot_519.png');

-- --------------------------------------------------------

--
-- Table structure for table `report_activity`
--

CREATE TABLE `report_activity` (
  `activity_id` int(11) NOT NULL,
  `account_id` int(11) DEFAULT NULL,
  `report_id` int(11) DEFAULT NULL,
  `activity_type` varchar(50) NOT NULL,
  `content` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `report_activity`
--

INSERT INTO `report_activity` (`activity_id`, `account_id`, `report_id`, `activity_type`, `content`) VALUES
(1, 1, 1, 'report_update', 'okay dear resident we are taking this actions of this report we may asssume you that we will take responsibility on this'),
(2, 1, 2, 'report_update', 'jkjvhv'),
(3, 1, 1, 'report_update', 'still in progress but 50% are now clean, we expected to finish this problem by the end of OCTOBER'),
(4, 1, 1, 'report_update', 'If you have any concerns or require further clarification regarding this matter, please do not hesitate to report it. Your feedback is valuable and we are here to address any questions or issues you may have, ensuring a comprehensive understanding and resolution.'),
(5, 1, 4, 'report_update', 'Thank you for submitting your report. We have successfully received and recorded the information you provided, and we want to assure you that your concern will be given proper attention.\r\n\r\nOur team will carefully review your report and take the necessary steps to determine the appropriate action regarding the matter. We appreciate your patience and cooperation while we work to address your concern.\r\n\r\nPlease make sure that the contact information you provided is accurate and accessible, as a member of our team may contact you for additional details, clarification, or updates regarding your report.\r\n\r\nThank you for bringing this matter to our attention. We will keep you informed of any developments and will contact you through your provided contact information once there is an update.'),
(6, 4, 1, 'feedbacks', 'lmao'),
(7, 6, 1, 'feedbacks', 'okay pu'),
(8, 15, 15, 'report_created', 'GLKADGJLKALK'),
(9, 1, 15, 'report_update', 'nakita kona,awla akong pake'),
(10, 15, 15, 'feedbacks', 'english'),
(14, 22, 14, 'upvote', 'upvote'),
(15, 22, 13, 'upvote', 'upvote'),
(16, 22, 12, 'upvote', 'upvote'),
(17, 22, 15, 'upvote', 'upvote'),
(18, 1, 15, 'report_update', '75%na'),
(19, 15, 10, 'upvote', 'upvote'),
(21, 15, 16, 'report_created', 'Putol na kahoy'),
(25, 15, 12, 'upvote', 'upvote'),
(32, 15, 15, 'upvote', 'upvote');

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
(40, 20, '09946531875'),
(43, 22, 'bedrockdawn@gmail.com'),
(44, 22, '09567334559');

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
(40, 1),
(43, 1),
(44, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `access_attempt`
--
ALTER TABLE `access_attempt`
  ADD PRIMARY KEY (`attempt_id`),
  ADD KEY `cred_id` (`cred_id`);

--
-- Indexes for table `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`account_id`),
  ADD KEY `contact_id` (`contact_id`),
  ADD KEY `address_id` (`address_id`);

--
-- Indexes for table `activity_media`
--
ALTER TABLE `activity_media`
  ADD KEY `activity_id` (`activity_id`);

--
-- Indexes for table `address`
--
ALTER TABLE `address`
  ADD PRIMARY KEY (`address_id`);

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
  ADD PRIMARY KEY (`contact_id`);

--
-- Indexes for table `credentials`
--
ALTER TABLE `credentials`
  ADD PRIMARY KEY (`cred_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `pass_id` (`pass_id`);

--
-- Indexes for table `location`
--
ALTER TABLE `location`
  ADD PRIMARY KEY (`location_id`);

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
  ADD KEY `location_id` (`location_id`);

--
-- Indexes for table `reports_media`
--
ALTER TABLE `reports_media`
  ADD KEY `report_id` (`report_id`);

--
-- Indexes for table `report_activity`
--
ALTER TABLE `report_activity`
  ADD PRIMARY KEY (`activity_id`),
  ADD KEY `account_id` (`account_id`),
  ADD KEY `report_id` (`report_id`);

--
-- Indexes for table `role`
--
ALTER TABLE `role`
  ADD PRIMARY KEY (`role_id`);

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
-- AUTO_INCREMENT for table `access_attempt`
--
ALTER TABLE `access_attempt`
  MODIFY `attempt_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=132;

--
-- AUTO_INCREMENT for table `accounts`
--
ALTER TABLE `accounts`
  MODIFY `account_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `address`
--
ALTER TABLE `address`
  MODIFY `address_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `announcements`
--
ALTER TABLE `announcements`
  MODIFY `ann_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `contacts`
--
ALTER TABLE `contacts`
  MODIFY `contact_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `credentials`
--
ALTER TABLE `credentials`
  MODIFY `cred_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT for table `location`
--
ALTER TABLE `location`
  MODIFY `location_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `password`
--
ALTER TABLE `password`
  MODIFY `pass_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `registration`
--
ALTER TABLE `registration`
  MODIFY `registration_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `reports`
--
ALTER TABLE `reports`
  MODIFY `report_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `report_activity`
--
ALTER TABLE `report_activity`
  MODIFY `activity_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `role`
--
ALTER TABLE `role`
  MODIFY `role_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `usercreds`
--
ALTER TABLE `usercreds`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `access_attempt`
--
ALTER TABLE `access_attempt`
  ADD CONSTRAINT `access_attempt_ibfk_1` FOREIGN KEY (`cred_id`) REFERENCES `credentials` (`cred_id`);

--
-- Constraints for table `accounts`
--
ALTER TABLE `accounts`
  ADD CONSTRAINT `accounts_ibfk_1` FOREIGN KEY (`contact_id`) REFERENCES `contacts` (`contact_id`),
  ADD CONSTRAINT `accounts_ibfk_2` FOREIGN KEY (`address_id`) REFERENCES `address` (`address_id`);

--
-- Constraints for table `activity_media`
--
ALTER TABLE `activity_media`
  ADD CONSTRAINT `activity_media_ibfk_1` FOREIGN KEY (`activity_id`) REFERENCES `report_activity` (`activity_id`);

--
-- Constraints for table `announcements`
--
ALTER TABLE `announcements`
  ADD CONSTRAINT `announcements_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`);

--
-- Constraints for table `credentials`
--
ALTER TABLE `credentials`
  ADD CONSTRAINT `credentials_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `usercreds` (`user_id`),
  ADD CONSTRAINT `credentials_ibfk_2` FOREIGN KEY (`pass_id`) REFERENCES `password` (`pass_id`);

--
-- Constraints for table `reports`
--
ALTER TABLE `reports`
  ADD CONSTRAINT `reports_ibfk_1` FOREIGN KEY (`location_id`) REFERENCES `location` (`location_id`);

--
-- Constraints for table `reports_media`
--
ALTER TABLE `reports_media`
  ADD CONSTRAINT `reports_media_ibfk_1` FOREIGN KEY (`report_id`) REFERENCES `reports` (`report_id`);

--
-- Constraints for table `report_activity`
--
ALTER TABLE `report_activity`
  ADD CONSTRAINT `report_activity_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`),
  ADD CONSTRAINT `report_activity_ibfk_2` FOREIGN KEY (`report_id`) REFERENCES `reports` (`report_id`);

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
