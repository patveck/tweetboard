/**
 * 
 */

define(["jquery", "hcharts", "highcharts_uttheme", "jasmine-html"], function($, hc, hct, jasmine) {
	"use strict";

	var chart1; 
	$(function () { 

		var jasmineEnv = jasmine.getEnv();
		jasmineEnv.updateInterval = 1000;

		var htmlReporter = new jasmine.HtmlReporter();

		jasmineEnv.addReporter(htmlReporter);

		jasmineEnv.specFilter = function(spec) {
			return htmlReporter.specFilter(spec);
		};

		$('#btRunJasmineTests').click(function() {
			require(["jasmine-specs/UTThemeSpec"], function(specs) {
				jasmineEnv.execute();
			});
		}); 

		$('#btUpdateWidgetButton').click(function() {
			console.log("Button btUpdateWidgetButton clicked");
			var newOptions = '';
			var theText = $('#txUpdateWidgetText').val();
			try {
				newOptions = $.parseJSON(theText);
			} catch(e) {
				alert("parseJSON() raised exception: " + e.toString() + ".");
			}
			chart1.destroy();
			try {
				chart1 = new Highcharts.Chart(newOptions);
			} catch(e) {
				alert("HighCharts.Chart() raised exception: " + e.toString() + ".");
			}
		});

		// Apply the theme
		var highchartsOptions = hc.setOptions(hct);

		chart1 = new hc.Chart({
			chart: {
				type: 'spline',
				renderTo: 'chart1',
				animation: Highcharts.svg
			},
			title: {
				text: 'Live random data'
			},
			xAxis: {
				type: 'datetime',
				tickPixelInterval: 150
			},
			yAxis: {
				title: {
					text: 'Value'
				},
				plotLines: [{
					value: 0,
					width: 1,
					color: '#808080'
				}]
			},
			series: [{
				name: 'Random data',
				data: (function() {
					// generate an array of random data
					var data = [],
					time = (new Date()).getTime(),
					i;

					for (i = -19; i <= 0; i++) {
						data.push({
							x: time + i * 1000,
							y: Math.random()
						});
					}
					return data;
				})()
			}]
		});
		if (!!window.EventSource) {
			var source = new EventSource('events');
		} else {
			// Result to xhr polling :(
		}
		source.addEventListener('message', function(e) {
			console.log("message event:" + e.data);
			$('#txMessages').append("message event:" + e.data + "\n");
		}, false);
		source.addEventListener('addpoint', function(e) {
			var newXY;
			console.log("addpoint event:" + e.data);
			$('#txMessages').append("addpoint event:" + e.data + "\n");
			try {
				newXY = $.parseJSON(e.data);
			} catch(e) {
				alert("parseJSON() raised exception: " + e.toString() + ".");
			}
			chart1.series[0].addPoint([newXY["X"], newXY["Y"]], true, true);
		}, false);    
		source.addEventListener('open', function(e) {
			console.log("EventSource connection opened.");
			$('#txMessages').append("EventSource connection opened.\n");
		}, false);
		source.addEventListener('error', function(e) {
			if (e.readyState == EventSource.CLOSED) {
				console.log("EventSource connection closed.");
				$('#txMessages').append("EventSource connection closed.\n");
			} else {
				console.log("EventSource error");
				$('#txMessages').append("EventSource error.\n");
			}
		}, false);
	});

});
