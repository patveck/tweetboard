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
        var mock = null;
        
        beforeEach(function() {
          mock = jasmine.createSpyObj("mock", ["setMonitor"]);
        });
        
        it("should call the second argument", function() {
            $("<div>").addMonitorGadget({}, function(theMonitor) {
                mock.setMonitor(theMonitor); });
            expect(mock.setMonitor).toHaveBeenCalled();
        });
        
        it("should contain a textarea", function() {
            var theDiv = $("<div>");
            theDiv.addMonitorGadget({}, function(theMonitor) {
                mock.setMonitor(theMonitor); });
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
        
});