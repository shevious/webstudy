import React, { Component } from "react";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import SwipeableRoutes from "react-swipeable-routes";
import SwipeableViews from "react-swipeable-views";
import Swiper from 'react-id-swiper';
import 'react-id-swiper/lib/styles/css/swiper.css';

class RedView extends Component {
  componentDidMount(){
    console.log("RedView componentDidMount");
  }
  render() {
    return (
      <div style={{ height: 300, backgroundColor: "red" }}>Red</div>
    )
  }
};

class WhiteView extends Component {
  render() {
    return (
      <SwipeableViews enableMouseEvents style={{ height: 300, backgroundColor: "white" }}>
        <Swiper>
          <div style={{ height: 200, backgroundColor: '#FEA900' }}>Slide #1</div>
          <div style={{ height: 200, backgroundColor: '#B3DC4A' }}>Slide #2</div>
          <div style={{ height: 200, backgroundColor: '#6AC0FF' }}>Slide #3</div>
          <div style={{ height: 200, backgroundColor: "rgb(0, 255, 149)" }}>Slide #4</div>
          <div style={{ height: 200, backgroundColor: "rgb(116, 106, 91)" }}>Slide #5</div>
        </Swiper>
      </SwipeableViews>
    )
  }
};

class BlueView extends Component {
  componentDidMount(){
    console.log("BlueView componentDidMount");
  }
  render() {
    return (
      <div style={{ height: 300, backgroundColor: "blue" }}>Blue</div>
    )
  }
};

class GreenView extends Component {
  componentDidMount(){
    console.log("GreenView componentDidMount");
  }
  render() {
    return (
      <div style={{ height: 300, backgroundColor: "green" }}>Green</div>
    )
  }
};

class YellowView extends Component {
  componentDidMount(){
    console.log("YellowView componentDidMount");
  }
  render() {
    return (
      <div style={{ height: 300, backgroundColor: "yellow" }}>Yellow</div>
    )
  }
};

const OtherColorView = ({ match }) => (
  <div style={{ height: 300, backgroundColor: match.params.color }}>
    {match.params.color}
  </div>
);

class App extends Component {
  render() {
    return (
      <Router>
        <div className="App">
          <div>
            <Link to="/red">Red</Link> |
            <Link to="/white">Swiper</Link> |
            <Link to="/blue">Blue</Link> |
            <Link to="/green">Green</Link> |
            <Link to="/yellow">Yellow</Link> |
            <Link to="/other/palevioletred">Pale Violet Red</Link> |
            <Link to="/other/saddlebrown">Saddle Brown</Link>
          </div>

          <SwipeableRoutes enableMouseEvents>
            <Route path="/red" component={RedView} />
            <Route path="/white" component={WhiteView} />
            <Route path="/blue" component={BlueView} />
            <Route path="/green" component={GreenView} />
            <Route path="/yellow" component={YellowView} />
            <Route
              path="/other/:color"
              component={OtherColorView}
              defaultParams={{ color: "grey" }}
            />
          </SwipeableRoutes>
        </div>
      </Router>
    );
  }
}

export default App;

