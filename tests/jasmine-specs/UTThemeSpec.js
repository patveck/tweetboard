/* jshint undef: true, unused: true */
/* global highchartsOptions, describe, it, expect */

describe("Dashboard has UT theme (highcharts_uttheme)", function() {

	"use strict";
	
	// Testing just one aspect of the UT theme to see if options object was set.
	it("should have UT green as first color", function() {
		expect(highchartsOptions.colors[0]).toEqual("#3F9C35");
	});
});