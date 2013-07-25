/* global define, describe, it, expect, beforeEach, jasmine */

/**
 * @module gadgetSpec
 * @author Pascal van Eck
 */

define(["jquery", "gadget"], function($, gadget) {
    "use strict";

    describe(".addMonitorGadget jQuery extension", function() {
        var mock;
        
        beforeEach(function() {
          mock = jasmine.createSpyObj("mock", ["setMonitor"]);
        });
        
        it("should call the second argument", function() {
            $("<div>").addMonitorGadget({}, function(theMonitor) {
                mock.setMonitor(theMonitor); });
            expect(mock.setMonitor).toHaveBeenCalled();
        });
        
    });
        
});