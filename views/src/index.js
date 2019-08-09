import React from 'react';
import ReactDOM from 'react-dom';

import "./scss/index.scss";

// BaseFramework
import {BaseFramework} from './components/BaseFramework'

//NavBtns
import {DashboardNavbtn} from "./pages/Dashboard";
import {MonitorNavBtn} from "./pages/Monitor";
import {CICDNavBtn} from "./pages/CICD";
import {SSHConnectorNavBtn} from "./pages/SSHConnector";

const navBtns = [
  DashboardNavbtn,
  MonitorNavBtn,
  CICDNavBtn,
  SSHConnectorNavBtn
];

ReactDOM.render(
  <BaseFramework btns = {navBtns} DefaultActiveHeaderBtn = {SSHConnectorNavBtn} />,
  document.getElementById('root')
);