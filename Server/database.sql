DROP DATABASE IF EXISTS `automatic_drying_rack`;
CREATE DATABASE `automatic_drying_rack`;
USE `automatic_drying_rack`;

CREATE TABLE `manager` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255),
  `username` varchar(50),
  `password` varchar(255),
  `created_at` timestamp
);

CREATE TABLE `accessories` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255)
);

CREATE TABLE `status` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255)
);

CREATE TABLE `history` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `accessories_id` int,
  `status_id` int,
  `manager_id` int,
  `setting_id` int,
  `description` varchar(255),
  `created_at` timestamp
);

CREATE TABLE `setting` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255),
  `data` varchar(500) DEFAULT "" COMMENT 'json data'
);

CREATE TABLE `current_status` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `open` int DEFAULT 0,
  `sunny` int DEFAULT 0,
  `raining` int DEFAULT 0
);

ALTER TABLE `history` ADD FOREIGN KEY (`accessories_id`) REFERENCES `accessories` (`id`);

ALTER TABLE `history` ADD FOREIGN KEY (`status_id`) REFERENCES `status` (`id`);

ALTER TABLE `history` ADD FOREIGN KEY (`manager_id`) REFERENCES `manager` (`id`);

ALTER TABLE `history` ADD FOREIGN KEY (`setting_id`) REFERENCES `setting` (`id`);

INSERT INTO `manager` (`name`, `username`, `password`, `created_at`) VALUES 
    ('Hệ thống', 'admin', '21232f297a57a5a743894a0e4a801fc3', NOW()),
    ('Hoàng Khắc Phúc', 'hoangkhacphuc', 'e10adc3949ba59abbe56e057f20f883e', NOW()),
    ('Nguyễn Đức Duy', 'nguyenducduy', 'e10adc3949ba59abbe56e057f20f883e', NOW()),
    ('Đường Ngọc Hà', 'duongngocha', 'e10adc3949ba59abbe56e057f20f883e', NOW());

INSERT INTO `accessories` (`name`) VALUES 
    ('Cảm biến mưa'),
    ('Cảm biến ánh sáng'),
    ('Motor'),
    ('Thời gian');

INSERT INTO `status` (`name`) VALUES 
    ('Đang hoạt động'),
    ('Đang tắt'),
    ('Đang bật'),
    ('Đang mở'),
    ('Đang đóng'),
    ('Đang mưa'),
    ('Đang nắng'),
    ('Trời nắng'),
    ('Trời tối');

INSERT INTO `setting` (`name`, `data`) VALUES 
    ('Thời gian mở', '{"open": "07:00:00"}'),
    ('Thời gian đóng', '{"close": "19:00:00"}');

INSERT INTO `current_status` (`open`, `sunny`, `raining`) VALUES 
    (1, 1, 0);