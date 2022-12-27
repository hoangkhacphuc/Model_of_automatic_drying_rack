SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

DROP DATABASE IF EXISTS `automatic_drying_rack`;
CREATE DATABASE IF NOT EXISTS `automatic_drying_rack` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `automatic_drying_rack`;

CREATE TABLE IF NOT EXISTS `accessories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

INSERT INTO `accessories` (`id`, `name`) VALUES
(1, 'Cảm biến mưa'),
(2, 'Cảm biến ánh sáng'),
(3, 'Motor'),
(4, 'Thời gian');

CREATE TABLE IF NOT EXISTS `current_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `open` int(11) DEFAULT 0,
  `sunny` int(11) DEFAULT 0,
  `raining` int(11) DEFAULT 0,
  `turn_off` int(11) DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

INSERT INTO `current_status` (`id`, `open`, `sunny`, `raining`, `turn_off`) VALUES
(1, 1, 1, 0, 0);

CREATE TABLE IF NOT EXISTS `history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `accessories_id` int(11) DEFAULT NULL,
  `status_id` int(11) DEFAULT NULL,
  `manager_id` int(11) DEFAULT NULL,
  `setting_id` int(11) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `accessories_id` (`accessories_id`),
  KEY `status_id` (`status_id`),
  KEY `manager_id` (`manager_id`),
  KEY `setting_id` (`setting_id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4;

INSERT INTO `history` (`id`, `accessories_id`, `status_id`, `manager_id`, `setting_id`, `description`, `created_at`) VALUES
(21, 1, 6, 1, NULL, 'Trời mưa thu quần áo', '2022-12-27 00:24:51'),
(22, 2, 7, 1, NULL, 'Trời nắng phơi quần áo', '2022-12-27 00:24:52'),
(23, 4, 9, 1, NULL, 'Tới thời gian thu quần áo', '2022-12-27 00:24:53'),
(24, 4, 8, 1, NULL, 'Tới thời gian phơi quần áo', '2022-12-27 00:24:54'),
(25, 1, 6, 1, NULL, 'Trời mưa thu quần áo', '2022-12-27 00:24:55'),
(26, 1, 6, 1, NULL, 'Trời mưa thu quần áo', '2022-12-27 00:24:56'),
(27, 2, 7, 1, NULL, 'Trời nắng phơi quần áo', '2022-12-27 00:24:57'),
(28, 4, 9, 1, NULL, 'Tới thời gian thu quần áo', '2022-12-27 00:24:58'),
(29, 4, 8, 1, NULL, 'Tới thời gian phơi quần áo', '2022-12-27 00:24:59'),
(30, 1, 6, 1, NULL, 'Trời mưa thu quần áo', '2022-12-27 00:25:00'),
(31, NULL, 7, NULL, NULL, 'Cập nhật cài đặt', '2022-12-27 02:34:32'),
(32, NULL, 7, NULL, NULL, 'Cập nhật cài đặt', '2022-12-27 02:37:53'),
(33, NULL, 7, NULL, NULL, 'Cập nhật cài đặt', '2022-12-27 02:46:15'),
(34, NULL, 7, NULL, NULL, 'Cập nhật cài đặt', '2022-12-27 02:56:02'),
(35, NULL, 7, NULL, NULL, 'Cập nhật cài đặt', '2022-12-27 03:11:41'),
(36, NULL, 7, NULL, NULL, 'Cập nhật cài đặt', '2022-12-27 03:11:56'),
(37, NULL, 7, NULL, NULL, 'Cập nhật cài đặt', '2022-12-27 03:12:27'),
(38, NULL, 7, NULL, NULL, 'Cập nhật cài đặt', '2022-12-27 03:21:58'),
(39, NULL, 2, NULL, NULL, 'Thu đồ thủ công', '2022-12-27 03:22:15'),
(40, NULL, 4, NULL, NULL, 'Phơi đồ thủ công', '2022-12-27 03:22:29'),
(41, NULL, 2, NULL, NULL, 'Thu đồ thủ công', '2022-12-27 03:23:10'),
(42, NULL, 4, NULL, NULL, 'Phơi đồ thủ công', '2022-12-27 03:23:13'),
(43, NULL, 2, NULL, NULL, 'Thu đồ thủ công', '2022-12-27 03:26:56'),
(44, NULL, 4, NULL, NULL, 'Phơi đồ thủ công', '2022-12-27 03:26:58');

CREATE TABLE IF NOT EXISTS `manager` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

INSERT INTO `manager` (`id`, `name`, `username`, `password`, `created_at`) VALUES
(1, 'Hệ thống', 'admin', '21232f297a57a5a743894a0e4a801fc3', '2022-12-26 18:44:19'),
(2, 'Hoàng Khắc Phúc', 'hoangkhacphuc', 'e10adc3949ba59abbe56e057f20f883e', '2022-12-26 18:44:19'),
(3, 'Nguyễn Đức Duy', 'nguyenducduy', 'e10adc3949ba59abbe56e057f20f883e', '2022-12-26 18:44:19'),
(4, 'Đường Ngọc Hà', 'duongngocha', 'e10adc3949ba59abbe56e057f20f883e', '2022-12-26 18:44:19');

CREATE TABLE IF NOT EXISTS `setting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `data` varchar(500) DEFAULT '' COMMENT 'json data',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

INSERT INTO `setting` (`id`, `name`, `data`) VALUES
(1, 'Thời gian mở', '{\"open\":\"02:00\"}'),
(2, 'Thời gian đóng', '{\"close\":\"19:00:00\"}');

CREATE TABLE IF NOT EXISTS `status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4;

INSERT INTO `status` (`id`, `name`) VALUES
(1, 'Đang hoạt động'),
(2, 'Đang tắt'),
(3, 'Đang bật'),
(4, 'Đang mở'),
(5, 'Đang đóng'),
(6, 'Đang mưa'),
(7, 'Đang nắng'),
(8, 'Trời nắng'),
(9, 'Trời tối');


ALTER TABLE `history`
  ADD CONSTRAINT `history_ibfk_1` FOREIGN KEY (`accessories_id`) REFERENCES `accessories` (`id`),
  ADD CONSTRAINT `history_ibfk_2` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`),
  ADD CONSTRAINT `history_ibfk_3` FOREIGN KEY (`manager_id`) REFERENCES `manager` (`id`),
  ADD CONSTRAINT `history_ibfk_4` FOREIGN KEY (`setting_id`) REFERENCES `setting` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
