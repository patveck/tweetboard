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
            "async":         "../lib/js/async",
            "gmap3":         "../lib/js/gmap3",
			"hcharts":       "../lib/js/highcharts",
			"jasmine":       "../lib/js/jasmine",
			"jasmine-html":  "../lib/js/jasmine-html",
			"jquery":        "../lib/js/jquery-1.8.2.min",
			"jasmine-specs": "../tests/jasmine-specs/",
        },
		"shim": {
            "gmap3": {
                deps: ["jquery",
                  "async!http://maps.googleapis.com/maps/api/js?sensor=false"],
                exports: "$.gmap3"
            },
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