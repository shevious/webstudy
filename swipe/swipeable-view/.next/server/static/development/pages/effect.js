module.exports =
/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = require('../../../ssr-module-cache.js');
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		var threw = true;
/******/ 		try {
/******/ 			modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/ 			threw = false;
/******/ 		} finally {
/******/ 			if(threw) delete installedModules[moduleId];
/******/ 		}
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 3);
/******/ })
/************************************************************************/
/******/ ({

/***/ "./node_modules/@babel/runtime-corejs2/core-js/object/assign.js":
/*!**********************************************************************!*\
  !*** ./node_modules/@babel/runtime-corejs2/core-js/object/assign.js ***!
  \**********************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! core-js/library/fn/object/assign */ "core-js/library/fn/object/assign");

/***/ }),

/***/ "./node_modules/@babel/runtime-corejs2/core-js/object/define-property.js":
/*!*******************************************************************************!*\
  !*** ./node_modules/@babel/runtime-corejs2/core-js/object/define-property.js ***!
  \*******************************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! core-js/library/fn/object/define-property */ "core-js/library/fn/object/define-property");

/***/ }),

/***/ "./node_modules/@babel/runtime-corejs2/helpers/esm/defineProperty.js":
/*!***************************************************************************!*\
  !*** ./node_modules/@babel/runtime-corejs2/helpers/esm/defineProperty.js ***!
  \***************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return _defineProperty; });
/* harmony import */ var _core_js_object_define_property__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../core-js/object/define-property */ "./node_modules/@babel/runtime-corejs2/core-js/object/define-property.js");
/* harmony import */ var _core_js_object_define_property__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_core_js_object_define_property__WEBPACK_IMPORTED_MODULE_0__);

function _defineProperty(obj, key, value) {
  if (key in obj) {
    _core_js_object_define_property__WEBPACK_IMPORTED_MODULE_0___default()(obj, key, {
      value: value,
      enumerable: true,
      configurable: true,
      writable: true
    });
  } else {
    obj[key] = value;
  }

  return obj;
}

/***/ }),

/***/ "./pages/effect.js":
/*!*************************!*\
  !*** ./pages/effect.js ***!
  \*************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _babel_runtime_corejs2_core_js_object_assign__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @babel/runtime-corejs2/core-js/object/assign */ "./node_modules/@babel/runtime-corejs2/core-js/object/assign.js");
/* harmony import */ var _babel_runtime_corejs2_core_js_object_assign__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_babel_runtime_corejs2_core_js_object_assign__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _babel_runtime_corejs2_helpers_esm_defineProperty__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @babel/runtime-corejs2/helpers/esm/defineProperty */ "./node_modules/@babel/runtime-corejs2/helpers/esm/defineProperty.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react_swipeable_views__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react-swipeable-views */ "react-swipeable-views");
/* harmony import */ var react_swipeable_views__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react_swipeable_views__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var animated_lib_targets_react_dom__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! animated/lib/targets/react-dom */ "animated/lib/targets/react-dom");
/* harmony import */ var animated_lib_targets_react_dom__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(animated_lib_targets_react_dom__WEBPACK_IMPORTED_MODULE_4__);


var _jsxFileName = "/home/vagrant/webstudy/swipe/swipeable-view/pages/effect.js";
var __jsx = react__WEBPACK_IMPORTED_MODULE_2___default.a.createElement;
 //import SwipeableViews from './SwipeableViews.js';



const styles = {
  root: {
    background: '#000',
    padding: '0px 0px'
  },
  slideContainer: {
    height: 400,
    padding: '0px 0px'
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
    height: 400
  },
  slide1: {
    backgroundColor: '#FEA900'
  },
  slide2: {
    backgroundColor: '#B3DC4A'
  },
  slide3: {
    backgroundColor: '#6AC0FF'
  },
  img: {
    width: 400,
    height: 250,
    display: 'block',
    marginBottom: 16
  }
};

class VirticalSwipeView extends react_swipeable_views__WEBPACK_IMPORTED_MODULE_3___default.a {}

const albums = [{
  name: 'Abbey Road',
  src: 'https://react-swipeable-views.com/static/album-art-1.jpg'
}, {
  name: 'Bat Out of Hell',
  src: 'https://react-swipeable-views.com/static/album-art-2.jpg'
}, {
  name: 'Homogenic',
  src: 'https://react-swipeable-views.com/static/album-art-3.jpg'
}];

class Effect extends react__WEBPACK_IMPORTED_MODULE_2___default.a.Component {
  constructor(...args) {
    super(...args);

    Object(_babel_runtime_corejs2_helpers_esm_defineProperty__WEBPACK_IMPORTED_MODULE_1__["default"])(this, "state", {
      index: 0,
      position: new animated_lib_targets_react_dom__WEBPACK_IMPORTED_MODULE_4___default.a.Value(0)
    });

    Object(_babel_runtime_corejs2_helpers_esm_defineProperty__WEBPACK_IMPORTED_MODULE_1__["default"])(this, "handleChangeIndex", index => {
      this.setState({
        index
      });
    });

    Object(_babel_runtime_corejs2_helpers_esm_defineProperty__WEBPACK_IMPORTED_MODULE_1__["default"])(this, "handleSwitch", (index, type) => {
      if (type === 'end') {
        animated_lib_targets_react_dom__WEBPACK_IMPORTED_MODULE_4___default.a.timing(this.state.position, {
          toValue: index
        }).start();
        return;
      }

      this.state.position.setValue(index);
    });

    Object(_babel_runtime_corejs2_helpers_esm_defineProperty__WEBPACK_IMPORTED_MODULE_1__["default"])(this, "getstyle", i => {
      if (i % 3 == 0) return styles.slide1;else if (i % 3 == 1) return styles.slide2;else return styles.slide3;
    });
  }

  /* containerStyle={styles.slideContainer} */
  render() {
    const {
      index,
      position
    } = this.state;
    console.log("position = ", position);
    return __jsx(VirticalSwipeView, {
      index: index,
      style: styles.root,
      containerStyle: styles.slideContainer,
      enableMouseEvents: true,
      axis: "y",
      onChangeIndex: this.handleChangeIndex,
      onSwitching: this.handleSwitch,
      __source: {
        fileName: _jsxFileName,
        lineNumber: 94
      },
      __self: this
    }, albums.map((album, currentIndex) => {
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
        })
      });
      const opacity = position.interpolate({
        inputRange,
        outputRange: inputRange.map(i => {
          if (currentIndex == this.state.index) return currentIndex == i ? 1 : 0.3;else //return currentIndex == i ? 1 : 0.3;
            return 1;
        })
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
            if (i == currentIndex) return 0;else if (i > currentIndex) return 200;else return -200;
          } else {
            if (i == currentIndex) return 0;else if (i > currentIndex) return 200;else return -200;
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

        })
      });
      console.log("inputRange=", inputRange); //console.log(translateY);

      const slidestyle = this.getstyle(currentIndex);
      console.log(album.src);
      return __jsx(animated_lib_targets_react_dom__WEBPACK_IMPORTED_MODULE_4___default.a.div, {
        key: String(currentIndex),
        style: _babel_runtime_corejs2_core_js_object_assign__WEBPACK_IMPORTED_MODULE_0___default()({
          opacity,
          transform: [{
            scale
          }, {
            translateY
          }]
        }, styles.slide, slidestyle),
        __source: {
          fileName: _jsxFileName,
          lineNumber: 196
        },
        __self: this
      }, __jsx("img", {
        style: styles.img,
        src: album.src,
        alt: "cover",
        __source: {
          fileName: _jsxFileName,
          lineNumber: 207
        },
        __self: this
      }), __jsx("p", {
        __source: {
          fileName: _jsxFileName,
          lineNumber: 208
        },
        __self: this
      }, album.name), __jsx("p", {
        __source: {
          fileName: _jsxFileName,
          lineNumber: 211
        },
        __self: this
      }, album.name));
    }));
  }

}

;
/* harmony default export */ __webpack_exports__["default"] = (Effect);

/***/ }),

/***/ 3:
/*!*******************************!*\
  !*** multi ./pages/effect.js ***!
  \*******************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! /home/vagrant/webstudy/swipe/swipeable-view/pages/effect.js */"./pages/effect.js");


/***/ }),

/***/ "animated/lib/targets/react-dom":
/*!*************************************************!*\
  !*** external "animated/lib/targets/react-dom" ***!
  \*************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = require("animated/lib/targets/react-dom");

/***/ }),

/***/ "core-js/library/fn/object/assign":
/*!***************************************************!*\
  !*** external "core-js/library/fn/object/assign" ***!
  \***************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = require("core-js/library/fn/object/assign");

/***/ }),

/***/ "core-js/library/fn/object/define-property":
/*!************************************************************!*\
  !*** external "core-js/library/fn/object/define-property" ***!
  \************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = require("core-js/library/fn/object/define-property");

/***/ }),

/***/ "react":
/*!************************!*\
  !*** external "react" ***!
  \************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = require("react");

/***/ }),

/***/ "react-swipeable-views":
/*!****************************************!*\
  !*** external "react-swipeable-views" ***!
  \****************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = require("react-swipeable-views");

/***/ })

/******/ });
//# sourceMappingURL=effect.js.map