webpackHotUpdate("static/development/pages/effect.js",{

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
/* harmony import */ var _babel_runtime_corejs2_helpers_esm_createClass__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @babel/runtime-corejs2/helpers/esm/createClass */ "./node_modules/@babel/runtime-corejs2/helpers/esm/createClass.js");
/* harmony import */ var _babel_runtime_corejs2_helpers_esm_assertThisInitialized__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @babel/runtime-corejs2/helpers/esm/assertThisInitialized */ "./node_modules/@babel/runtime-corejs2/helpers/esm/assertThisInitialized.js");
/* harmony import */ var _babel_runtime_corejs2_helpers_esm_defineProperty__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @babel/runtime-corejs2/helpers/esm/defineProperty */ "./node_modules/@babel/runtime-corejs2/helpers/esm/defineProperty.js");
/* harmony import */ var _babel_runtime_corejs2_helpers_esm_classCallCheck__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @babel/runtime-corejs2/helpers/esm/classCallCheck */ "./node_modules/@babel/runtime-corejs2/helpers/esm/classCallCheck.js");
/* harmony import */ var _babel_runtime_corejs2_helpers_esm_possibleConstructorReturn__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @babel/runtime-corejs2/helpers/esm/possibleConstructorReturn */ "./node_modules/@babel/runtime-corejs2/helpers/esm/possibleConstructorReturn.js");
/* harmony import */ var _babel_runtime_corejs2_helpers_esm_getPrototypeOf__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @babel/runtime-corejs2/helpers/esm/getPrototypeOf */ "./node_modules/@babel/runtime-corejs2/helpers/esm/getPrototypeOf.js");
/* harmony import */ var _babel_runtime_corejs2_helpers_esm_inherits__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @babel/runtime-corejs2/helpers/esm/inherits */ "./node_modules/@babel/runtime-corejs2/helpers/esm/inherits.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! react */ "./node_modules/react/index.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _SwipeableViews_js__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./SwipeableViews.js */ "./pages/SwipeableViews.js");
/* harmony import */ var animated_lib_targets_react_dom__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! animated/lib/targets/react-dom */ "./node_modules/animated/lib/targets/react-dom.js");
/* harmony import */ var animated_lib_targets_react_dom__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(animated_lib_targets_react_dom__WEBPACK_IMPORTED_MODULE_10__);








var _jsxFileName = "/home/vagrant/webstudy/swipe/swipeable-view/pages/effect.js";
var __jsx = react__WEBPACK_IMPORTED_MODULE_8___default.a.createElement;



var styles = {
  slideContainer: {
    height: 400
  },
  slide: {
    //padding: 15,
    minHeight: 400,
    color: '#fff'
  },
  slide1: {
    backgroundColor: '#FEA900'
  },
  slide2: {
    backgroundColor: '#B3DC4A'
  },
  slide3: {
    backgroundColor: '#6AC0FF'
  }
};

var VirticalSwipeView =
/*#__PURE__*/
function (_SwipeableViews) {
  Object(_babel_runtime_corejs2_helpers_esm_inherits__WEBPACK_IMPORTED_MODULE_7__["default"])(VirticalSwipeView, _SwipeableViews);

  function VirticalSwipeView() {
    Object(_babel_runtime_corejs2_helpers_esm_classCallCheck__WEBPACK_IMPORTED_MODULE_4__["default"])(this, VirticalSwipeView);

    return Object(_babel_runtime_corejs2_helpers_esm_possibleConstructorReturn__WEBPACK_IMPORTED_MODULE_5__["default"])(this, Object(_babel_runtime_corejs2_helpers_esm_getPrototypeOf__WEBPACK_IMPORTED_MODULE_6__["default"])(VirticalSwipeView).apply(this, arguments));
  }

  return VirticalSwipeView;
}(_SwipeableViews_js__WEBPACK_IMPORTED_MODULE_9__["default"]);

var albums = [0, 1, 2];

var Effect =
/*#__PURE__*/
function (_React$Component) {
  Object(_babel_runtime_corejs2_helpers_esm_inherits__WEBPACK_IMPORTED_MODULE_7__["default"])(Effect, _React$Component);

  function Effect() {
    var _getPrototypeOf2;

    var _this;

    Object(_babel_runtime_corejs2_helpers_esm_classCallCheck__WEBPACK_IMPORTED_MODULE_4__["default"])(this, Effect);

    for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }

    _this = Object(_babel_runtime_corejs2_helpers_esm_possibleConstructorReturn__WEBPACK_IMPORTED_MODULE_5__["default"])(this, (_getPrototypeOf2 = Object(_babel_runtime_corejs2_helpers_esm_getPrototypeOf__WEBPACK_IMPORTED_MODULE_6__["default"])(Effect)).call.apply(_getPrototypeOf2, [this].concat(args)));

    Object(_babel_runtime_corejs2_helpers_esm_defineProperty__WEBPACK_IMPORTED_MODULE_3__["default"])(Object(_babel_runtime_corejs2_helpers_esm_assertThisInitialized__WEBPACK_IMPORTED_MODULE_2__["default"])(_this), "state", {
      index: 0,
      position: new animated_lib_targets_react_dom__WEBPACK_IMPORTED_MODULE_10___default.a.Value(0)
    });

    Object(_babel_runtime_corejs2_helpers_esm_defineProperty__WEBPACK_IMPORTED_MODULE_3__["default"])(Object(_babel_runtime_corejs2_helpers_esm_assertThisInitialized__WEBPACK_IMPORTED_MODULE_2__["default"])(_this), "handleChangeIndex", function (index) {
      _this.setState({
        index: index
      });
    });

    Object(_babel_runtime_corejs2_helpers_esm_defineProperty__WEBPACK_IMPORTED_MODULE_3__["default"])(Object(_babel_runtime_corejs2_helpers_esm_assertThisInitialized__WEBPACK_IMPORTED_MODULE_2__["default"])(_this), "handleSwitch", function (index, type) {
      if (type === 'end') {
        animated_lib_targets_react_dom__WEBPACK_IMPORTED_MODULE_10___default.a.spring(_this.state.position, {
          toValue: index
        }).start();
        return;
      }

      _this.state.position.setValue(index);
    });

    Object(_babel_runtime_corejs2_helpers_esm_defineProperty__WEBPACK_IMPORTED_MODULE_3__["default"])(Object(_babel_runtime_corejs2_helpers_esm_assertThisInitialized__WEBPACK_IMPORTED_MODULE_2__["default"])(_this), "getstyle", function (i) {
      if (i % 3 == 0) return styles.slide1;else if (i % 3 == 1) return styles.slide2;else return styles.slide3;
    });

    return _this;
  }

  Object(_babel_runtime_corejs2_helpers_esm_createClass__WEBPACK_IMPORTED_MODULE_1__["default"])(Effect, [{
    key: "render",
    value: function render() {
      var _this2 = this;

      var _this$state = this.state,
          index = _this$state.index,
          position = _this$state.position;
      console.log("position = ", position);
      return __jsx(VirticalSwipeView, {
        index: index,
        containerStyle: styles.slideContainer,
        enableMouseEvents: true,
        axis: "y",
        resistance: true,
        onChangeIndex: this.handleChangeIndex,
        onSwitching: this.handleSwitch,
        __source: {
          fileName: _jsxFileName,
          lineNumber: 62
        },
        __self: this
      }, albums.map(function (album, currentIndex) {
        var inputRange = albums.map(function (_, i) {
          return i;
        });
        /*
        */

        var scale = position.interpolate({
          inputRange: inputRange,
          outputRange: inputRange.map(function (i) {
            return currentIndex === i ? 1 : 0.7;
          })
        });
        var opacity = position.interpolate({
          inputRange: inputRange,
          outputRange: inputRange.map(function (i) {
            return currentIndex != i ? 1 : 0.2;
          })
        });
        var translateY = position.interpolate({
          inputRange: inputRange,
          outputRange: inputRange.map(function (i) {
            if (i == currentIndex) return 100 / 2 * (i - currentIndex);else return 100 / 2 * (i - currentIndex);
          })
        });
        console.log("inputRange=", inputRange);
        console.log(translateY);

        var slidestyle = _this2.getstyle(currentIndex);

        return __jsx(animated_lib_targets_react_dom__WEBPACK_IMPORTED_MODULE_10___default.a.div, {
          key: String(currentIndex),
          style: _babel_runtime_corejs2_core_js_object_assign__WEBPACK_IMPORTED_MODULE_0___default()({
            opacity: opacity,
            transform: [{
              scale: scale
            }, {
              translateY: translateY
            }]
          }, styles.slide, slidestyle),
          __source: {
            fileName: _jsxFileName,
            lineNumber: 98
          },
          __self: this
        });
      }));
    }
  }]);

  return Effect;
}(react__WEBPACK_IMPORTED_MODULE_8___default.a.Component);

;
/* harmony default export */ __webpack_exports__["default"] = (Effect);

/***/ })

})
//# sourceMappingURL=effect.js.95d53202f9a586113698.hot-update.js.map