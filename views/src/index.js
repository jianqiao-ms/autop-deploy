import React from 'react';
import ReactDOM from 'react-dom';

// BaseFramework
import {BaseFramework} from './components/BaseFramework'

//NavBtns
import {DashboardNavbtn} from "./components/pages/dashboard";
import {CICDNavBtn} from "./components/pages/CICD";

// Panels
import {DashboardPanel} from './components/pages/dashboard'
import {CICDPanel} from "./components/pages/CICD";

const navBtns = [
  DashboardNavbtn,
  CICDNavBtn
];

const panels = [
  <DashboardPanel />,
  <CICDPanel/>
];

ReactDOM.render(
  <BaseFramework btns = {navBtns} panels={panels}/>,
  document.getElementById('root')
);