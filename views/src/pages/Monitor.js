import React from 'react';
import {HeaderNavbtn} from '../components/BaseFramework'

class MonitorNavBtn extends React.Component {
  handleActive = (e, id, panel = MonitorPanel) => {
    this.props.hanlerHeaderActive(e, id, panel);
  };

  render() {
    const id = "Monitor";
    return(<HeaderNavbtn id={id} handleSpecificActive={this.handleActive} headerActiveId={this.props.headerActiveId}/>)
  }
}

class MonitorPanel extends React.Component {
  render() {
    return(
        <h1>Monitor Panel</h1>
    )
  }
}

export {MonitorNavBtn}