import React from 'react';

import "../scss/index.scss";

class HeaderNavbtn extends React.Component {
  handleActive = (e) => {
    this.props.handleSpecificActive(e)
  };

  render() {
    return(
      <li className="nav-item">
        <button className={"btn nav-link " + (this.props.active? "active":"")}
                id={this.props.text}
                onClick={this.handleActive}
        >
          {this.props.text}
        </button>
      </li>
    )
  }
}

class HeaderNavBar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {active:null};
    // this.btnList = props.btns.map(
    //   (BTN) => <BTN handlerGlobalActive={this.handleActive} key={BTN.name} active={this.state.active}/>
    //   );
  }


  handleActive = (e) => {
    this.setState({active:e.target.id});
  };

  componentDidMount = () => {

  };


  render() {
    return(
      <nav className="navbar navbar-expand-md navbar-dark bg-dark mb-4"><a className="navbar-brand" href="/">Autop</a>
        <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse"
                aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation"><span
          className="navbar-toggler-icon" /></button>
        <div className="collapse navbar-collapse" id="navbarCollapse">
          <ul className="navbar-nav mr-auto">
            {this.props.btns.map(
              (BTN) => <BTN handlerGlobalActive={this.handleActive} key={BTN.name} active={this.state.active}/>
              )}
          </ul>
          <form className="form-inline mt-2 mt-md-0">
            <input className="form-control mr-sm-2" type="text" placeholder="Search" aria-label="Search" />
              <button className="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
          </form>
        </div>
      </nav>
    )
  }
}

class Container extends React.Component {
  render() {
    return(
      <div className={"container-fluid fixed-top mt-5 p-0"}>
        {this.props.children}
      </div>
    )
  }
}

class BaseFramework extends React.Component {
  render() {
    return(
      <React.Fragment>
        <HeaderNavBar btns = {this.props.btns}/>
        <Container panels = {this.props.panels}/>
      </React.Fragment>
    );
  }
}

export {HeaderNavbtn, BaseFramework}