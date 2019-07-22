import React from 'react';
import {HeaderNavbtn} from '../BaseFramework'

import '../../scss/index.scss'


class CICDNavBtn extends React.Component {
  handleActive = (e) => {
    this.props.handlerGlobalActive(e);

  };

  render() {
    const text = "CICD";
    const isActive = text.indexOf(this.props.active) >= 0;
    return(<HeaderNavbtn text={text} handleSpecificActive={this.handleActive} active={isActive}/>)
  }
}

class CICDPanel extends React.Component {

  render() {
    return(
        <h1>CICD Panel</h1>
    )
  }
}

export {CICDNavBtn, CICDPanel}