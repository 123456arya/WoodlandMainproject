-- phpMyAdmin SQL Dump
-- version 3.3.9
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 06, 2023 at 09:53 AM
-- Server version: 5.5.8
-- PHP Version: 5.3.5

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `woodland`
--

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE IF NOT EXISTS `cart` (
  `cartID` int(11) NOT NULL AUTO_INCREMENT,
  `ProductID` int(11) NOT NULL,
  `CustomerID` int(11) NOT NULL,
  `count` int(11) NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`cartID`),
  KEY `CustomerID` (`CustomerID`),
  KEY `ProductID` (`ProductID`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=81 ;

--
-- Dumping data for table `cart`
--


-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE IF NOT EXISTS `category` (
  `categoryID` int(11) NOT NULL AUTO_INCREMENT,
  `category` varchar(50) NOT NULL,
  PRIMARY KEY (`categoryID`),
  UNIQUE KEY `category` (`category`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=15 ;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`categoryID`, `category`) VALUES
(7, 'Alamara'),
(5, 'Chair'),
(12, 'cupboard'),
(6, 'Cupbords'),
(1, 'Dress'),
(10, 'Kasera'),
(14, 'small tables'),
(11, 'sofa'),
(4, 'Table'),
(8, 'Teepo');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE IF NOT EXISTS `customer` (
  `CustomerID` int(11) NOT NULL AUTO_INCREMENT,
  `Fname` varchar(50) NOT NULL,
  `Lname` varchar(50) NOT NULL,
  `Housename` varchar(50) NOT NULL,
  `Street` varchar(50) NOT NULL,
  `District` varchar(50) NOT NULL,
  `State` varchar(50) NOT NULL,
  `PinCode` int(11) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `Mobno1` bigint(11) NOT NULL,
  `Mobno2` bigint(11) DEFAULT NULL,
  PRIMARY KEY (`CustomerID`),
  UNIQUE KEY `Email` (`Email`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `password` (`password`),
  UNIQUE KEY `Mobno1` (`Mobno1`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=8 ;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`CustomerID`, `Fname`, `Lname`, `Housename`, `Street`, `District`, `State`, `PinCode`, `Email`, `username`, `password`, `Mobno1`, `Mobno2`) VALUES
(2, 'ramu', 'ram', 'kripa', 'TVR', 'kply', 'Kerala', 682308, 'ramu@gmail.com', 'ramu', 'ramu123', 9978458758, 9887768589),
(4, 'Jyothis', 'K J', 'Jyothis Home', 'Vallikkadu', 'Kottayam', 'Kerala', 686631, 'jyo@gmail.com', 'jyothis', 'Jyothis2', 8590594041, 9847422078),
(7, 'Aleena', 'RajuB', 'Happy Home', 'Kannimala', 'Erumely', 'Kerala', 686631, 'aleena@gmail.com', 'aleena', 'Aleena@33', 9578965411, 9234556782);

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

CREATE TABLE IF NOT EXISTS `employee` (
  `EmpID` int(11) NOT NULL AUTO_INCREMENT,
  `Fname` varchar(20) NOT NULL,
  `Lname` varchar(20) NOT NULL,
  `Housename` varchar(30) NOT NULL,
  `Street` varchar(20) NOT NULL,
  `District` varchar(20) NOT NULL,
  `State` varchar(20) NOT NULL,
  `PinCode` int(11) NOT NULL,
  `Email` varchar(30) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `Salary` int(11) NOT NULL,
  `Designation` varchar(50) NOT NULL,
  `Mob1` bigint(20) NOT NULL,
  `Mob2` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`EmpID`),
  UNIQUE KEY `Email` (`Email`),
  UNIQUE KEY `Mob1` (`Mob1`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `password` (`password`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `employee`
--

INSERT INTO `employee` (`EmpID`, `Fname`, `Lname`, `Housename`, `Street`, `District`, `State`, `PinCode`, `Email`, `username`, `password`, `Salary`, `Designation`, `Mob1`, `Mob2`) VALUES
(2, 'Anamika', 'Arun', 'Anu Home', 'Anny', 'Kochi', 'Kerala', 123456, 'anamika@gmail.com', 'anamika', 'Anamika@21', 15000, 'worker', 9789564123, 9874525555),
(3, 'arya', 'biju', 'aryabome', 'emly', 'ktym', 'kerala', 686509, 'arya@gmail.com', 'arya', 'Arya@123', 80000, 'coordinator', 7412589632, 8547124522);

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE IF NOT EXISTS `login` (
  `loginID` int(11) NOT NULL AUTO_INCREMENT,
  `Username` varchar(20) NOT NULL,
  `Password` varchar(20) NOT NULL,
  `Usertype` varchar(20) NOT NULL,
  PRIMARY KEY (`loginID`),
  UNIQUE KEY `Username` (`Username`),
  UNIQUE KEY `Password` (`Password`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=28 ;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`loginID`, `Username`, `Password`, `Usertype`) VALUES
(1, 'admin@gmail.com', 'admin', 'admin'),
(2, 'ramu', 'ramu123', 'Customer'),
(24, 'aleena', 'Aleena@33', 'Customer'),
(26, 'anamika', 'Anamika@21', 'Employee'),
(27, 'arya', 'Arya@123', 'Employee');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE IF NOT EXISTS `orders` (
  `OrderID` int(11) NOT NULL AUTO_INCREMENT,
  `ProductID` int(11) NOT NULL,
  `CustomerID` int(11) NOT NULL,
  `Status` varchar(20) NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`OrderID`),
  KEY `CustomerID` (`CustomerID`),
  KEY `ProductID` (`ProductID`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=47 ;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`OrderID`, `ProductID`, `CustomerID`, `Status`, `date`) VALUES
(46, 26, 2, 'paid', '2023-02-02');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE IF NOT EXISTS `products` (
  `ProductID` int(11) NOT NULL AUTO_INCREMENT,
  `Pname` varchar(20) NOT NULL,
  `SubcategoryID` int(11) NOT NULL,
  `Price` int(11) NOT NULL,
  `Pricenot` int(11) NOT NULL,
  `Description` varchar(500) NOT NULL,
  `qty` int(11) NOT NULL,
  `image1` varchar(200) NOT NULL,
  `image2` varchar(200) DEFAULT NULL,
  `image3` varchar(200) DEFAULT NULL,
  `image4` varchar(200) DEFAULT NULL,
  `image5` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`ProductID`),
  KEY `SubcategoryID` (`SubcategoryID`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=29 ;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`ProductID`, `Pname`, `SubcategoryID`, `Price`, `Pricenot`, `Description`, `qty`, `image1`, `image2`, `image3`, `image4`, `image5`) VALUES
(26, 'Novo 2 Seater Dining', 11, 15000, 20000, 'Bohemiana is a new range of furniture inspired by the spirit of freedom and adventure. The design philosophy explores the use of a combination of materials, colours, patterns and textures to create unique handcrafted furniture, of the finest quality.', 10, '/media/71ObDm7X9pL._SL1500_.jpg', '/media/a746dc18f299bba6ce17b67a66a910b7.jpg', '/media/a746dc18f299bba6ce17b67a66a910b7_nm59Shb.jpg', '/media/images%20(1).jpeg', '/media/solid-wood-dining-table.jpg'),
(27, 'Antalya 3 Seater Sof', 12, 35000, 40000, 'rban Living is transforming the perception of Indian Craft by offering premium quality furniture at approachable prices. We specialise in developing sofas, loungers and chairs for residential and hospitality marketsContemporary Style Sofas are very current and in trend. I', 20, '/media/cstmrlog_wFnLeto.jpg', '/media/admin_ZLVbuhx.jpg', '/media/blog-6_Rcw4UKj.jpg', '/media/prod3.jpg', '/media/prod1.jpg'),
(28, 'Bladen 2 Seater sofa', 12, 10000, 15000, 'Adorn India, one of the most trusted & respected furniture manufacturer. With decades of experience behind us we surge forward to make our brand a household name & also to be known as the brand with quality & durability as its 2 primary virtues.', 15, '/media/OIP%20(2).jpeg', '/media/OIP%20(3).jpeg', '/media/download.jpeg', '/media/OIP.jpeg', '/media/OIP%20(1).jpeg');

-- --------------------------------------------------------

--
-- Table structure for table `subcategory`
--

CREATE TABLE IF NOT EXISTS `subcategory` (
  `SubID` int(11) NOT NULL AUTO_INCREMENT,
  `categoryID` int(11) NOT NULL,
  `subcategory` varchar(50) NOT NULL,
  PRIMARY KEY (`SubID`),
  KEY `categoryID` (`categoryID`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=14 ;

--
-- Dumping data for table `subcategory`
--

INSERT INTO `subcategory` (`SubID`, `categoryID`, `subcategory`) VALUES
(1, 1, 'round table'),
(5, 12, 'single sofa'),
(6, 12, 'single door cupboard'),
(8, 4, 'single chair'),
(9, 12, 'corner sofa'),
(10, 10, 'small teepo'),
(11, 14, 'round shape'),
(12, 11, 'Sofa Set'),
(13, 6, 'Wooden cupboard');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `cart`
--
ALTER TABLE `cart`
  ADD CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `customer` (`CustomerID`),
  ADD CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `products` (`ProductID`);

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `customer` (`CustomerID`),
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `products` (`ProductID`);

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`SubcategoryID`) REFERENCES `subcategory` (`SubID`);

--
-- Constraints for table `subcategory`
--
ALTER TABLE `subcategory`
  ADD CONSTRAINT `subcategory_ibfk_1` FOREIGN KEY (`categoryID`) REFERENCES `category` (`categoryID`);
