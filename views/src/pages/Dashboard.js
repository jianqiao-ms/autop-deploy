import React from 'react';
import {HeaderNavbtn} from '../components/BaseFramework'

class DashboardNavbtn extends React.Component {
  handleActive = (e, id, panel = DashboardPanel) => {
    this.props.hanlerHeaderActive(e, id, panel);
  };

  render() {
    const id = "Dashboard";
    return(<HeaderNavbtn id={id} handleSpecificActive={this.handleActive} headerActiveId={this.props.headerActiveId}/>)
  }
}

class DashboardPanel extends React.Component {
  render() {
    return(
        <h1>Dashboard Panel</h1>
    )
  }
}

export {DashboardNavbtn}