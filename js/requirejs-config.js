/**
 * Settings for requirejs. Mainly needed to accommodate libraries (jquery, 
 * jasmine, highcharts) that are not requirejs-compliant.
 * 
 */

(function() {
	"use strict";
	
	requirejs.config({
		"baseUrl": "js",
		"paths": {
			"hcharts":       "../lib/js/highcharts",
			"jasmine":       "../lib/js/jasmine",
			"jasmine-html":  "../lib/js/jasmine-html",
			"jquery":        "../lib/js/jquery-1.8.2.min",
			"jasmine-specs": "../tests/jasmine-specs/"
		},
		"shim": {
			"jasmine": {
				exports: "jasmine"
			},
			"jasmine-html": {
				deps: ["jasmine"],
				exports: "jasmine"
			},
			"hcharts": {
				"deps": ["jquery"],
				"exports": "Highcharts"
			}
		}
	});
}());