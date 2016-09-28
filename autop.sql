/*
Navicat MySQL Data Transfer

Source Server         : local-195
Source Server Version : 50626
Source Host           : 192.168.0.195:3306
Source Database       : autop

Target Server Type    : MYSQL
Target Server Version : 50626
File Encoding         : 65001

Date: 2016-09-28 18:13:28
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for t_assets_env
-- ----------------------------
DROP TABLE IF EXISTS `t_assets_env`;
CREATE TABLE `t_assets_env` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `environment` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_assets_env
-- ----------------------------
INSERT INTO `t_assets_env` VALUES ('1', '测试环境');

-- ----------------------------
-- Table structure for t_assets_history
-- ----------------------------
DROP TABLE IF EXISTS `t_assets_history`;
CREATE TABLE `t_assets_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `repo` varchar(255) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`) USING HASH
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_assets_history
-- ----------------------------
INSERT INTO `t_assets_history` VALUES ('1', 'git@192.168.1.141:devs/imanager.git', 'imanager_core');
INSERT INTO `t_assets_history` VALUES ('2', 'git@192.168.1.141:devs/imanager_web.git', 'imanager_web');
INSERT INTO `t_assets_history` VALUES ('3', 'git@192.168.1.141:devs/imanager_api.git', 'api');
INSERT INTO `t_assets_history` VALUES ('4', 'git@192.168.1.141:devs/imanager_iservice.git', 'iservice');
INSERT INTO `t_assets_history` VALUES ('5', 'git@192.168.1.141:devs/iservice.git', 'actor');

-- ----------------------------
-- Table structure for t_assets_host
-- ----------------------------
DROP TABLE IF EXISTS `t_assets_host`;
CREATE TABLE `t_assets_host` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(255) DEFAULT 'localhost.localdomain',
  `alias` varchar(255) DEFAULT 'localhost',
  `ip_addr` varchar(15) NOT NULL,
  `env_id` int(11) NOT NULL,
  `type_id` varchar(255) DEFAULT '1',
  `group_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`,`ip_addr`,`env_id`),
  UNIQUE KEY `ip_addr` (`ip_addr`,`env_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_assets_host
-- ----------------------------
INSERT INTO `t_assets_host` VALUES ('1', 'localhost', 'localhost', '192.168.0.105', '0', '1', '1');
INSERT INTO `t_assets_host` VALUES ('2', 'localhost', 'localhost', '192.168.0.106', '0', '1', '1');
INSERT INTO `t_assets_host` VALUES ('3', 'localhost', 'localhost', '192.168.0.111', '0', '1', '2');
INSERT INTO `t_assets_host` VALUES ('4', 'localhost', 'localhost', '192.168.0.112', '0', '1', '2');
INSERT INTO `t_assets_host` VALUES ('5', 'localhost', 'localhost', '192.168.0.81', '1', '1', null);
INSERT INTO `t_assets_host` VALUES ('6', 'localhost', 'localhost', '192.168.0.61', '1', '1', null);

-- ----------------------------
-- Table structure for t_assets_hostgroup
-- ----------------------------
DROP TABLE IF EXISTS `t_assets_hostgroup`;
CREATE TABLE `t_assets_hostgroup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `env_id` int(11) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`,`name`),
  UNIQUE KEY `name` (`name`,`env_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_assets_hostgroup
-- ----------------------------
INSERT INTO `t_assets_hostgroup` VALUES ('1', 'imanager', '1', 'hosts in imanager cluster');
INSERT INTO `t_assets_hostgroup` VALUES ('2', 'iservice', '1', 'hosts in iservice cluster');

-- ----------------------------
-- Table structure for t_assets_hosttype
-- ----------------------------
DROP TABLE IF EXISTS `t_assets_hosttype`;
CREATE TABLE `t_assets_hosttype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_assets_hosttype
-- ----------------------------
INSERT INTO `t_assets_hosttype` VALUES ('1', 'Linux');

-- ----------------------------
-- Table structure for t_assets_project
-- ----------------------------
DROP TABLE IF EXISTS `t_assets_project`;
CREATE TABLE `t_assets_project` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `repo` varchar(255) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`) USING HASH
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_assets_project
-- ----------------------------
INSERT INTO `t_assets_project` VALUES ('1', 'http://192.168.1.141/devs/imanager.git', 'imanager_core');
INSERT INTO `t_assets_project` VALUES ('2', 'http://192.168.1.141/devs/imanager_web.git', 'imanager_web');
INSERT INTO `t_assets_project` VALUES ('3', 'http://192.168.1.141/devs/imanager_api.git', 'api');
INSERT INTO `t_assets_project` VALUES ('4', 'http://192.168.1.141/devs/imanager_iservice.git', 'iservice');
INSERT INTO `t_assets_project` VALUES ('5', 'http://192.168.1.141/devs/iservice.git', 'actor');

-- ----------------------------
-- Table structure for t_assets_project_deploy_settings
-- ----------------------------
DROP TABLE IF EXISTS `t_assets_project_deploy_settings`;
CREATE TABLE `t_assets_project_deploy_settings` (
  `id` int(11) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `env_id` int(255) DEFAULT NULL,
  `branch` varchar(255) DEFAULT NULL,
  `update_method` enum('增量更新','全量更新') DEFAULT NULL,
  `host_id` int(11) DEFAULT NULL,
  `hostgroup_id` int(11) DEFAULT NULL,
  UNIQUE KEY `project_id` (`project_id`,`env_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_assets_project_deploy_settings
-- ----------------------------

-- ----------------------------
-- Table structure for t_deploy_history
-- ----------------------------
DROP TABLE IF EXISTS `t_deploy_history`;
CREATE TABLE `t_deploy_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) DEFAULT NULL,
  `env_id` int(11) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `create_user` varchar(255) DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `start_user` varchar(255) DEFAULT NULL,
  `finish_time` datetime DEFAULT NULL,
  `finish_status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_id` (`project_id`,`env_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_deploy_history
-- ----------------------------

-- ----------------------------
-- Table structure for t_deploy_running
-- ----------------------------
DROP TABLE IF EXISTS `t_deploy_running`;
CREATE TABLE `t_deploy_running` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) DEFAULT NULL,
  `env_id` int(11) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `create_user` varchar(255) DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `start_user` varchar(255) DEFAULT NULL,
  `finish_time` datetime DEFAULT NULL,
  `finish_status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_id` (`project_id`,`env_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_deploy_running
-- ----------------------------
