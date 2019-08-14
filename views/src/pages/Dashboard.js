import React from 'react';

class DashboardPage extends React.Component {

  render() {
    return(<DashboardPanel />)
  }
}

class DashboardPanel extends React.Component {
  render() {
    return(
        <h1>Dashboard Panel</h1>
    )
  }
}

export default DashboardPage