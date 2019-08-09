import React from 'react';
import {HeaderNavbtn} from '../components/BaseFramework'

class CICDNavBtn extends React.Component {
  handleActive = (e, id, panel = CICDPanel) => {
    this.props.hanlerHeaderActive(e, id, panel);
  };

  render() {
    const id = "CICD";
    return(<HeaderNavbtn id={id} handleSpecificActive={this.handleActive} headerActiveId={this.props.headerActiveId}/>)
  }
}

class CICDPanel extends React.Component {
  render() {
    return(
        <h1>CICD Panel</h1>
    )
  }
}

export {CICDNavBtn}