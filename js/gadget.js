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
	};
	
	$.fn.addChartGadget = function(options, ref) {
		options.callback = function(sel) {
            return $('<div> style="width:100%; height:400px;"').attr("id", options.id+"Div");
		};
		this.addGadget(options);
		return new hc.Chart(options.chartConfig);
	};
	
	$.fn.addMessageGadget = function(options) {
		options.callback = function(sel) {
			return $('<textarea id="txUpdateWidgetText"placeholder="HighCharts options object in JSON notation."></textarea>').append($('<br>')).append($('<button id="btUpdateWidgetButton" type="button">Update</button>'));
		};
		this.addGadget(options);
	};
	
	$.fn.addMonitorGadget = function(options, ref) {
        options.callback = function(sel) {
            var theTextArea = $('<textarea id="txMessages" rows="20" width="100%"></textarea>');
            ref.monitors[options.id] = theTextArea;
            return theTextArea;
        };
		this.addGadget(options);
	};
	
});