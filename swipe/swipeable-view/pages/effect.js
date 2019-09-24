import React from 'react';
//import SwipeableViews from './SwipeableViews.js';
import SwipeableViews from 'react-swipeable-views';
import Animated from 'animated/lib/targets/react-dom';

const styles = {
  root: {
    background: '#000',
    padding: '0px 0px',
  },
  slideContainer: {
    height: 400,
    padding: '0px 0px',
  },
  slide: {
    //padding: 15,
    //minHeight: 400,
    color: '#fff',
    alignItems: 'center',
    justifyContent: 'top',
    flexDirection: 'column',
    display: 'flex',
    overflow: 'hidden',
    height: 400,
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
  img: {
    width: 400,
    height: 250,
    display: 'block',
    marginBottom: 16,
  },
};

class VirticalSwipeView extends SwipeableViews {
}

const albums = [
  {
    name: 'Abbey Road',
    src: 'https://react-swipeable-views.com/static/album-art-1.jpg',
  },
  {
    name: 'Bat Out of Hell',
    src: 'https://react-swipeable-views.com/static/album-art-2.jpg',
  },
  {
    name: 'Homogenic',
    src: 'https://react-swipeable-views.com/static/album-art-3.jpg',
  },
];

class Effect extends React.Component {
  state = {
    index: 0,
    position: new Animated.Value(0),
  };

  handleChangeIndex = index => {
    this.setState({ index });
  };

  handleSwitch = (index, type) => {
    if (type === 'end') {
      Animated.timing(this.state.position, { toValue: index }).start();
      return;
    }
    this.state.position.setValue(index);
  };

  getstyle = (i) => {
    if (i%3 == 0)
      return styles.slide1;
    else if (i%3 == 1)
      return styles.slide2;
    else
      return styles.slide3;
  }

/* containerStyle={styles.slideContainer} */

  render() {
    const { index, position } = this.state;
    console.log("position = ", position);
    return (
      <VirticalSwipeView
        index={index}
        style={styles.root}
        containerStyle={styles.slideContainer}
        enableMouseEvents axis="y" 
        onChangeIndex={this.handleChangeIndex}
        onSwitching={this.handleSwitch}
      >
        {albums.map((album, currentIndex) => {
          const inputRange = albums.map((_, i) => i);
/*
*/
          console.log("currentIndex=", currentIndex);
          console.log("index=", this.state.index);
          console.log("inputRange=", inputRange);
          const scale = position.interpolate({
            inputRange,
            outputRange: inputRange.map(i => {
              //return currentIndex === i ? 1 : 0.7;
              return 1;
            }),
          });
          const opacity = position.interpolate({
            inputRange,
            outputRange: inputRange.map(i => {
              if (currentIndex == this.state.index)
                return currentIndex == i ? 1 : 0.3;
              else
                //return currentIndex == i ? 1 : 0.3;
                return 1;
            }),
          });
/*
          const height = position.interpolate({
            inputRange,
            outputRange: inputRange.map(i => {
              if (currentIndex == this.state.index) {
                if (i == currentIndex)
                  return 400;
                else
                  return 200;
              } else {
                  return 400;
              }
            }),
          });
*/
          const translateY = position.interpolate({
            inputRange,
            outputRange: inputRange.map(i => {
              if (currentIndex == this.state.index) {
                if (i == currentIndex)
                  return 0;
                else if (i > currentIndex)
                  return 200;
                else 
                  return -200;
              } else {
                if (i == currentIndex)
                  return 0;
                else if (i > currentIndex)
                  return 200;
                else 
                  return -200;
              }
/*
              if (currentIndex == this.state.index) {
                if (i == currentIndex)
                  return 0;
                else if (i < currentIndex)
                  return -400;
                else
                  return 400;
              } else if (currentIndex > this.state.index)
                return 0;
              else 
                return 0;
*/
        
/*
              if (i == this.state.index)
                return 0;
              return -200;
              if (i == currentIndex)
                return 0;
              else if (i < currentIndex)
                return 200;
              else
                return -200;
              if (i == currentIndex)
                return (100 / 2) * (i - currentIndex);
              else
                return 100/2 * (i - currentIndex);
*/
            }),
          });
          console.log("inputRange=",inputRange);
          //console.log(translateY);
          const slidestyle = this.getstyle(currentIndex);

          console.log(album.src);
          return (
            <Animated.div
              key={String(currentIndex)}
              style={Object.assign(
                {
                  opacity,
                  transform: [{ scale }, { translateY }],
                },
                styles.slide,
                slidestyle,
              )}
            >
              <img style={styles.img} src={album.src} alt="cover" />
              <p>
              {album.name} 
              </p>
              <p>
              {album.name} 
              </p>
            </Animated.div>
          );
        })}
      </VirticalSwipeView>
    );
  };
};

export default Effect;

