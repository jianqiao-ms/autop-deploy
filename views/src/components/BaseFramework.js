import React from 'react';
import ReactDOM from 'react-dom';

import "../scss/index.scss";


class HeaderNavBarAnchor extends React.Component {
  render() {
    return <a href={this.props.text} className="nav-link" >{this.props.text}</a>
  }
}


class HeaderNavBarAnchorList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {active:''};

    const anchors = this.props.components.map((c) =>
      <li key={c.anchorText} className="nav-item"><HeaderNavBarAnchor text={c.anchorText}/></li>
    )
  }

  render() {
    return(
      <ul className="navbar-nav mr-auto">
        {this.anchors}
      </ul>
    )
  }
}


class HeaderNavBar extends React.Component {
  // constructor(props) {
  //   super(props)
  // }

  render() {
    return(
      <nav className="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
        <a className="navbar-brand" href="/">Autop</a>
        <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse"
                aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation"><span
          className="navbar-toggler-icon"/></button>
        <div className="collapse navbar-collapse" id="navbarCollapse">
          {/*<ul className="navbar-nav mr-auto">*/}
          {/*  <li className="nav-item"><a className="nav-link" href="#">Home</a></li>*/}
          {/*  <li className="nav-item"><a className="nav-link" href="#">Link</a></li>*/}
          {/*  <li className="nav-item"><a className="nav-link" href="#">Disabled</a></li>*/}
          {/*</ul>*/}
          <form className="form-inline mt-2 mt-md-0">
            <input className="form-control mr-sm-2" type="text" placeholder="Search" aria-label="Search" />
              <button className="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
          </form>
        </div>
      </nav>
    )
  }
}


class BaseFramework extends React.Component {
  // constructor(props) {
  //   super(props);
  // }
  render() {
    return(
      <React.Fragment>
        <HeaderNavBar />
        {this.props.containers.map( (c) => c )}
      </React.Fragment>
    );
  }
}

export {BaseFramework}