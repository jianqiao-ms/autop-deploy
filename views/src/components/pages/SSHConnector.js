import React from 'react';
import {HeaderNavbtn} from '../BaseFramework'

import '../../scss/ssh_connector.scss'

import {FormInputText} from "../PublicComponents";
import {FormInputPassword} from "../PublicComponents";

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
  constructor(props){
    super(props);
    this.state = {
      isLogin : false
    }
  }
  render() {
    return(
      <div className={"container-fluid d-flex justify-content-center"}>
        {this.state.isLogin ? <SSHTerminal /> : <SSHLoginForm />}
      </div>
    )
  }
}
export {SSHConnectorNavBtn}


class SSHTerminal extends React.Component {
  render() {
    return(
      <div id={"terminal"}>Terminal</div>
    )
  }
}



class SSHLoginForm extends React.Component {
  render() {
    return(
      <div className={"bg-light shadow p-4"}>
        <FontAwesomeIcon icon="terminal" />
        <form>
          <FormInputText label={"Server FQDN"} placeholder={"IP or DNS Name of Server"}/>
          <FormInputPassword />
          <div className={"d-flex justify-content-end"}>
            <button type="submit" className="btn btn-primary">SSH Login</button>
          </div>
        </form>
      </div>
    )
  }
}