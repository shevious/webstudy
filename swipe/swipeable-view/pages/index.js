//import React from 'react';
import SwipeableViews from 'react-swipeable-views';
import Link from 'next/link';

const styles = {
  slide: {
    padding: 15,
    minHeight: 100,
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


const Index = () => {
  return (
    <div>
    <SwipeableViews enableMouseEvents>
      <div style={Object.assign({}, styles.slide, styles.slide1)}>slide n°1</div>
      <div style={Object.assign({}, styles.slide, styles.slide2)}>slide n°2</div>
      <div style={Object.assign({}, styles.slide, styles.slide3)}>slide n°3</div>
    </SwipeableViews>
    <Link href="/effect">
        <a>effect</a>
    </Link>
    </div>
  );
};

export default Index;

