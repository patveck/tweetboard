/**
 * @author patveck
 */

define(["jquery", "hcharts", "highcharts_uttheme", "jasmine-html"],
    function($, hc, hct, jasmine) {
        "use strict";

        /** @exports main */
        var main = {
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

            /* The ViewModel: */
            source: null,
            chartViews: [],
            monitorView: null,
            messageView: null,
            
            eventTypes: ["buildInfo", "message", "addpoint", "open", "error"],

            highchartsOptions: hc.setOptions(hct), // Apply the theme

            jasmineEnv: jasmine.getEnv(),
            htmlReporter: new jasmine.HtmlReporter(),

            /** @method */
            updateWidget: function(theText) {
                console.log("Function updateWidget called: " + theText + ".");
                var newOptions = "";
                try {
                    newOptions = $.parseJSON(theText);
                } catch (e) {
                    alert("parseJSON() raised exception: " +
                        e.toString() + ".");
                }
                var storedDivId = this.chartViews.firstGraph.renderTo.id;
                this.chartViews.firstGraph.destroy();
                if (!("chart" in newOptions)) {
                    newOptions.chart = {renderTo: storedDivId
                    };
                } else {
                    newOptions.chart.renderTo = storedDivId;
                }
                try {
                    this.chartViews.firstGraph = new Highcharts.Chart(
                                    newOptions);
                } catch (e) {
                    alert("HighCharts.Chart() raised exception: " +
                        e.toString() + ".");
                }
            },

            createMonitor: function(destination) {
                if (!this.monitorView) {
                    $(destination).addMonitorGadget({
                        id: "monitorGadget",
                        title: "Message monitor"
                    }, function(theMonitor) {
                        this.monitorView = theMonitor;
                    }.bind(this));
                }
            },

            handleLocalMessage: function(eventType, eventData) {
                var event = $.Event(eventType);
                event.data = eventData;
                this.handleEvent(event);
            },
            
            createMessager: function(destination) {
                if (!this.messageView) {
                    $(destination).addMessageGadget(
                        {
                            id: "testGadget",
                            title: "Local test gadget",
                            placeholder:
                                "Event data in JSON notation.",
                            eventTypes: this.eventTypes,
                        },
                        function(theMessage) {
                            this.messageView = theMessage;
                        }.bind(this),
                        function() {
                            console.log("Button of Messager clicked.");
                            this.handleLocalMessage(
                                this.messageView.eventType.val(),
                                this.messageView.eventData.val());
                        }.bind(this));
                }
            },

            createChartGadget: function(destination) {
                $(destination).addChartGadget({
                    id: "firstGraph",
                    title: "The first chart",
                    chartConfig: this.tmp
                }, function(theChart) {
                    this.chartViews.firstGraph = theChart;
                }.bind(this));
            },

            run: function() {
                /* Initialize Jasmine JavaScript test runner: */
                this.jasmineEnv.updateInterval = 1000;
                this.jasmineEnv.addReporter(this.htmlReporter);
                this.jasmineEnv.specFilter = function(spec) {
                    return this.htmlReporter.specFilter(spec);
                }.bind(this);
                $("#btRunJasmineTests").click(
                    function() {
                        require([
                            "jasmine-html", "jasmine-specs/UTThemeSpec",
                            "jasmine-specs/gadgetSpec"], function() {
                            jasmine.getEnv().execute();
                        });
                    });

                this.createChartGadget("#cell1");
                this.createMessager("#cell2");
                this.createMonitor("#cell3");

                /* Initialize eventsource component: */
                this.source = new EventSource("events");
                this.eventTypes.forEach(
                    function(eventType) {
                        console.log("Initializing event type " + eventType +
                            ".");
                        this.initEventSource(eventType);
                    }, this);
            },
            
            buildInfoEventReceived: function(event, data) {
                $("#buildinfo").append("This is tweetboard, branch " +
                    data.branch + ", commit " + data.commit + ".<br>");
            },

            messageEventReceived: function(event, data) {
                console.log("message event:" + data);
                this.monitorView.append("message event:" + data + "\n");
            },

            addpointEventReceived: function(event, data) {
                this.chartViews.firstGraph.series[0].addPoint([
                    data.X, data.Y], true, true);
            },

            errorEventReceived: function(event, data) {
                if (e.readyState == EventSource.CLOSED) {
                    console.log("EventSource connection closed.");
                    this.monitorView.append("EventSource connection closed.\n");
                } else {
                    console.log("EventSource error");
                    this.monitorView.append("EventSource error.\n");
                }
            },

            openEventReceived: function(event, data) {
                console.log("EventSource connection opened.");
                this.monitorView.append("EventSource connection opened.\n");
            },
            
            handleEvent: function(event) {
                var logMessage = "EventSource: message received, type is " +
                    event.type + ", data is " + event.data + ".";
                console.log(logMessage);
                this.monitorView.append(logMessage + "\n");
                var handlerName = event.type + "EventReceived";
                if (typeof this[handlerName] !== "undefined") {
                    var parsedData = {};
                    try {
                        if (typeof event.data !== "undefined") {
                            parsedData = window.JSON.parse(event.data);
                        }
                    } catch (e) {
                        alert("parseJSON() raised exception: " +
                            e.toString() + ".");
                    }
                    this[handlerName].call(this, event, parsedData);
                } else {
                    console.log("No handler for event " + event.type + ".");
                }
            },

            initEventSource: function(eventType) {
                this.source.addEventListener(eventType,
                    (this.handleEvent).bind(this), false);
            }
        };
        return main;
    });
