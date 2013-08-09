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

            tmp: {
                chart: {
                    type: "spline",
                    animation: Highcharts.svg
                },
                title: {text: "Live random data"
                },
                xAxis: {
                    type: "datetime",
                    tickPixelInterval: 150
                },
                yAxis: {
                    title: {text: "Value"
                    },
                    plotLines: [{
                        value: 0,
                        width: 1,
                        color: "#808080"
                    }]
                },
                series: [{
                    name: "Random data",
                    data: (function() {
                        // generate an array of random data
                        var data = [], time = (new Date()).getTime(), i;

                        for (i = -19; i <= 0; i++) {
                            data.push({
                                x: time + i * 1000,
                                y: Math.random()
                            });
                        }
                        return data;
                    })()
                }]
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
             * @param {String} destination Id of the HTML element to which the
             * gadget is appended
             * @param {String} id A string that serves as reference for the
             * gadget that is created
             * @method
             * @memberof module:view
             */
            createAlerter: function(destination, id) {
                if (!this.alertViews[id]) {
                    $(destination).addAlertGadget(
                        {
                            id: "alertGadget",
                            title: "Alert!"
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
             * @param {String} destination Id of the HTML element to which the
             * gadget is appended
             * @method
             * @memberof module:view
             */
            createChartGadget: function(destination) {
                // TODO: Check whether destination is an empty element:
                $(destination).addChartGadget({
                    id: "firstGraph",
                    title: "The first chart",
                    chartConfig: this.tmp
                }, function(theChart) {
                    // TODO: Append to chartViews (rather than replace):
                    this.chartViews.firstGraph = theChart;
                }.bind(this));
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
