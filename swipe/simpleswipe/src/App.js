import React from 'react';
//import logo from './logo.svg';
import './App.css';

class App extends React.Component
{
    render() {
      return (
        <div className="App">
            <div className="mydiv">Swipe me</div>
            <div className="mydiv" data-swipe-threshold="100">or me</div>
        </div>
      );
    }
}

export default App;
