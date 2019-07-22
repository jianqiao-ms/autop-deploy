import React from 'react';

import {HeaderNavbtn} from '../BaseFramework'

class DashboardNavbtn extends React.Component {
  handleActive = (e) => {
    console.log(e);
    this.props.handlerGlobalActive(e);
  };

  render() {
    const text = "Dashboard";
    const isActive = text.indexOf(this.props.active) >= 0;
    return(<HeaderNavbtn text={text} handleSpecificActive={this.handleActive} active={isActive}/>)
  }
}

class DashboardPanel extends React.Component {
  text = () => {
    return "Dashboard"
  };

  render() {
    return(
        <h1>Dashboard Panel</h1>
    )
  }
}

export {DashboardNavbtn, DashboardPanel}