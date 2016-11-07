/*
Navicat MySQL Data Transfer

Source Server         : local_195
Source Server Version : 50626
Source Host           : 192.168.0.195:3306
Source Database       : autop

Target Server Type    : MYSQL
Target Server Version : 50626
File Encoding         : 65001

Date: 2016-11-07 18:08:10
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
-- Records of t_assets_env
-- ----------------------------
INSERT INTO `t_assets_env` VALUES ('1', '测试环境');

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
-- Records of t_assets_host
-- ----------------------------
INSERT INTO `t_assets_host` VALUES ('12', 'imanager_105.localdomain\n', '192.168.0.105', '', '1');
INSERT INTO `t_assets_host` VALUES ('13', 'master_150.localdomain\n', '192.168.0.150', '5', '1');
INSERT INTO `t_assets_host` VALUES ('15', 'actor_152.localdomain\n', '192.168.0.152', '5', '1');
INSERT INTO `t_assets_host` VALUES ('16', 'actor_153.localdomain\n', '192.168.0.153', '5', '1');
INSERT INTO `t_assets_host` VALUES ('17', 'actor_154.localdomain\n', '192.168.0.154', '5', '1');

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
-- Records of t_assets_hostgroup
-- ----------------------------
INSERT INTO `t_assets_hostgroup` VALUES ('5', 'actor', '', '1');

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
) ENGINE=TokuDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_assets_proj_branch
-- ----------------------------
INSERT INTO `t_assets_proj_branch` VALUES ('17', 'export_ygrs', '1');
INSERT INTO `t_assets_proj_branch` VALUES ('18', 'imanager_monthlyReport', '1');
INSERT INTO `t_assets_proj_branch` VALUES ('24', 'master', '1');
INSERT INTO `t_assets_proj_branch` VALUES ('19', 'webhooks', '1');
INSERT INTO `t_assets_proj_branch` VALUES ('22', 'devlop', '4');
INSERT INTO `t_assets_proj_branch` VALUES ('25', 'master', '4');
INSERT INTO `t_assets_proj_branch` VALUES ('23', 'imanager_web_monthlyReport', '5');
INSERT INTO `t_assets_proj_branch` VALUES ('26', 'master', '5');

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
  `full_update` tinyint(1) DEFAULT '0',
  `artifact` varchar(255) DEFAULT NULL,
  `rely_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `repo` (`repo`) USING BTREE,
  UNIQUE KEY `alias` (`alias`),
  UNIQUE KEY `name` (`name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_assets_project
-- ----------------------------
INSERT INTO `t_assets_project` VALUES ('1', 'http://192.168.1.141/devs/imanager.git', 'imanager', 'imanager_core', 'WEB-INF/lib', '1', '1', 'imanager_core-0.0.1-SNAPSHOT.jar', '0');
INSERT INTO `t_assets_project` VALUES ('4', 'http://192.168.1.141/devs/iservice.git', 'iservice', 'actor', 'iservice', '0', '0', null, '1');
INSERT INTO `t_assets_project` VALUES ('5', 'http://192.168.1.141/devs/imanager_web.git', 'imanager_web', 'imanager_web', 'imanager', '0', '0', null, '1');

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
) ENGINE=TokuDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_deploy_auto_rule
-- ----------------------------
INSERT INTO `t_deploy_auto_rule` VALUES ('6', '1', 'master', null, null, 'dhkAf1IRmGc6v');
INSERT INTO `t_deploy_auto_rule` VALUES ('8', '4', 'master', null, '5', 'Fi92RZVaIeGM4');
INSERT INTO `t_deploy_auto_rule` VALUES ('9', '5', 'master', '12', null, 'glpyYAuXe9aIH');

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
  `status` varchar(4096) DEFAULT 'OK',
  PRIMARY KEY (`id`)
) ENGINE=TokuDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_deploy_history
-- ----------------------------
INSERT INTO `t_deploy_history` VALUES ('18', '17', 'INIT', 'manual', '2016-11-03 10:57:13', null, '80c5ce63f744c179c323c5927e3ccf5caa5a63ea', null);
INSERT INTO `t_deploy_history` VALUES ('19', '18', 'INIT', 'manual', '2016-11-03 10:57:14', null, '5bb7e026f4abfa073053228103c0f2851d720b1e', null);
INSERT INTO `t_deploy_history` VALUES ('20', '19', 'INIT', 'manual', '2016-11-03 10:57:14', null, '65938b0c6d6a6fff9b01df9aa3b1a5c1e47f6edf', null);
INSERT INTO `t_deploy_history` VALUES ('23', '22', 'INIT', 'manual', '2016-11-03 17:07:14', null, '0e1b855a1ec8e9c86db704e05f885e555010e645', null);
INSERT INTO `t_deploy_history` VALUES ('24', '23', 'INIT', 'manual', '2016-11-04 11:21:39', null, '6f2ee86bd3f055bc12f2ec569221353d73afc601', null);

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

-- ----------------------------
-- Records of t_deploy_history1
-- ----------------------------
SET FOREIGN_KEY_CHECKS=1;
