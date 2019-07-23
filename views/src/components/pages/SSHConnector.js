import React from 'react';
import {HeaderNavbtn} from '../BaseFramework'

class SSHConnectorNavBtn extends React.Component {
  handleActive = (e, id, panel = SSHConnectorPanel) => {
    this.props.hanlerHeaderActive(e, id, panel);
  };

  render() {
    const id = "SSHConnector";
    return(<HeaderNavbtn id={id} handleSpecificActive={this.handleActive} headerActiveId={this.props.headerActiveId}/>)
  }
}

class SSHConnectorPanel extends React.Component {
  render() {
    return(
        <h1>SSHConnector Panel</h1>
    )
  }
}

export {SSHConnectorNavBtn}