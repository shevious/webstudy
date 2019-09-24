webpackHotUpdate("static/development/pages/coverflow.js",{

/***/ "./pages/coverflow.js":
/*!****************************!*\
  !*** ./pages/coverflow.js ***!
  \****************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _babel_runtime_corejs2_core_js_object_assign__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @babel/runtime-corejs2/core-js/object/assign */ "./node_modules/@babel/runtime-corejs2/core-js/object/assign.js");
/* harmony import */ var _babel_runtime_corejs2_core_js_object_assign__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_babel_runtime_corejs2_core_js_object_assign__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _babel_runtime_corejs2_helpers_esm_classCallCheck__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @babel/runtime-corejs2/helpers/esm/classCallCheck */ "./node_modules/@babel/runtime-corejs2/helpers/esm/classCallCheck.js");
/* harmony import */ var _babel_runtime_corejs2_helpers_esm_createClass__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @babel/runtime-corejs2/helpers/esm/createClass */ "./node_modules/@babel/runtime-corejs2/helpers/esm/createClass.js");
/* harmony import */ var _babel_runtime_corejs2_helpers_esm_possibleConstructorReturn__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @babel/runtime-corejs2/helpers/esm/possibleConstructorReturn */ "./node_modules/@babel/runtime-corejs2/helpers/esm/possibleConstructorReturn.js");
/* harmony import */ var _babel_runtime_corejs2_helpers_esm_getPrototypeOf__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @babel/runtime-corejs2/helpers/esm/getPrototypeOf */ "./node_modules/@babel/runtime-corejs2/helpers/esm/getPrototypeOf.js");
/* harmony import */ var _babel_runtime_corejs2_helpers_esm_assertThisInitialized__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @babel/runtime-corejs2/helpers/esm/assertThisInitialized */ "./node_modules/@babel/runtime-corejs2/helpers/esm/assertThisInitialized.js");
/* harmony import */ var _babel_runtime_corejs2_helpers_esm_inherits__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @babel/runtime-corejs2/helpers/esm/inherits */ "./node_modules/@babel/runtime-corejs2/helpers/esm/inherits.js");
/* harmony import */ var _babel_runtime_corejs2_helpers_esm_defineProperty__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @babel/runtime-corejs2/helpers/esm/defineProperty */ "./node_modules/@babel/runtime-corejs2/helpers/esm/defineProperty.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! react */ "./node_modules/react/index.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var react_swipeable_views__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! react-swipeable-views */ "./node_modules/react-swipeable-views/lib/index.js");
/* harmony import */ var react_swipeable_views__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(react_swipeable_views__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var animated_lib_targets_react_dom__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! animated/lib/targets/react-dom */ "./node_modules/animated/lib/targets/react-dom.js");
/* harmony import */ var animated_lib_targets_react_dom__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(animated_lib_targets_react_dom__WEBPACK_IMPORTED_MODULE_10__);








var _jsxFileName = "/home/vagrant/webstudy/swipe/swipeable-view/pages/coverflow.js";
var __jsx = react__WEBPACK_IMPORTED_MODULE_8___default.a.createElement;



var styles = {
  root: {
    background: '#000',
    padding: '0 50px'
  },
  slide: {
    padding: '24px 16px',
    color: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    flexDirection: 'column',
    display: 'flex'
  },
  img: {
    width: 180,
    height: 180,
    display: 'block',
    marginBottom: 16
  }
};
var albums = [{
  name: 'Abbey Road',
  src: 'https://react-swipeable-views.com/static/album-art-1.jpg'
}, {
  name: 'Bat Out of Hell',
  src: 'https://react-swipeable-views.com/static/album-art-2.jpg'
}, {
  name: 'Homogenic',
  src: 'https://react-swipeable-views.com/static/album-art-3.jpg'
}, {
  name: 'Number of the Beast',
  src: 'https://react-swipeable-views.com/static/album-art-4.jpg'
}, {
  name: "It's Blitz",
  src: 'https://react-swipeable-views.com/static/album-art-5.jpg'
}, {
  name: 'The Man-Machine',
  src: 'https://react-swipeable-views.com/static/album-art-6.jpg'
}, {
  name: 'The Score',
  src: 'https://react-swipeable-views.com/static/album-art-7.jpg'
}, {
  name: 'Lost Horizons',
  src: 'https://react-swipeable-views.com/static/album-art-8.jpg'
}];

var DemoCoverflow =
/*#__PURE__*/
function (_React$Component) {
  Object(_babel_runtime_corejs2_helpers_esm_inherits__WEBPACK_IMPORTED_MODULE_6__["default"])(DemoCoverflow, _React$Component);

  function DemoCoverflow() {
    var _getPrototypeOf2;

    var _this;

    Object(_babel_runtime_corejs2_helpers_esm_classCallCheck__WEBPACK_IMPORTED_MODULE_1__["default"])(this, DemoCoverflow);

    for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }

    _this = Object(_babel_runtime_corejs2_helpers_esm_possibleConstructorReturn__WEBPACK_IMPORTED_MODULE_3__["default"])(this, (_getPrototypeOf2 = Object(_babel_runtime_corejs2_helpers_esm_getPrototypeOf__WEBPACK_IMPORTED_MODULE_4__["default"])(DemoCoverflow)).call.apply(_getPrototypeOf2, [this].concat(args)));

    Object(_babel_runtime_corejs2_helpers_esm_defineProperty__WEBPACK_IMPORTED_MODULE_7__["default"])(Object(_babel_runtime_corejs2_helpers_esm_assertThisInitialized__WEBPACK_IMPORTED_MODULE_5__["default"])(_this), "state", {
      index: 0,
      position: new animated_lib_targets_react_dom__WEBPACK_IMPORTED_MODULE_10___default.a.Value(0)
    });

    Object(_babel_runtime_corejs2_helpers_esm_defineProperty__WEBPACK_IMPORTED_MODULE_7__["default"])(Object(_babel_runtime_corejs2_helpers_esm_assertThisInitialized__WEBPACK_IMPORTED_MODULE_5__["default"])(_this), "handleChangeIndex", function (index) {
      _this.setState({
        index: index
      });
    });

    Object(_babel_runtime_corejs2_helpers_esm_defineProperty__WEBPACK_IMPORTED_MODULE_7__["default"])(Object(_babel_runtime_corejs2_helpers_esm_assertThisInitialized__WEBPACK_IMPORTED_MODULE_5__["default"])(_this), "handleSwitch", function (index, type) {
      if (type === 'end') {
        animated_lib_targets_react_dom__WEBPACK_IMPORTED_MODULE_10___default.a.spring(_this.state.position, {
          toValue: index
        }).start();
        return;
      }

      _this.state.position.setValue(index);
    });

    return _this;
  }

  Object(_babel_runtime_corejs2_helpers_esm_createClass__WEBPACK_IMPORTED_MODULE_2__["default"])(DemoCoverflow, [{
    key: "render",
    value: function render() {
      var _this$state = this.state,
          index = _this$state.index,
          position = _this$state.position;
      return __jsx(react_swipeable_views__WEBPACK_IMPORTED_MODULE_9___default.a, {
        index: index,
        style: styles.root,
        onChangeIndex: this.handleChangeIndex,
        onSwitching: this.handleSwitch,
        enableMouseEvents: true,
        __source: {
          fileName: _jsxFileName,
          lineNumber: 83
        },
        __self: this
      }, albums.map(function (album, currentIndex) {
        var inputRange = albums.map(function (_, i) {
          return i;
        });
        var scale = position.interpolate({
          inputRange: inputRange,
          outputRange: inputRange.map(function (i) {
            return currentIndex === i ? 1 : 0.7;
          })
        });
        var opacity = position.interpolate({
          inputRange: inputRange,
          outputRange: inputRange.map(function (i) {
            return currentIndex === i ? 1 : 0.3;
          })
        });
        var translateX = position.interpolate({
          inputRange: inputRange,
          outputRange: inputRange.map(function (i) {
            return 100 / 2 * (i - currentIndex);
          })
        });
        return __jsx(animated_lib_targets_react_dom__WEBPACK_IMPORTED_MODULE_10___default.a.div, {
          key: String(currentIndex),
          style: _babel_runtime_corejs2_core_js_object_assign__WEBPACK_IMPORTED_MODULE_0___default()({
            opacity: opacity,
            transform: [{
              scale: scale
            }, {
              translateX: translateX
            }]
          }, styles.slide),
          __source: {
            fileName: _jsxFileName,
            lineNumber: 112
          },
          __self: this
        }, __jsx("img", {
          style: styles.img,
          src: album.src,
          alt: "cover",
          __source: {
            fileName: _jsxFileName,
            lineNumber: 122
          },
          __self: this
        }), album.name);
      }));
    }
  }]);

  return DemoCoverflow;
}(react__WEBPACK_IMPORTED_MODULE_8___default.a.Component);

/* harmony default export */ __webpack_exports__["default"] = (DemoCoverflow);

/***/ })

})
//# sourceMappingURL=coverflow.js.fefac3c3c9f82d385cb7.hot-update.js.map