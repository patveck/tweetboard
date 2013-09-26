
// PhantomJS (used in automated tests) doesn't have bind(), so we use the
// following shim, taken from 
// https://github.com/c9/smith/blob/master/tests/public/test.js#L2-L7.
// By putting it here, we ensure that it is only loaded by test code.
Function.prototype.bind = Function.prototype.bind || function (thisp) {
  var fn = this;
  return function () {
    return fn.apply(thisp, arguments);
  };
};

/* jshint -W106 */
var tests = Object.keys(window.__karma__.files).filter(function (file) {
    "use strict";
      return (/Spec\.js$/).test(file);
});
/* jshint +W106 */

requirejs.config({
    // Karma serves files from '/base'
    baseUrl: "/base/js",

    paths: {
    "async":         "../lib/js/async",
    "gmap3":         "../lib/js/gmap3",
    "jqcloud":       "../lib/js/jqcloud-1.0.4",
	"hcharts":       "../lib/js/highcharts",
	"jquery":        "../lib/js/jquery-1.8.2.min"
    },

    shim: {
        "gmap3": {
            deps: ["jquery",
              "async!http://maps.googleapis.com/maps/api/js?sensor=false"],
            exports: "$.gmap3"
        },
        "jqcloud": {
            deps: ["jquery"]
        },
        "hcharts": {
            "deps": ["jquery"],
            "exports": "Highcharts"
                }
    },

    // ask Require.js to load these files (all our tests)
    deps: tests,

    // start test run, once Require.js is done
    /* jshint -W106 */
    callback: window.__karma__.start
    /* jshint +W106 */

});
