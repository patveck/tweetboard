/* jshint undef: true, unused: true */
/* global define, describe, it, expect */

/**
 * @module UTThemeSpec
 * @author Pascal van Eck
 */

define(["highcharts_uttheme"], function(hct) {
	"use strict";
	describe("Dashboard has UT theme (highcharts_uttheme)", function() {
		// Testing just one aspect of the UT theme to see if options object was set.
		it("should have UT green as first color", function() {
			expect(hct.colors[0]).toEqual("#3F9C35");
		});
	});
});