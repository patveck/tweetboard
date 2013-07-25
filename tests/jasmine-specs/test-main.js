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
	"hcharts":       "../lib/js/highcharts",
	"jquery":        "../lib/js/jquery-1.8.2.min"
    },

    shim: {
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
