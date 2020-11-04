CREATE TABLE `authors` (
  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(64) NOT NULL
) DEFAULT CHARSET=utf8;
CREATE TABLE `books` (
  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `barcode` varchar(64) DEFAULT NULL,
  `name` varchar(64) NOT NULL,
  `authorId` int(11) NOT NULL,
  `typeId` int(11) NOT NULL,
  `class` varchar(64) DEFAULT NULL
) DEFAULT CHARSET=utf8;
CREATE TABLE `book_types` (
  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(64) NOT NULL
);
CREATE TABLE `issues` (
  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `bookId` int(11) NOT NULL,
  `userId` int(11) NOT NULL,
  `issueDate` varchar(64) NOT NULL,
  `returnDate` varchar(64) DEFAULT NULL,
  `issueStatusId` int(11) NOT NULL
) DEFAULT CHARSET=utf8;
CREATE TABLE `issue_types` (
  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(64) NOT NULL
) DEFAULT CHARSET=utf8;
CREATE TABLE `users` (
  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `surname` varchar(64) NOT NULL,
  `patronymic` varchar(64) NOT NULL,
  `studentCardId` varchar(64) NOT NULL,
  `vkId` varchar(64) NOT NULL
) DEFAULT CHARSET=utf8;