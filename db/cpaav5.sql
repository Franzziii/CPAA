-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 08, 2025 at 03:34 PM
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
-- Database: `cpaav5`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `last_login` datetime DEFAULT NULL,
  `is_superadmin` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`id`, `username`, `password`, `full_name`, `email`, `created_at`, `last_login`, `is_superadmin`) VALUES
(1, 'Admin', 'pbkdf2:sha256:260000$zngDdhBEcItbTsMZ$fd929f3431bfe1f013e4dfcc99521eeb673deeeae13df92f7f7867d90865dc61', 'Administrator', 'franzlynel508@gmail.com', '2025-04-27 22:25:09', '2025-05-30 12:20:35', 1),
(2, 'Bitas Admin', 'scrypt:32768:8:1$Jid8KkVBthUiFQLT$ac96ca467478718bbeaf5f14efaab1c08d8767f5f05ac3d8a3e9907e767a6fa9f9fc2898d011f4dffc7acd4bcdadf5526140eb0d34db1c4ac6a063ea8ebe2004', 'Brgy. Bitas Admin', 'franzlynel318@gmail.com', '2025-05-06 13:28:03', '2025-05-29 22:18:21', 0),
(3, 'Bagumbayan Admin', 'scrypt:32768:8:1$HMwzosYlVtBgamGu$a71ea828ee7390664a7be782ab5a12b2dd22a928703721b791bac8d3a85da433658cf1420d986005554ede686360d09d88173dbebf551d38f1afa66354a5f42e', 'Brgy. Bagumbayan Admin', 'franz1005@gmail.com', '2025-05-06 14:39:04', '2025-05-06 14:39:49', 0);

-- --------------------------------------------------------

--
-- Table structure for table `admin_logs`
--

CREATE TABLE `admin_logs` (
  `id` int(11) NOT NULL,
  `admin_id` int(11) DEFAULT NULL,
  `action` varchar(255) NOT NULL,
  `details` text DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin_logs`
--

INSERT INTO `admin_logs` (`id`, `admin_id`, `action`, `details`, `ip_address`, `user_agent`, `created_at`) VALUES
(1, 1, 'Admin Login', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 135.0.0', '2025-04-27 23:17:57'),
(2, 1, 'Admin Logout', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 135.0.0', '2025-04-27 23:20:46'),
(3, 1, 'Admin Login', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 135.0.0', '2025-04-27 23:22:03'),
(4, 1, 'Admin Login', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 135.0.0', '2025-04-28 09:01:23'),
(5, 1, 'Update Report Status', '{\"report_id\": 1, \"status\": \"Under Investigation\", \"feedback\": \"etwtwtwetwt\"}', '127.0.0.1', 'PC / Windows 10 / Chrome 135.0.0', '2025-04-28 09:46:48'),
(6, 1, 'Admin Logout', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 135.0.0', '2025-04-28 10:35:22'),
(7, 1, 'Admin Login', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 135.0.0', '2025-04-28 10:38:11'),
(8, 1, 'Update Report Status', '{\"report_id\": 2, \"status\": \"Resolved\", \"feedback\": \"afaff\"}', '127.0.0.1', 'PC / Windows 10 / Chrome 135.0.0', '2025-04-28 11:07:56'),
(9, 1, 'Admin Login', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 135.0.0', '2025-04-28 11:47:08'),
(10, 1, 'Update Report Status', '{\"report_id\": 1, \"status\": \"Resolved\", \"feedback\": \"etwtwtwetwtrraw\"}', '127.0.0.1', 'PC / Windows 10 / Chrome 135.0.0', '2025-04-28 11:51:26'),
(11, 1, 'Admin Login', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-05 21:54:33'),
(12, 1, 'Update Report Status', '{\"report_id\": 3, \"status\": \"Resolved\", \"feedback\": \"ok\"}', '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-05 21:56:35'),
(13, 1, 'Block User', '{\"user_id\": 2, \"reason\": \"Hacker\"}', '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-05 22:14:25'),
(14, 1, 'Unblock User', '{\"user_id\": 2}', '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-05 23:46:46'),
(15, 1, 'Block User', '{\"user_id\": 2, \"reason\": \"HACKER\"}', '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-05 23:47:05'),
(16, 1, 'Admin Login', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-06 11:28:21'),
(17, 1, 'Update Report Status', '{\"report_id\": 5, \"status\": \"Under Investigation\", \"feedback\": \"We investigate that to confirm thankyou for reporting\"}', '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-06 11:29:19'),
(18, 1, 'Unblock User', '{\"user_id\": 2}', '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-06 11:29:59'),
(19, 1, 'Admin Logout', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-06 11:31:14'),
(20, 1, 'Admin Login', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-06 11:31:30'),
(21, 1, 'Admin Login', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-06 11:35:55'),
(22, 1, 'Update Report Status', '{\"report_id\": 1, \"status\": \"Rejected\", \"feedback\": \"this report is not valid\"}', '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-06 11:42:45'),
(23, 1, 'Admin Login', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-06 13:24:54'),
(24, 1, 'Create Admin', '{\"username\": \"Bitas Admin\", \"email\": \"franzlynel318@gmail.com\", \"is_superadmin\": false}', '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-06 13:28:03'),
(25, 1, 'Admin Logout', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-06 13:28:15'),
(26, 2, 'Admin Login', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-06 13:28:26'),
(27, 2, 'Admin Logout', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-06 13:46:59'),
(28, 1, 'Admin Login', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-06 13:53:44'),
(29, 1, 'Block User', '{\"user_id\": 2, \"reason\": \"\"}', '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-06 13:54:06'),
(30, 1, 'Unblock User', '{\"user_id\": 2}', '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-06 13:54:56'),
(31, 1, 'Admin Logout', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-06 14:34:03'),
(32, 1, 'Admin Login', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-06 14:34:13'),
(33, 1, 'Admin Logout', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-06 14:35:25'),
(34, 1, 'Admin Login', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-06 14:35:39'),
(35, 1, 'Create Admin', '{\"username\": \"Bagumbayan Admin\", \"email\": \"franz1005@gmail.com\", \"is_superadmin\": false}', '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-06 14:39:04'),
(36, 1, 'Admin Logout', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-06 14:39:11'),
(37, 3, 'Admin Login', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-06 14:39:49'),
(38, 3, 'Admin Logout', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-06 14:40:26'),
(39, 1, 'Admin Login', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-06 14:40:35'),
(40, 1, 'Block User', '{\"user_id\": 2, \"reason\": \"\"}', '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-06 17:05:29'),
(41, 1, 'Admin Login', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-20 18:55:43'),
(42, 1, 'Admin Logout', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-20 18:57:14'),
(43, 1, 'Admin Login', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-20 20:08:48'),
(44, 1, 'Admin Logout', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-20 20:19:25'),
(45, 1, 'Admin Login', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-20 20:19:38'),
(46, 1, 'Admin Logout', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-20 20:20:05'),
(47, 1, 'Admin Login', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-20 20:55:42'),
(48, 1, 'Admin Login', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-29 22:02:21'),
(49, 1, 'Update Report Status', '{\"report_id\": 5, \"status\": \"Resolved\", \"feedback\": \"We investigate that to confirm thankyou for reporting\"}', '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-29 22:05:46'),
(50, 1, 'Update Report Status', '{\"report_id\": 5, \"status\": \"Under Investigation\", \"feedback\": \"We investigate that to confirm thankyou for reporting\"}', '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-29 22:07:16'),
(51, 1, 'Unblock User', '{\"user_id\": 2}', '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-29 22:14:48'),
(52, 1, 'Admin Logout', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-29 22:16:52'),
(53, 1, 'Admin Login', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-29 22:17:51'),
(54, 1, 'Admin Logout', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-29 22:18:03'),
(55, 2, 'Admin Login', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-29 22:18:21'),
(56, 2, 'Admin Logout', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-29 22:19:16'),
(57, 1, 'Admin Login', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-29 22:19:38'),
(58, 1, 'Admin Login', NULL, '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-30 12:20:35'),
(59, 1, 'Block User', '{\"user_id\": 2, \"reason\": \"\"}', '127.0.0.1', 'PC / Windows 10 / Chrome 136.0.0', '2025-05-30 12:23:27');

-- --------------------------------------------------------

--
-- Table structure for table `blocked_users`
--

CREATE TABLE `blocked_users` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `admin_id` int(11) NOT NULL,
  `reason` text DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `blocked_users`
--

INSERT INTO `blocked_users` (`id`, `user_id`, `admin_id`, `reason`, `created_at`) VALUES
(5, 2, 1, '', '2025-05-30 12:23:27');

-- --------------------------------------------------------

--
-- Table structure for table `crime_reports`
--

CREATE TABLE `crime_reports` (
  `id` int(11) NOT NULL,
  `complainant_name` varchar(100) NOT NULL,
  `victim_name` varchar(100) DEFAULT NULL,
  `suspect_name` varchar(100) DEFAULT NULL,
  `concern` text DEFAULT NULL,
  `incident` text DEFAULT NULL,
  `incident_type` enum('Theft','Rape','Vehicular Accident','Murder','Fraud','Other') NOT NULL,
  `location` varchar(255) NOT NULL,
  `latitude` decimal(10,8) DEFAULT NULL,
  `longitude` decimal(11,8) DEFAULT NULL,
  `report_date` date NOT NULL,
  `status` enum('Pending','Under Investigation','Resolved','Rejected') DEFAULT 'Pending',
  `user_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `admin_feedback` text DEFAULT NULL,
  `admin_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `crime_reports`
--

INSERT INTO `crime_reports` (`id`, `complainant_name`, `victim_name`, `suspect_name`, `concern`, `incident`, `incident_type`, `location`, `latitude`, `longitude`, `report_date`, `status`, `user_id`, `created_at`, `updated_at`, `admin_feedback`, `admin_id`) VALUES
(1, 'Franz Lynel Flores', NULL, NULL, 'nadjabhdjagbaihdsdgvhiasydgvasyidfaysdufausydfka', NULL, 'Vehicular Accident', 'Pajo, Iloilo, Western Visayas, Philippines', 10.86904707, 122.38989254, '2025-04-26', 'Rejected', 1, '2025-04-26 12:03:32', '2025-05-06 03:42:45', 'this report is not valid', 1),
(2, 'Franz Lynel Flores', NULL, NULL, 'dad afdasfasfasfasf', NULL, 'Rape', 'Narfaith Place, La Paz, Ingore, Iloilo City, Western Visayas, 5000, Philippines', 10.71131872, 122.58623886, '2025-04-28', 'Resolved', 2, '2025-04-28 02:26:35', '2025-04-28 03:07:56', 'afaff', 1),
(3, 'Franz Lynel Flores', NULL, NULL, 'car accedent in tigabuan', NULL, 'Vehicular Accident', 'Tigbauan Gym, Taldelore Street, Poblacion, Barangay 3, Tigbauan, Iloilo, Western Visayas, 5021, Philippines', 10.67449259, 122.37579918, '2025-04-28', 'Resolved', 2, '2025-04-28 03:49:54', '2025-05-05 13:56:35', 'ok', 1),
(4, 'Franz Lynel Flores', NULL, NULL, 'i see people planning to kill someone in plaza tigbauan', NULL, 'Other', 'Tigbauan Gym, Taldelore Street, Poblacion, Barangay 3, Tigbauan, Iloilo, Western Visayas, 5021, Philippines', 10.67442799, 122.37607867, '2025-05-05', 'Pending', 1, '2025-05-05 14:52:16', '2025-05-05 14:52:16', NULL, NULL),
(5, 'Franz Lynel Flores', NULL, NULL, 'ojdnaijbfdbadbasd', NULL, 'Rape', 'Sum-ag, Bacolod-2, Bacolod, Negros Island Region, Philippines', 10.59717120, 122.93570560, '2025-05-05', 'Under Investigation', 1, '2025-05-05 14:53:18', '2025-05-29 14:07:16', 'We investigate that to confirm thankyou for reporting', 1),
(6, 'Franz Lynel Flores', NULL, NULL, 'drugss in a plaza', NULL, 'Other', 'Luna Street, Remon Ville, Desamparados, Jaro, Calubihan, Iloilo City, Western Visayas, 5000, Philippines', 10.72403486, 122.55766958, '2025-05-06', 'Pending', 1, '2025-05-06 09:00:18', '2025-05-06 09:00:18', NULL, NULL),
(7, 'Franz Lynel Flores', NULL, NULL, 'motorcycle collision in front of  tigbauan plaza ', NULL, 'Vehicular Accident', 'Taldelore Street, Poblacion, Barangay 3, Tigbauan, Iloilo, Western Visayas, 5021, Philippines', 10.67460722, 122.37642199, '2025-05-06', 'Pending', 1, '2025-05-06 09:10:13', '2025-05-06 09:10:13', NULL, NULL),
(8, 'Franz Lynel Flores', NULL, NULL, 'Gin sakit ni alexymar sapat sa balay nila kay tamad', NULL, 'Murder', 'Aleosan-Alimodian Road, Santa Clara, Alimodian, Iloilo, Western Visayas, 5020, Philippines', 10.78571164, 122.43086815, '2025-05-29', 'Pending', 1, '2025-05-29 13:59:14', '2025-05-29 13:59:14', NULL, NULL),
(11, 'Franz Lynel Flores', NULL, NULL, 'dafafafafa', NULL, '', 'Tigbauan National High School, Tupan Street, Poblacion, Barangay 3, Tigbauan, Iloilo, Western Visayas, 5021, Philippines', 10.67822379, 122.38282013, '2025-08-08', 'Pending', 1, '2025-08-08 13:33:01', '2025-08-08 13:33:01', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `system_settings`
--

CREATE TABLE `system_settings` (
  `id` int(11) NOT NULL,
  `setting_name` varchar(255) NOT NULL,
  `setting_value` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `system_settings`
--

INSERT INTO `system_settings` (`id`, `setting_name`, `setting_value`, `created_at`, `updated_at`) VALUES
(1, 'maintenance_mode', '0', '2025-08-08 12:46:19', '2025-08-08 12:46:19');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `fname` varchar(50) NOT NULL,
  `lname` varchar(50) NOT NULL,
  `phone_num` varchar(15) NOT NULL,
  `age` int(11) NOT NULL,
  `birthday` date NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `fname`, `lname`, `phone_num`, `age`, `birthday`, `email`, `password`, `created_at`) VALUES
(1, 'Franz Lynel', 'Flores', '09631519038', 21, '2003-10-05', 'franzlynelfloress@gmail.com', 'pbkdf2:sha256:260000$jwGAcISSjhUlDfRl$a8cd608813d517c56593122ed907d2b58699a80447fd739258293a58dcd7b8bc', '2025-04-26 12:01:53'),
(2, 'Franz Lynel', 'Flores', '09098088887', 21, '2025-04-28', 'franzlynel508@gmail.com', 'pbkdf2:sha256:260000$6jPNlQafbhyv3cco$3c9056279c53c71eba6c473d58444aa5f504143ecd3e789ede33a20dbe386434', '2025-04-28 01:57:43');

-- --------------------------------------------------------

--
-- Table structure for table `user_logs`
--

CREATE TABLE `user_logs` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `action` varchar(255) NOT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_logs`
--

INSERT INTO `user_logs` (`id`, `user_id`, `action`, `ip_address`, `user_agent`, `location`, `created_at`) VALUES
(1, 1, 'User Login', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'Localhost', '2025-05-05 22:04:05'),
(2, NULL, 'System Maintenance', '127.0.0.1', 'Python/3.9', 'Server', '2025-05-05 22:04:05'),
(3, 1, 'User Login', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'Localhost', '2025-05-05 22:09:46'),
(4, 1, 'User Login', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'Localhost', '2025-05-05 22:13:06'),
(5, 2, 'User Login', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'Localhost', '2025-05-05 22:13:06'),
(6, 2, 'User Login', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'Localhost', '2025-05-05 22:13:59'),
(7, 1, 'User Login', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', NULL, '2025-05-05 22:49:20'),
(8, NULL, 'Failed Login Attempt', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', NULL, '2025-05-05 22:54:33'),
(9, NULL, 'Failed Login Attempt', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', NULL, '2025-05-05 23:59:10'),
(10, NULL, 'Failed Login Attempt', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', NULL, '2025-05-05 23:59:35'),
(11, 1, 'User Login', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', NULL, '2025-05-06 11:27:12'),
(12, 1, 'User Login', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', NULL, '2025-05-06 13:19:30'),
(13, NULL, 'Failed Login Attempt', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', NULL, '2025-05-20 18:43:12'),
(14, 1, 'Failed Login Attempt', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', NULL, '2025-05-20 18:43:26'),
(15, 1, 'Failed Login Attempt', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', NULL, '2025-05-20 18:43:52'),
(16, 1, 'Failed Login Attempt', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', NULL, '2025-05-20 18:44:08'),
(17, 1, 'Failed Login Attempt', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', NULL, '2025-05-20 18:44:30'),
(18, 1, 'User Login', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', NULL, '2025-05-20 18:44:58'),
(19, 1, 'User Login', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', NULL, '2025-05-29 21:54:01'),
(20, 2, 'User Login', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', NULL, '2025-05-29 22:15:20'),
(21, 1, 'Failed Login Attempt', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', NULL, '2025-05-30 12:13:12'),
(22, 1, 'Failed Login Attempt', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', NULL, '2025-05-30 12:13:36'),
(23, NULL, 'Failed Login Attempt', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', NULL, '2025-05-30 12:13:55'),
(24, 1, 'User Login', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', NULL, '2025-05-30 12:14:31'),
(25, NULL, 'Failed Login Attempt', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36', NULL, '2025-08-08 21:03:14'),
(26, 1, 'Failed Login Attempt', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36', NULL, '2025-08-08 21:05:22'),
(27, 1, 'Failed Login Attempt', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36', NULL, '2025-08-08 21:05:48'),
(28, 1, 'Failed Login Attempt', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36', NULL, '2025-08-08 21:17:42'),
(29, 1, 'Failed Login Attempt', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36', NULL, '2025-08-08 21:18:03'),
(30, 1, 'User Login', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36', NULL, '2025-08-08 21:19:32');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `admin_logs`
--
ALTER TABLE `admin_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `admin_id` (`admin_id`);

--
-- Indexes for table `blocked_users`
--
ALTER TABLE `blocked_users`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `admin_id` (`admin_id`);

--
-- Indexes for table `crime_reports`
--
ALTER TABLE `crime_reports`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_crime_reports_user` (`user_id`),
  ADD KEY `idx_crime_reports_status` (`status`),
  ADD KEY `idx_crime_reports_type` (`incident_type`),
  ADD KEY `idx_crime_reports_date` (`report_date`),
  ADD KEY `admin_id` (`admin_id`);

--
-- Indexes for table `system_settings`
--
ALTER TABLE `system_settings`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `setting_name` (`setting_name`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `user_logs`
--
ALTER TABLE `user_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `admin_logs`
--
ALTER TABLE `admin_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=60;

--
-- AUTO_INCREMENT for table `blocked_users`
--
ALTER TABLE `blocked_users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `crime_reports`
--
ALTER TABLE `crime_reports`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `system_settings`
--
ALTER TABLE `system_settings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `user_logs`
--
ALTER TABLE `user_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `admin_logs`
--
ALTER TABLE `admin_logs`
  ADD CONSTRAINT `admin_logs_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admins` (`id`);

--
-- Constraints for table `blocked_users`
--
ALTER TABLE `blocked_users`
  ADD CONSTRAINT `blocked_users_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `blocked_users_ibfk_2` FOREIGN KEY (`admin_id`) REFERENCES `admins` (`id`);

--
-- Constraints for table `crime_reports`
--
ALTER TABLE `crime_reports`
  ADD CONSTRAINT `crime_reports_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `crime_reports_ibfk_2` FOREIGN KEY (`admin_id`) REFERENCES `admins` (`id`),
  ADD CONSTRAINT `crime_reports_ibfk_3` FOREIGN KEY (`admin_id`) REFERENCES `admins` (`id`);

--
-- Constraints for table `user_logs`
--
ALTER TABLE `user_logs`
  ADD CONSTRAINT `user_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
