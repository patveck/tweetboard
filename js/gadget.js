/**
 * Gadget.js: jQuery plugins to render gadgets.
 * 
 * @author Pascal van Eck
 * 
 */

define(["jquery", "hcharts"],
    /**
     * Module containing a number of jQuery plugins.
     * 
     * Remember that jQuery plugins (in contrast to jQueryUI plugins) cannot 
     * maintain state. Instead, we bind the gadget to a calling component
     * using callbacks. In terms of the MVVM pattern, these jQuery plugins are
     * proper views, the calling component plays the role of viewmodel.
     * @exports gadget
     * 
     */
    function($, hc) {

    "use strict";
	
	/** 
	 * Create a general gadget and append it to a given element. Expects an 
	 * options object with "id" and "title" keys.
	 * 
	 * Creates a set of hierarchically nested div elements that can be styled
	 * with CSS to look like a gadget. At the deepest level, the elements of
	 * array contents is appended, element by element. Can be chained.
	 * @function addGadget
	 * @param {Object} options Settings object with "id" and "title" keys
	 * @param {Array} contents Contents of the gadget
	 * @memberof module:gadget
	 */
	$.fn.addGadget = function(options, contents) {
		var theGadget = $("<div>").attr("id", options.id).addClass("gadget");
		var theTitle = $("<div>").addClass("gadget-title").text(options.title);
		var theContents = $("<div>").addClass("gadget-contents");
		contents.forEach(function(contentsItem) {
            theContents.append(contentsItem);
		});
		theGadget.append(theTitle);
		theGadget.append(theContents);
		this.append(theGadget);
		return this;
	};
	
	/* jshint -W110 */
	
    /** 
     * Create a gadget containing a chart from the HighCharts library. 
     * 
     * Expects an options object with "id" and "title" keys.
     * Creates a set of hierarchically nested div elements that can be styled
     * with CSS to look like a gadget. At the deepest level, the elements of
     * array contents is appended, element by element. Can be chained.
     * @function addChartGadget
     * @param {Object} options Settings object with "id" and "title" keys
     * @param {Function} callback to establish binding
     * @memberof module:gadget
     */
	$.fn.addChartGadget = function(options, addToModel) {
        var contents = [];
        contents[0] = $('<div> style="width:100%; height:400px;"').attr("id",
                options.id+"Div");
		this.addGadget(options, contents);
		// TODO: check if keys exist
        options.chartConfig.chart.renderTo = options.id + "Div";
		addToModel(new hc.Chart(options.chartConfig));
		return this;
	};
	
	$.fn.addMessageGadget = function(options, addToModel, clickCallBack) {
		var contents = [];
		contents[0] = $('<textarea placeholder="' + options.placeholder +
                        '"></textarea>');
		contents[1] = $('<br>');
		contents[3] = $('<button type="button">Update</button>').click(
            clickCallBack);
		this.addGadget(options, contents);
		addToModel(contents[0]);
		return this;
	};
	
	$.fn.addMonitorGadget = function(options, addToModel) {
        var contents = [];
        contents[0] = $('<textarea id="txMessages" rows="20" width="100%">' +
                        '</textarea>');
		this.addGadget(options, contents);
		addToModel(contents[0]);
		return this;
	};
	
});