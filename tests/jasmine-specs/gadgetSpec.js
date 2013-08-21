/* global define, describe, it, expect, beforeEach, jasmine */

/**
 * @module gadgetSpec
 * @author Pascal van Eck
 */

define(["jquery", "gadget"], function($, gadget) {
    "use strict";

    describe(".addGadget jQuery extension", function() {
        
        it("should set up correct div hierarchy", function() {
          var theDiv = $("<div>");
          var theContents = ["The contents"];
          theDiv.addGadget({"id": "theID", "title": "My title"}, theContents);
          expect(theDiv.children().size()).toEqual(1);
          expect(theDiv.children().attr("id")).toEqual("theID");
          expect(theDiv.children().hasClass("gadget")).toBeTruthy();
          expect(theDiv.children().children().size()).toEqual(2);
          expect(theDiv.children().children().first()
              .hasClass("gadget-title")).toBeTruthy();
          expect(theDiv.children().children().first().text())
              .toEqual("My title");
          expect(theDiv.children().children().last()
              .hasClass("gadget-contents")).toBeTruthy();
          expect(theDiv.children().children().last().text())
              .toEqual("The contents");
        });
        
        it("should fall back gracefully if no id provided", function() {
            var theDiv = $("<div>");
            var theContents = ["The contents"];
            theDiv.addGadget({}, theContents);
            expect(theDiv.children().size()).toEqual(1);
            expect(theDiv.children().attr("id")).toBeUndefined();
            expect(theDiv.children().hasClass("gadget")).toBeTruthy();
            expect(theDiv.children().children().size()).toEqual(2);
            expect(theDiv.children().children().first()
                .hasClass("gadget-title")).toBeTruthy();
            expect(theDiv.children().children().first().text())
                .toEqual("");
            expect(theDiv.children().children().last()
                .hasClass("gadget-contents")).toBeTruthy();
            expect(theDiv.children().children().last().text())
                .toEqual("The contents");
        });
    });
    
    describe(".addMonitorGadget jQuery extension", function() {
        var monitorCallBackMock = null;
        
        beforeEach(function() {
            monitorCallBackMock = jasmine.createSpyObj("monitorCallBackMock",
                ["setMonitor"]);
        });
        
        afterEach(function() {
            monitorCallBackMock = null;
        });
        
        it("should call the second argument exactly once", function() {
            $("<div>").addMonitorGadget({}, function(theMonitor) {
                monitorCallBackMock.setMonitor(theMonitor);
            });
            expect(monitorCallBackMock.setMonitor.calls.length).toEqual(1);
        });
        
        it("should contain a textarea", function() {
            var theDiv = $("<div>");
            theDiv.addMonitorGadget({}, function(theMonitor) {
                monitorCallBackMock.setMonitor(theMonitor);
            });
            expect(theDiv.children().size()).toEqual(1);
            expect(theDiv.children().attr("id")).toBeUndefined();
            expect(theDiv.children().hasClass("gadget")).toBeTruthy();
            expect(theDiv.children().children().size()).toEqual(2);
            expect(theDiv.children().children().first()
                .hasClass("gadget-title")).toBeTruthy();
            expect(theDiv.children().children().first().text())
                .toEqual("");
            expect(theDiv.children().children().last()
                .hasClass("gadget-contents")).toBeTruthy();
            expect(theDiv.children().children().last().children().size())
                .toEqual(1);
            expect(theDiv.children().children().last().children()
                .prop("tagName")).toEqual("TEXTAREA");
        });
        
    });

    describe("AlertGadget jQuery extension", function() {
        var mock = null;
        
        beforeEach(function() {
            mock = jasmine.createSpyObj("mock", ["setAlerter"]);
        });
        
        afterEach(function() {
            mock = null;
        });
        
        it("should call the second argument exactly once", function() {
            $("<div>").addAlertGadget({}, function(theAlerter) {
                mock.setAlerter(theAlerter);
            });
            expect(mock.setAlerter.calls.length).toEqual(1);
        });
        
        it("should set the class of the containing div to alertgadget-cell",
            function() {
            var theDiv = $("<div>");
            theDiv.addAlertGadget({}, function(theAlerter) {
                mock.setAlerter(theAlerter);
            });
            expect(theDiv.hasClass("alertgadget-cell")).toBeTruthy();
        });
        
        it("should contain a div with class alertgadget", function() {
            var theDiv = $("<div>");
            theDiv.addAlertGadget({}, function(theAlerter) {
                mock.setAlerter(theAlerter);
            });
            expect(theDiv.children().size()).toEqual(1);
            expect(theDiv.children().attr("id")).toBeUndefined();
            expect(theDiv.children().hasClass("gadget")).toBeTruthy();
            expect(theDiv.children().children().size()).toEqual(2);
            expect(theDiv.children().children().first()
                .hasClass("gadget-title")).toBeTruthy();
            expect(theDiv.children().children().first().text())
                .toEqual("");
            expect(theDiv.children().children().last()
                .hasClass("gadget-contents")).toBeTruthy();
            expect(theDiv.children().children().last().children().size())
                .toEqual(1);
            var gadgetContents = theDiv.children().children().last()
                .children().first();
            expect(gadgetContents.prop("tagName")).toEqual("DIV");
            expect(gadgetContents.hasClass("alertgadget")).toBeTruthy();
        });
        
        it("newAlert should show an alert", function() {
            var theDiv = $("<div>");
            var alertText = "Behold! This is an alert!";
            var theAlertView = null;
            jasmine.Clock.useMock();
            theDiv.addAlertGadget({}, function(theAlerter) {
                theAlertView = theAlerter;
            });
            theAlertView.newAlert(alertText);
            expect(theDiv.css("visibility")).toEqual("visible");
            expect(parseInt(theDiv.css("height"), 10)).toBeGreaterThan(0);
            var gadgetContents = theDiv.children().children().last()
                .children().first();
            expect(gadgetContents.find(":contains('" + alertText + "')").size())
                .toBeGreaterThan(0);
            jasmine.Clock.tick(7500);
            expect(theDiv.css("visibility")).toEqual("visible");
            expect(parseInt(theDiv.css("height"), 10)).toBeGreaterThan(0);
            jasmine.Clock.tick(1000);
            expect(gadgetContents.find(":contains('" + alertText + "')").size())
            .toEqual(0);
            expect(theDiv.css("visibility")).toEqual("hidden");
            expect(parseInt(theDiv.css("height"), 10)).toEqual(0);
        });
        
        it("newAlert should be able to show alerts together", function() {
            var theDiv = $("<div>");
            var alertText1 = "Alert 1";
            var alertText2 = "Alert 2";
            var alertText3 = "Alert 3";
            var theAlertView = null;
            jasmine.Clock.useMock();
            theDiv.addAlertGadget({}, function(theAlerter) {
                theAlertView = theAlerter;
            });
            theAlertView.newAlert(alertText1);
            theAlertView.newAlert(alertText2);
            jasmine.Clock.tick(4000);
            theAlertView.newAlert(alertText3);
            expect(theDiv.css("visibility")).toEqual("visible");
            expect(parseInt(theDiv.css("height"), 10)).toBeGreaterThan(0);
            var gadgetContents = theDiv.children().children().last()
                .children().first();
            expect(gadgetContents.find(":contains('" + alertText1 + "')")
                .size()).toBeGreaterThan(0);
            expect(gadgetContents.find(":contains('" + alertText2 + "')")
                .size()).toBeGreaterThan(0);
            expect(gadgetContents.find(":contains('" + alertText3 + "')")
                .size()).toBeGreaterThan(0);
            jasmine.Clock.tick(3500);
            expect(theDiv.css("visibility")).toEqual("visible");
            expect(parseInt(theDiv.css("height"), 10)).toBeGreaterThan(0);
            jasmine.Clock.tick(1000);
            expect(gadgetContents.find(":contains('" + alertText1 + "')")
                .size()).toEqual(0);
            expect(gadgetContents.find(":contains('" + alertText2 + "')")
                .size()).toEqual(0);
            expect(gadgetContents.find(":contains('" + alertText3 + "')")
                .size()).toBeGreaterThan(0);
            expect(theDiv.css("visibility")).toEqual("visible");
            expect(parseInt(theDiv.css("height"), 10)).toBeGreaterThan(0);
            jasmine.Clock.tick(4000);
            expect(gadgetContents.find(":contains('" + alertText1 + "')")
                .size()).toEqual(0);
            expect(gadgetContents.find(":contains('" + alertText2 + "')")
                .size()).toEqual(0);
            expect(gadgetContents.find(":contains('" + alertText3 + "')")
                .size()).toEqual(0);
            expect(theDiv.css("visibility")).toEqual("hidden");
            expect(parseInt(theDiv.css("height"), 10)).toEqual(0);
        });
        
    });
    
    describe(".addChartGadget jQuery extension", function() {
        var chartCallbackMock = null;
        
        beforeEach(function() {
            chartCallbackMock = jasmine.createSpyObj("chartCallbackMock",
                ["setChart"]);
            spyOn(console, "error");
        });
        
        afterEach(function() {
            chartCallbackMock = null;
        });
        
        it("should call the second argument exactly once", function() {
            var theDiv = $("<div>");
            $("body").append(theDiv);
            theDiv.addChartGadget({id: "myDiv",
                                   chartConfig: {}}, function(theChart) {
                chartCallbackMock.setChart(theChart);
            });
            expect(chartCallbackMock.setChart.calls.length).toEqual(1);
        });
        
        it("should log an error and not call second argument if no id given",
            function() {
            var theDiv = $("<div>");
            $("body").append(theDiv);
            theDiv.addChartGadget({chartConfig: {}}, function(theChart) {
                chartCallbackMock.setChart(theChart);
            });
            expect(chartCallbackMock.setChart.calls.length).toEqual(0);
            expect(console.error).toHaveBeenCalled();
        });
        
        it("should log an error and not call 2nd arg if chartConfig missing",
            function() {
            $("<div>").addChartGadget({}, function(theChart) {
                chartCallbackMock.setChart(theChart);
            });
            expect(chartCallbackMock.setChart.calls.length).toEqual(0);
            expect(console.error).toHaveBeenCalled();
        });
        
        // The selection is decorated with CSS class "chartgadget-cell", the 
        // gadget contents with CSS class "chartgadget".
        it("should decorate with the specified CSS classes", function() {
            var theDiv = $("<div>");
            theDiv.addChartGadget({id: "myID"}, function(theChart) {
                chartCallbackMock.setChart(theChart);
            });
            expect(theDiv.hasClass("chartgadget-cell")).toBeTruthy();
        });
    });
        
});