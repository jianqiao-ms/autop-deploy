/*
Navicat MySQL Data Transfer

Source Server         : local-195
Source Server Version : 50626
Source Host           : 192.168.0.195:3306
Source Database       : autop

Target Server Type    : MYSQL
Target Server Version : 50626
File Encoding         : 65001

Date: 2016-08-29 18:25:13
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for t_assets_env
-- ----------------------------
DROP TABLE IF EXISTS `t_assets_env`;
CREATE TABLE `t_assets_env` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `environment` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `environment` (`environment`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_assets_env
-- ----------------------------

-- ----------------------------
-- Table structure for t_assets_host
-- ----------------------------
DROP TABLE IF EXISTS `t_assets_host`;
CREATE TABLE `t_assets_host` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
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
INSERT INTO `t_assets_host` VALUES ('1', '192.168.0.105', '0', '1', '1');
INSERT INTO `t_assets_host` VALUES ('2', '192.168.0.106', '0', '1', '1');
INSERT INTO `t_assets_host` VALUES ('3', '192.168.0.111', '0', '1', '2');
INSERT INTO `t_assets_host` VALUES ('4', '192.168.0.112', '0', '1', '2');
INSERT INTO `t_assets_host` VALUES ('5', '192.168.0.81', '0', '1', null);
INSERT INTO `t_assets_host` VALUES ('6', '192.168.0.61', '0', '1', null);

-- ----------------------------
-- Table structure for t_assets_hostgroup
-- ----------------------------
DROP TABLE IF EXISTS `t_assets_hostgroup`;
CREATE TABLE `t_assets_hostgroup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `env_id` int(11) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`,`name`,`env_id`),
  UNIQUE KEY `name` (`name`,`env_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_assets_hostgroup
-- ----------------------------
INSERT INTO `t_assets_hostgroup` VALUES ('1', 'imanager', '0', 'hosts in imanager cluster');
INSERT INTO `t_assets_hostgroup` VALUES ('2', 'iservice', '0', 'hosts in iservice cluster');

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
INSERT INTO `t_assets_project` VALUES ('1', 'git@192.168.1.141:devs/imanager.git', 'imanager_core');
INSERT INTO `t_assets_project` VALUES ('2', 'git@192.168.1.141:devs/imanager_web.git', 'imanager_web');
INSERT INTO `t_assets_project` VALUES ('3', 'git@192.168.1.141:devs/imanager_api.git', 'api');
INSERT INTO `t_assets_project` VALUES ('4', 'git@192.168.1.141:devs/imanager_iservice.git', 'iservice');
INSERT INTO `t_assets_project` VALUES ('5', 'git@192.168.1.141:devs/iservice.git', 'actor');

-- ----------------------------
-- Table structure for t_deploy_task
-- ----------------------------
DROP TABLE IF EXISTS `t_deploy_task`;
CREATE TABLE `t_deploy_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `template_id` int(11) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `create_user` varchar(255) DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `start_user` varchar(255) DEFAULT NULL,
  `finish_time` datetime DEFAULT NULL,
  `finish_status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_deploy_task
-- ----------------------------
INSERT INTO `t_deploy_task` VALUES ('1', '2', '2016-07-27 16:10:04', 'admin', null, null, null, null);
INSERT INTO `t_deploy_task` VALUES ('2', '1', '2016-07-27 15:51:29', 'admin', null, null, null, null);

-- ----------------------------
-- Table structure for t_deploy_template
-- ----------------------------
DROP TABLE IF EXISTS `t_deploy_template`;
CREATE TABLE `t_deploy_template` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `deploy_method` enum('host','hostgroup') DEFAULT NULL,
  `infrastructure_id` int(11) DEFAULT NULL,
  `deploy_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_deploy_template
-- ----------------------------
INSERT INTO `t_deploy_template` VALUES ('1', 'imanager', '2', 'hostgroup', '1', '/usr/local/tomcat1/webapps/imanager');
INSERT INTO `t_deploy_template` VALUES ('2', 'iservice', '4', 'hostgroup', '2', '/usr/local/tomcat1/webapps/iservice');
INSERT INTO `t_deploy_template` VALUES ('3', 'api', '3', 'host', '6', '/usr/local/tomcat1/webapps/api');

-- ----------------------------
-- Table structure for t_map_deploy_env
-- ----------------------------
DROP TABLE IF EXISTS `t_map_deploy_env`;
CREATE TABLE `t_map_deploy_env` (
  `id` int(11) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `env_id` int(11) DEFAULT NULL,
  `host/hostgroup_id` int(11) DEFAULT NULL,
  `deploy_path` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_map_deploy_env
-- ----------------------------
