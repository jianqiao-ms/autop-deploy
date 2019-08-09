import React from 'react';
import {HeaderNavbtn} from '../components/BaseFramework'
import '../scss/ssh_connector.scss'

import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faTerminal} from "@fortawesome/free-solid-svg-icons";

import {handlerInputChangeContext} from "../PublicComponents";
import {FormInput} from "../PublicComponents";

import Websocket from 'react-websocket';
import {Terminal} from "xterm";
import * as fit from 'xterm/lib/addons/fit/fit';
import * as fullscreen from 'xterm/lib/addons/fullscreen/fullscreen';
import * as attach from 'xterm/lib/addons/attach/attach';

Terminal.applyAddon(fit);
Terminal.applyAddon(attach);
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
      isLogin : false,
      socket : null
    }
  }

  handlerLogin = () => {this.setState({isLogin : true})};

  render() {
    return(
      <div className={"container-fluid d-flex justify-content-center"}>
        {
          this.state.isLogin ?
          <SSHTerminal /> :
          <SSHLoginForm handlerLogin = {this.handlerLogin}/>
        }
        {/*{this.state.isLogin ? <SSHLoginForm /> : <SSHTerminal />}*/}
      </div>
    )
  }
}
export {SSHConnectorNavBtn}

// Console modules

class SSHTerminal extends React.Component {
  componentDidMount() {
    let ws = new WebSocket('ws://localhost:8080/websocket');
    let term = new Terminal();
    term.open(this.termDiv);
    ws.onopen = function(event) {

        term.on('data', function(data) {
            ws.send(JSON.stringify(['stdin', data]));
        });

        term.on('title', function(title) {
            document.title = title;
        });

        ws.onmessage = function(event) {

        };
    };
  }

  updateTerminal = (e) => {
    // const json_msg = JSON.parse(e.data);
    // switch(json_msg[0]) {
    //     case "stdout":
    //         term.write(json_msg[1]);
    //         break;
    //     case "disconnect":
    //         term.write("\r\n\r\n[Finished... Terminado]\r\n");
    //         break;
    // }
  };

  render() {
    return(
      <React.Fragment>
      <div className={"w-100 vh-100"} id={"terminal"} ref={ _this => this.termDiv = _this} />
      <Websocket url={'ws://localhost:8080/websocket'} onMessage={this.updateTerminal}/>
      </React.Fragment>
    )
  }
}

class SSHLoginForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      fqdn : "",
      port : "22",
      user : "",
      pasword : ""
    }
  }

  handlerSubmit = (e) => {
    e.preventDefault();
    this.props.handlerLogin(e, this.state)
  };

  render() {
    return(
      <div className={"bg-light shadow p-3 rounded-lg" + this.props.extraClasses}>
        <div className={"pt-1 mb-3 mr-3"}><FontAwesomeIcon icon={faTerminal} size="3x" className={"text-light bg-secondary p-2 rounded"}/></div>
        <form>
          <handlerInputChangeContext.Provider value={(e, id) => this.setState({[id]:e.target.value})}>
            <FormInput label={"Server FQDN"} placeholder={"IP or DNS Name of Server"} id={"fqdn"} />
            <FormInput label={"SSH Port"} placeholder={"SSH Port. Default 22"}     id={"port"} />
            <FormInput label={"User"} placeholder={"SSH User"}     id={"user"} />
            <FormInput label={"Password"} id={"pasword"} type={"password"}/>
          </handlerInputChangeContext.Provider>
          <div className={"d-flex justify-content-end"}>
            <button type="submit" className="btn btn-primary" onClick={this.handlerSubmit}>SSH Login</button>
          </div>
        </form>
      </div>
    )
  }
}