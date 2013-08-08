/* global define, describe, it, expect, beforeEach, jasmine */

/**
 * @module viewSpec
 * @author Pascal van Eck
 */

define(["jquery", "view"], function($, view) {
    "use strict";

    describe("Method createMonitor", function() {
        var myView = null;
        var myDiv = null;
        
        beforeEach(function() {
           myView = view.factory();
           myDiv = $("<div>").attr("id", "dest1");
        });
        
        afterEach(function() {
           myDiv.remove();
           myDiv = null;
        });
        
        it("should create a monitor on an empty DIV element", function() {
            expect(myView.monitorView).toBeNull();
            // TODO: also test without hash mark before cell1:
            myView.createMonitor(myDiv);
            expect(myView.monitorView).not.toBeNull();
            // TODO: add more expectations
        });
        
    });
    
    describe("Method createMessager", function() {
        var myView = null;
        var myDiv = null;
        var eventTypes = ["eventType1", "eventType2", "eventType3"];
        var callback = null;
        
        beforeEach(function() {
            myView = view.factory();
            myDiv = $("<div>").attr("id", "dest1");
            callback = jasmine.createSpy("buttonClickCallback");
         });
         
         afterEach(function() {
            myDiv.remove();
            myDiv = null;
         });
         
        it("should create a messager on an empty DIV element", function() {
            var eventTestData = "This is the test data.";
            expect(myView.messageView).toBeNull();
            myView.createMessager(myDiv, eventTypes, callback);
            expect(myView.messageView).not.toBeNull();
            myDiv.find("option[value=eventType1]").prop("selected", true);
            myDiv.find("textarea").val(eventTestData);
            myDiv.find("button").click();
            expect(callback).toHaveBeenCalledWith("eventType1", eventTestData);
        });
    });
});
