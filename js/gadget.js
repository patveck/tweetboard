/**
 * @module gadget
 */

define(["jquery", "hcharts"], function($, hc) {
	"use strict";
	
	$.fn.addGadget = function(options) {
		var theGadget = $("<div>").attr("id", options.id).addClass("gadget");
		var theTitle = $("<div>").addClass("gadget-title").text(options.title);
		var theContents = $("<div>").addClass("gadget-contents").append(options.callback(this)); 
		theGadget.append(theTitle);
		theGadget.append(theContents);
		this.append(theGadget);
		return this;
	};
	
	$.fn.addChartGadget = function(options) {
		var theChart = $('<div> style="width:100%; height:400px;"').highcharts(options.chartConfig);
		options.contents = theChart;
		this.addGadget(options);
		return this;
	};
	
	$.fn.addMessageGadget = function(options) {
		options.callback = function(sel) {
			var theTextarea = $('<textarea rows="20" width="100%">');
			var theButton = $("<button>").click(function() {});
			sel.append($('<textarea id="txUpdateWidgetText"placeholder="HighCharts options object in JSON notation."></textarea>'));
			sel.append($('<br>'));
			sel.append($)
		};
		options.contents = '<button id="btUpdateWidgetButton" type="button">Update</button>';
		this.addGadget(options);
		
		return this;
	};
	
	$.fn.addMonitorGadget = function(options) {
		options.contents = '<textarea id="txMessages" rows="20" width="100%"></textarea>';
		this.addGadget(options);
		return this;
	};
	
});