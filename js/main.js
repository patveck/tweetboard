/**
 * @module main 
 */

define(["jquery", "hcharts", "highcharts_uttheme", "jasmine-html"], function($, hc, hct, jasmine) {
	"use strict";

	return {
		source: null,
		chart1: new hc.Chart({
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
		}),
		
		highchartsOptions: hc.setOptions(hct), // Apply the theme 

		jasmineEnv: jasmine.getEnv(),
		htmlReporter: new jasmine.HtmlReporter(),

		run: function() {
			this.jasmineEnv.updateInterval = 1000;			
			this.jasmineEnv.addReporter(this.htmlReporter);
			this.jasmineEnv.specFilter = $.proxy(function(spec) {
				return this.htmlReporter.specFilter(spec);
			}, this);
			$('#btRunJasmineTests').click(function() {
				require(["jasmine-html", "jasmine-specs/UTThemeSpec"], function(jasmine, spec) { 
					jasmine.getEnv().execute(); });
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
				this.chart1.destroy();
				try {
					this.chart1 = new Highcharts.Chart(newOptions);
				} catch(e) {
					alert("HighCharts.Chart() raised exception: " + e.toString() + ".");
				}
			});
			if (!!window.EventSource) {
				this.source = new EventSource('events');
			} else {
				// Result to xhr polling :(
			}
			this.source.addEventListener('message', function(event) {
				console.log("message event:" + event.data);
				$('#txMessages').append("message event:" + event.data + "\n");
			}, false);
			this.source.addEventListener('addpoint', $.proxy(function(event) {
				var newXY;
				console.log("addpoint event:" + event.data);
				$('#txMessages').append("addpoint event:" + event.data + "\n");
				try {
					newXY = $.parseJSON(event.data);
				} catch(e) {
					alert("parseJSON() raised exception: " + e.toString() + ".");
				}
				this.chart1.series[0].addPoint([newXY.X, newXY.Y], true, true);
			}, this), false);    
			this.source.addEventListener('open', function(event) {
				console.log("EventSource connection opened.");
				$('#txMessages').append("EventSource connection opened.\n");
			}, false);
			this.source.addEventListener('error', function(event) {
				if (e.readyState == EventSource.CLOSED) {
					console.log("EventSource connection closed.");
					$('#txMessages').append("EventSource connection closed.\n");
				} else {
					console.log("EventSource error");
					$('#txMessages').append("EventSource error.\n");
				}
			}, false);

		}
	};
});
