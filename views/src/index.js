import React from 'react';
import ReactDOM from 'react-dom';

import "../scss/index.scss";

// BaseFramework
import {BaseFramework} from './components/BaseFramework'

//NavBtns
import {DashboardNavbtn} from "./components/pages/Dashboard";
import {MonitorNavBtn} from "./components/pages/Monitor";
import {CICDNavBtn} from "./components/pages/CICD";
import {SSHConnectorNavBtn} from "./components/pages/SSHConnector";

const navBtns = [
  DashboardNavbtn,
  MonitorNavBtn,
  CICDNavBtn,
  SSHConnectorNavBtn
];

ReactDOM.render(
  <BaseFramework btns = {navBtns} DefaultActiveHeaderBtn = {DashboardNavbtn} />,
  document.getElementById('root')
);