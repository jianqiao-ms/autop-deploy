import React from 'react';
import ReactDOM from 'react-dom';

import '../../scss/index.scss'

class DashboardContent extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    const anchorText = 'Dashboard';
    return(
      <div key={anchorText} className={"container-fluid"}>
        <h1>{anchorText} Content</h1>
      </div>
    )
  }
}

export {DashboardContent}