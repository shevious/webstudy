//import React from 'react';
import SwipeableViews from './SwipeableViews.js';

const styles = {
  slideContainer: {
    height: 200,
  },
  slide: {
    //padding: 15,
    minHeight: 200,
    color: '#fff',
  },
  slide1: {
    backgroundColor: '#FEA900',
  },
  slide2: {
    backgroundColor: '#B3DC4A',
  },
  slide3: {
    backgroundColor: '#6AC0FF',
  },
};


const Vertical = () => {
  return (
    <SwipeableViews containerStyle={styles.slideContainer} enableMouseEvents axis="y" resistance>
      <div style={Object.assign({}, styles.slide, styles.slide1)}>slide n°1</div>
      <div style={Object.assign({}, styles.slide, styles.slide2)}>slide n°2</div>
      <div style={Object.assign({}, styles.slide, styles.slide3)}>slide n°3</div>
    </SwipeableViews>
  );
};

export default Vertical;

