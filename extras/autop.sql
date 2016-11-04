/*
Navicat MySQL Data Transfer

Source Server         : local_195
Source Server Version : 50626
Source Host           : 192.168.0.195:3306
Source Database       : autop

Target Server Type    : MYSQL
Target Server Version : 50626
File Encoding         : 65001

Date: 2016-11-04 10:40:56
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for t_assets_env
-- ----------------------------
DROP TABLE IF EXISTS `t_assets_env`;
CREATE TABLE `t_assets_env` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `environment` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for t_assets_host
-- ----------------------------
DROP TABLE IF EXISTS `t_assets_host`;
CREATE TABLE `t_assets_host` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT 'localhost.localdomain',
  `ip_addr` varchar(15) NOT NULL,
  `hg_id` varchar(2) DEFAULT '',
  `env_id` varchar(2) NOT NULL,
  PRIMARY KEY (`id`,`ip_addr`,`env_id`),
  UNIQUE KEY `ip_addr` (`ip_addr`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for t_assets_hostgroup
-- ----------------------------
DROP TABLE IF EXISTS `t_assets_hostgroup`;
CREATE TABLE `t_assets_hostgroup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT '',
  `env_id` varchar(2) NOT NULL,
  PRIMARY KEY (`id`,`name`),
  UNIQUE KEY `name` (`name`,`env_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for t_assets_proj_branch
-- ----------------------------
DROP TABLE IF EXISTS `t_assets_proj_branch`;
CREATE TABLE `t_assets_proj_branch` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `branch` varchar(255) DEFAULT NULL,
  `proj_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `proj_id` (`proj_id`,`branch`)
) ENGINE=TokuDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for t_assets_project
-- ----------------------------
DROP TABLE IF EXISTS `t_assets_project`;
CREATE TABLE `t_assets_project` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `repo` varchar(255) NOT NULL,
  `name` varchar(255) DEFAULT '',
  `alias` varchar(255) DEFAULT '',
  `webapp_name` varchar(255) DEFAULT NULL,
  `reliable` tinyint(1) DEFAULT '0',
  `rely_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `repo` (`repo`) USING BTREE,
  UNIQUE KEY `alias` (`alias`),
  UNIQUE KEY `name` (`name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for t_deploy_auto_rule
-- ----------------------------
DROP TABLE IF EXISTS `t_deploy_auto_rule`;
CREATE TABLE `t_deploy_auto_rule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `proj_id` int(11) DEFAULT NULL,
  `proj_branch` varchar(255) DEFAULT NULL,
  `host_id` int(11) DEFAULT NULL,
  `hg_id` int(11) DEFAULT NULL,
  `token` varchar(13) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_id` (`proj_id`)
) ENGINE=TokuDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for t_deploy_history
-- ----------------------------
DROP TABLE IF EXISTS `t_deploy_history`;
CREATE TABLE `t_deploy_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pb_id` int(11) DEFAULT NULL,
  `event` varchar(16) DEFAULT NULL,
  `type` enum('auto','manual') DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `before_commit` varchar(255) DEFAULT NULL,
  `after_commit` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=TokuDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for t_deploy_history1
-- ----------------------------
DROP TABLE IF EXISTS `t_deploy_history1`;
CREATE TABLE `t_deploy_history1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ar_id` int(11) DEFAULT NULL,
  `before` varchar(255) DEFAULT NULL,
  `after` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=TokuDB DEFAULT CHARSET=utf8;
SET FOREIGN_KEY_CHECKS=1;
