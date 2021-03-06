import React, { Component } from "react";
import {
  Route,
  NavLink,
  HashRouter
} from "react-router-dom";
import DashboardPage from './pages/Dashboard'
import CICDPage from  './pages/CICD'
import MonitorPage from './pages/Monitor'
import WebCRTPage from './pages/WebCRT'

import "./scss/index.scss";

class App extends Component {
  render() {
    return (
    <HashRouter>
      <nav className="navbar navbar-expand-md navbar-dark bg-dark mb-4 ">
       <NavLink className="navbar-brand" to="/">Autop</NavLink>
       <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse"
               aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation"><span
         className="navbar-toggler-icon" /></button>
       <div className="collapse navbar-collapse" id="navbarCollapse">
         <ul className="navbar-nav mr-auto">
           <li className="nav-item"><NavLink exact className="nav-link" to="/">Dashboard</NavLink></li>
           <li className="nav-item"><NavLink className="nav-link" to="/cicd">CICD</NavLink></li>
           <li className="nav-item"><NavLink className="nav-link" to="/monitor">Monitor</NavLink></li>
           <li className="nav-item"><NavLink className="nav-link" to="/crt">WebCRT</NavLink></li>
         </ul>
         <form className="form-inline mt-2 mt-md-0">
           <input className="form-control mr-sm-2" type="text" placeholder="Search" aria-label="Search" />
             <button className="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
         </form>
       </div>
      </nav>
      <div className="container-fluid">
        <Route exact path="/" component={DashboardPage}/>
        <Route path="/cicd" component={CICDPage}/>
        <Route path="/monitor" component={MonitorPage}/>
        <Route path="/crt" component={WebCRTPage}/>
      </div>
    </HashRouter>
    );
  }
}

export default App