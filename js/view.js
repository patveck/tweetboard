/**
 * view.js: User interface of the Tweetboard Web Interface
 * 
 * @author Pascal van Eck
 * 
 */

define(["jquery", "hcharts", "highcharts_uttheme", "gadget"],
    /**
     * Module defining a singleton that serves as the Javascript representation
     * of the Tweetboard web interface UI. This singleton is responsible for 
     * initializing and maintaining the view model (as known from the
     * MVVM design pattern)
     * 
     * @exports view
     */
    function($, hc, hct, jasmine) {
        "use strict";

        var view = {

            /**
             * Create the View singleton (factory). 
             *
             * @function
             * @memberof module:view
             */
            factory: function() {
                /* The ViewModel: */
                this.chartViews = [];
                this.monitorView = null;
                this.messageView = null;
                this.alertViews = [];
                this.highchartsOptions = hc.setOptions(hct);
                return this;
            },

            /**
             * Create a monitor gadget. 
             *
             * There can only be one monitor gadget. If a monitor gadget has
             * already been created, this method does nothing.
             * @param {String} destination Id of the HTML element to which the
             * gadget is appended
             * @method
             * @memberof module:view
             */
            createMonitor: function(destination) {
                if (!this.monitorView) {
                    // TODO: Check whether destination is an empty element:
                    $(destination).addMonitorGadget({
                        id: "monitorGadget",
                        title: "Message monitor"
                    }, function(theMonitor) {
                        this.monitorView = theMonitor;
                    }.bind(this));
                }
            },

            /**
             * Create a messager gadget. 
             *
             * There can only be one messager gadget. If a monitor gadget has
             * already been created, this method does nothing.
             * @param {String} destination Id of the HTML element to which the
             * gadget is appended
             * @param {eventTypes} An array of strings of event types that can
             * be sent by this gadget
             * @param {Function} buttonHandler Callback for the Update button.
             * Called with two string arguments: the event type and data.
             * @method
             * @memberof module:view
             */
            createMessager: function(destination, eventTypes, buttonHandler) {
                if (!this.messageView) {
                    // TODO: Check whether destination is an empty element:
                    $(destination).addMessageGadget(
                        {
                            id: "testGadget",
                            title: "Local test gadget",
                            placeholder:
                                "Event data in JSON notation.",
                            eventTypes: eventTypes
                        },
                        function(theMessage) {
                            this.messageView = theMessage;
                        }.bind(this),
                        function() {
                            console.log("Button of Messager clicked.");
                            buttonHandler(
                                this.messageView.eventType.val(),
                                this.messageView.eventData.val());
                        }.bind(this));
                }
            },
            
            /**
             * 
             * Create an alert gadget.
             * 
             * @param {String} cell Id of the HTML element to which the
             * gadget is appended
             * @param {String} id A string that serves as reference for the
             * gadget that is created
             * @param {String} title Title of the gadget, will be displayed in
             * the gadget's title bar
             * @method
             * @memberof module:view
             */
            createAlerter: function(cell, id, title) {
                if (!this.alertViews[id]) {
                    $(cell).addAlertGadget({
                        id: id,
                        title: title
                    },
                    function(theAlerter) {
                        this.alertViews[id] = theAlerter;
                    }.bind(this));
                }
            },

            
            /**
             * Create a chart gadget. 
             *
             * already been created, this method does nothing.
             * @param {String} cell Id of the HTML element to which the
             * gadget is appended
             * @param {String} id A string that serves as reference for the
             * gadget that is created
             * @param {String} title Title of the gadget, will be displayed in
             * the gadget's title bar
             * @param {Object} options Chart options as required by
             * HighCharts.JS
             * @method
             * @memberof module:view
             */
            createChartGadget: function(cell, id, title, options) {
                // TODO: Check whether destination is an empty element:
                if (!this.alertViews[id]) {
                    $(cell).addChartGadget({
                        id: id,
                        title: title,
                        chartConfig: options
                    }, function(theChart) {
                        this.chartViews[id] = theChart;
                    }.bind(this));
                }
            },
            
            /** 
             * Update an existing chart widget
             * 
             * @param {String} chartOptions Options of new chart as 
             * JSON-formatted string
             * @method
             * @memberof module:view
             */
            updateWidget: function(chartOptions) {
                console.log("Function updateWidget called: " + chartOptions +
                    ".");
                var newOptions = "";
                try {
                    // TODO: check why JSON parsing is needed here:
                    // TODO: change to window.JSON.parse:
                    newOptions = $.parseJSON(chartOptions);
                } catch (e) {
                    alert("parseJSON() raised exception: " +
                        e.toString() + ".");
                }
                // TODO: enable changing any chart, not just the first one:
                var storedDivId = this.chartViews.firstGraph.renderTo.id;
                this.chartViews.firstGraph.destroy();
                if (!("chart" in newOptions)) {
                    newOptions.chart = {renderTo: storedDivId
                    };
                } else {
                    newOptions.chart.renderTo = storedDivId;
                }
                try {
                    this.chartViews.firstGraph = new hc.Chart(
                                    newOptions);
                } catch (e) {
                    alert("HighCharts.Chart() raised exception: " +
                        e.toString() + ".");
                }
            }

        };
        return view;
    });
