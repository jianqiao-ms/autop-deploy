import React from 'react';
import {HeaderNavbtn} from '../BaseFramework'
import '../../scss/ssh_connector.scss'

import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faTerminal} from "@fortawesome/free-solid-svg-icons";

import {handlerInputChangeContext} from "../PublicComponents";
import {FormInput} from "../PublicComponents";

import {Terminal} from "xterm";
import * as fit from 'xterm/lib/addons/fit/fit';
import * as fullscreen from 'xterm/lib/addons/fullscreen/fullscreen';
import Websocket from 'react-websocket'

Terminal.applyAddon(fit);
Terminal.applyAddon(fullscreen);
// Header And Console Control
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
        {/*{this.state.isLogin ? <SSHTerminal /> : <SSHLoginForm />}*/}
        {this.state.isLogin ? <SSHLoginForm /> : <SSHTerminal />}
      </div>
    )
  }
}
export {SSHConnectorNavBtn}

// Console modules

class SSHTerminal extends React.Component {
  constructor(props) {
    super(props);
    this.term = new Terminal();
  }
  componentDidMount() {
    this.term.open(this.termDiv);
    console.log(this.term.rows)
    this.term.fit();
    console.log(this.term.rows)
    this.term.write('Hello from \x1B[1;3;31mxterm.js\x1B[0mHello from \x1B[1;3;31mxterm.js\x1B[0mHello from \x1B[1;3;31mxterm.js\x1B[0mHello from \x1B[1;3;31mxterm.js\x1B[0mHello from \x1B[1;3;31mxterm.js\x1B[0mHello from \x1B[1;3;31mxterm.js\x1B[0mHello from \x1B[1;3;31mxterm.js\x1B[0mHello from \x1B[1;3;31mxterm.js\x1B[0m $ ')
  }

  render() {

    return(
      <div className={"w-100 vh-100"} id={"terminal"} ref={ _this => this.termDiv = _this} />
    )
  }
}

class SSHLoginForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      fqdn : "",
      port : "",
      pasword : ""
    }
  }

  handlerSubmit = (e) => {
    e.preventDefault();
  };

  render() {
    return(
      <div className={"bg-light shadow p-3 rounded-lg" + this.props.extraClasses}>
        <div className={"pt-1 mb-3 mr-3"}><FontAwesomeIcon icon={faTerminal} size="3x" className={"text-light bg-secondary p-2 rounded"}/></div>
        <form>
          <handlerInputChangeContext.Provider value={(e, id) => this.setState({[id]:e.target.value})}>
            <FormInput label={"Server FQDN"} placeholder={"IP or DNS Name of Server"} id={"fqdn"} />
            <FormInput label={"SSH Port"} placeholder={"SSH Port. Default 22"} id={"port"} />
            <FormInput type={"password"} label={"Host Password"} id={"pasword"} />
          </handlerInputChangeContext.Provider>
          <div className={"d-flex justify-content-end"}>
            <button type="submit" className="btn btn-primary" onClick={this.handlerSubmit}>SSH Login</button>
          </div>
        </form>
      </div>
    )
  }
}