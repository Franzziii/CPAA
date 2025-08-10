-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 16, 2025 at 10:49 AM
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
-- Database: `crime_prevention_app`
--

-- --------------------------------------------------------

--
-- Table structure for table `crime_reports`
--

CREATE TABLE `crime_reports` (
  `id` int(11) NOT NULL,
  `victim_name` varchar(255) NOT NULL,
  `suspect_name` varchar(255) NOT NULL,
  `incident` text NOT NULL,
  `incident_type` varchar(255) NOT NULL,
  `report_date` date NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `crime_reports`
--

INSERT INTO `crime_reports` (`id`, `victim_name`, `suspect_name`, `incident`, `incident_type`, `report_date`, `user_id`) VALUES
(11, 'Laylako', 'Aldous', 'Layla discovered unauthorized transactions on her account. Further investigation revealed Aldous had been using stolen card details for online purchases.', 'Theft', '2025-03-11', 14),
(12, 'Kagura', 'Hanzo', 'Kagura\'s personal details were used to open multiple bank accounts. Authorities traced the fraudulent activities back to Hanzo.', 'fraud', '2025-03-11', 14),
(13, 'Granger', 'Thamuz', 'Granger was fatally shot after intruders broke into his home. Evidence linked Thamuz to the crime through fingerprints on a weapon left behind.', 'Murder', '2025-03-11', 14),
(14, 'Gusion', 'Khufra', 'Gusion was struck by a speeding vehicle while crossing the road. Witnesses saw Khufra fleeing the scene in his heavily damaged car.', 'Vehicular Accident', '2025-03-11', 14),
(15, 'Diggie', 'Johnson', 'Diggie\'s car was stolen from a parking lot. Witnesses reported seeing Johnson speeding away in the stolen vehicle.', 'theft', '2025-03-11', 14),
(16, 'Erithel', 'Gord', 'Irithel was found dead in her apartment under suspicious circumstances. Gord, a suspect with a history of violence, remains under investigation.', 'Murder', '2025-03-11', 14),
(17, 'Guinevere', 'Zhask', 'Guinevere was deceived into sending money to someone she met online. Later, she discovered Zhask had been impersonating another person.', 'fraud', '2025-03-11', 14),
(18, 'Minsitthar', 'Gloo', 'Minsitthar was hospitalized after a severe beating. His partner, Gloo, was arrested for domestic violence.', 'other', '2025-03-11', 14),
(19, 'Selena', 'Cyclops', 'Selena crashed her car into a barricade while being chased by police. Cyclops, who was in the passenger seat, fled the scene.', 'Vehicular Accident', '2025-03-11', 14),
(20, 'Hylos', 'XBorg', 'Hylos was brutally attacked with a crowbar in a parking lot. Security cameras caught X.Borg wielding the weapon.', 'other', '2025-03-11', 14),
(22, 'Beatrix', 'KImmy', 'Beatrix applied for a loan but later discovered a fake account was created in her name. Investigation pointed to Kimmy as the mastermind.', 'fraud', '2025-03-11', 14),
(24, 'HAnz', 'Agii', 'nag rape', 'Rape', '2025-03-12', 14),
(25, 'ANAa', 'Lisaa', 'dnandandadf', 'Rape', '2025-03-05', 14),
(27, 'hahaha', 'huhuhu', 'hehehe', 'other', '2025-03-15', 14),
(28, 'franz', 'flores', 'afdafaf', 'other', '2025-03-16', 14);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `fname` varchar(100) DEFAULT NULL,
  `lname` varchar(100) DEFAULT NULL,
  `phone_num` varchar(15) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `birthday` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `fname`, `lname`, `phone_num`, `age`, `email`, `password`, `birthday`) VALUES
(14, 'Franz Lynel', 'Flores', '09631519038', 21, 'franzlynelfloress@gmail.com', 'scrypt:32768:8:1$dp3iuxG6iiMv6hKk$a3a9a353511c8b66ee56e5e1914adf6acb4261c22ea068d44bd5166f450538327c7621669fb14cc3486f256e80bfc3628d254c90f068a3afdd1a45f63ec5250a', '2003-10-05'),
(15, 'Hanz', 'Alido', '09625221739', 21, 'hafr.alido.ui@phinmaed.com', 'scrypt:32768:8:1$L1KagBlH79Y2AFnP$8c608a74a7581f25c8d436b7094f16e138438ada3c1f93af8fb0975ef631b9f6360239e4e98ec162cc661753525d1e0592e540d755b26b626da7155e9f29c880', '2002-08-31'),
(16, 'Alexymar', 'Tayongtong', '09485160656', 21, 'alec.tayongtong.ui@phinmaed.com', 'scrypt:32768:8:1$uraH8NO6kVwk89HC$d51e040cc417810cf123e5a6eb14d2bc255331edc54bfc0ae9a0636854d2e63e9db3b2341541a3e096ca2288d179cc3dc5c1de5d49233df3fb74a736a9f6ef51', '2004-01-16');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `crime_reports`
--
ALTER TABLE `crime_reports`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `crime_reports`
--
ALTER TABLE `crime_reports`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `crime_reports`
--
ALTER TABLE `crime_reports`
  ADD CONSTRAINT `crime_reports_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
