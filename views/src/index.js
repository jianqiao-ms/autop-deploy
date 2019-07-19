import React from 'react';
import ReactDOM from 'react-dom';



import {BaseFramework} from './components/BaseFramework'
import {DashboardContent} from './components/pages/dashboard'




const containers = [
  <DashboardContent />
];


ReactDOM.render(
  <BaseFramework containers = {containers} />,
  document.getElementById('root')
);