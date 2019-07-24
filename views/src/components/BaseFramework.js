import React from 'react';
//import ReactDOM from 'react-dom';
import "../scss/index.scss";

class HeaderNavbtn extends React.Component {
  handleActive = (e, id = this.props.id, panel) => {
    this.props.handleSpecificActive(e, id, panel)
  };

  componentDidMount() {
     if (this.props.headerActiveId === "ACTIVE") {
       this.handleActive(null)
     }
  }

  render() {
    const isActive = (this.props.id.indexOf(this.props.headerActiveId) >= 0);
    return(
      <li className="nav-item">
        <button className={"btn nav-link " + (isActive? "active":"")}
                id={this.props.id}
                onClick={this.handleActive}
        >
          {this.props.id}
        </button>
      </li>
    )
  }
}

class HeaderNavBar extends React.Component {
  componentDidMount() {
    const headerHeight = document.getElementById('header').clientHeight;
    this.uploadHeight(headerHeight);
  }

  uploadHeight = (h) => {
    this.props.getHeaderHeight(h);
  };

  handleActive = (e, id, panel) => {
    this.props.handlerGlobalActive(e, id, panel)
  };

  render() {
    return(
      <nav className="navbar navbar-expand-md navbar-dark bg-dark mb-4 fixed-top" id={"header"}>
        <a className="navbar-brand" href="/">Autop</a>
        <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse"
                aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation"><span
          className="navbar-toggler-icon" /></button>
        <div className="collapse navbar-collapse" id="navbarCollapse">
          <ul className="navbar-nav mr-auto">
            {this.props.btns.map((BTN, index) => {
              if (this.props.headerActiveId === BTN ) {
                return <BTN key={index}
                            hanlerHeaderActive={this.handleActive}
                            headerActiveId="ACTIVE"/>
              } else {
                return <BTN key={index}
                            hanlerHeaderActive={this.handleActive}
                            headerActiveId={this.props.headerActiveId} />
              }
            })}
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
    const Child = this.props.child;
    if (!Child) { return null}
    return(
      //<div style={{paddingTop : this.props.headerHeight + 17}}>
      <div className={"position-fixed vw-100 "} style={{top : this.props.headerHeight + 17, bottom:0}}>
        <Child />
      </div>
    )
  }
}

class BaseFramework extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      headerHeight : "7em",
      headerActiveId : null,
      panelActive : null
    };

    if (this.state.headerActiveId  === null && typeof this.props.DefaultActiveHeaderBtn === 'function') {
      this.state = {
        headerActiveId : this.props.DefaultActiveHeaderBtn,
        panelActive : null
      }
    }
  }

  getHeaderHeight = (h) => {
    this.setState({
      headerHeight : h
    })
  };

  handleActive = (e, id, panel) => {
    this.setState({
      headerActiveId : id,
      panelActive : panel
    });
  };

  render() {
    return(
      <React.Fragment>
        <HeaderNavBar btns                = {this.props.btns}
                      headerActiveId      = {this.state.headerActiveId}
                      handlerGlobalActive = {this.handleActive}
                      getHeaderHeight     = {this.getHeaderHeight}
                      />
        <Container child = {this.state.panelActive} headerHeight = {this.state.headerHeight} />
      </React.Fragment>
    );
  }
}



export {HeaderNavbtn, BaseFramework}
