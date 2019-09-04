
$(document).ready(function(){
	// $('#TextSum_and_SA').hide();
	// $('#QA').hide();
	var currentAjax = null;
	$('#analyze').on('click', function(){
		var text = $('#paste_text').val();
		var algorithm = $('.btn-group > button.active')[0].id;
		var percentage = $('.btn-group > button.active')[1].getAttribute("percentage");

		$('#TextSum_and_SA').show();
		$('#QA').show();

		// getSummary(text, algorithm, percentage);
		getSentiment(text);
	});


	$('.btn-group > button').on('click', function(){
		$(this).parent().find('button').removeClass('active');
		$(this).toggleClass('active');

		var text = $('#paste_text').val();
		var algorithm = $('.btn-group > button.active')[0].id;
		var percentage = $('.btn-group > button.active')[1].getAttribute("percentage");

		getSummary(text, algorithm, percentage);
	});

	// 問題回報
	$('#report').on('click', function(){
		history.replaceState(null, "report page", window.location.href);
		window.location.href = 'report.html';
	});



	//**********Function**********//

	var getSummary = function(text, algorithm, percentage){
	stopAjax(currentAjax);

	currentAjax = $.ajax({
		method: "POST",
		url: "../cgi-bin/getSummary.py",
		// async: false, //同步化
		// dataType:"json",
		data: {
			"text" : text,
			"algorithm" : algorithm,
			"percentage" : percentage
		},
		beforeSend:function(){
			$("#summary").val("計算摘要中...");
		},
		success: function(text){
			console.log(text);
			$("#summary").val(text);
		},
		complete:function(){
		}
	});

	function stopAjax(ajax){  
	    //如果ajax未完成，則中止該ajax  
	        if(ajax) {ajax.abort();}  
	    }  
	}

	var getSentiment = function(text, algorithm, percentage){
	stopAjax(currentAjax);

	currentAjax = $.ajax({
		method: "POST",
		url: "../cgi-bin/getSentiment.py",
		// async: false, //同步化
		// dataType:"json",
		data: {
			"text" : text
		},
		beforeSend:function(){
		},
		success: function(text){
			text = text.replace(/'/g,'"');
			console.log(text);
			var senRatio = JSON.parse(text);
			var labels=[],data=[];
			Object.keys(senRatio).forEach(function(key) {
				labels.push(key);
				data.push(senRatio[key]);
			});
			console.log(senRatio);
			var barData = {
				"labels": labels,
				"datasets": [{
					"data": data,
					"fill": false,
					"backgroundColor": ["rgba(255, 99, 132, 0.2)", "rgba(255, 159, 64, 0.5)", "rgba(255, 205, 86, 0.5)", "rgba(75, 192, 192, 0.5)", "rgba(54, 162, 235, 0.5)"],
					"borderColor": ["rgb(255, 99, 132)", "rgb(255, 159, 64)", "rgb(255, 205, 86)", "rgb(75, 192, 192)", "rgb(54, 162, 235)"],
					"borderWidth": 1
				}]
			};
			Chart.defaults.global.legend.display = false;
			Chart.defaults.scale.gridLines.display = false;
			for (var i in barData.labels) {
				var lab = barData.labels[i];
				var $img = $("<img/>").attr("id", lab).attr("src", "../img/" + lab + ".png");
				$("#pics").append($img);
			}
			var originalBarController = Chart.controllers.bar;
			Chart.controllers.bar = Chart.controllers.bar.extend({
				draw: function() {
					originalBarController.prototype.draw.call(this, arguments);
					drawFlags(this);
				}
			});
			function drawFlags(t) {
				var chartInstance = t.chart;
				var dataset = chartInstance.config.data.datasets[0];
				var meta = chartInstance.controller.getDatasetMeta(0);
				var y0 = chartInstance.scales.y0.top + chartInstance.scales.y0.height;
				ctx.save();
				meta.data.forEach(function(bar, index) {
					var lab = bar._model.label;
					var img = document.getElementById(lab);
					ctx.drawImage(img, bar._model.y - 10, x0 - 6, 20, 12);
					ctx.stroke();
				});
				ctx.restore();
			}

			var ctx = document.getElementById("sentimentBar").getContext("2d");
			var myBar = new Chart(ctx, {
				"type": "horizontalBar",
				"data": barData,
				"options": {
					"legend": {
						"display": false
					},
					"scales": {
						"xAxes": [{
							"id": "x0",
							"ticks": {
								"display": false,
								"beginAtZero": true
							}
						}]
					}
				}
			});
			// sentimentBar = new Chart(document.getElementById("sentimentBar"), {
				// "type": "horizontalBar",
				// "data": {
					// "labels": labels,
					// "datasets": [{
						// "data": data,
						// "fill": false,
						// "backgroundColor": ["rgba(255, 99, 132, 0.2)", "rgba(255, 159, 64, 0.2)",
							// "rgba(255, 205, 86, 0.2)", "rgba(75, 192, 192, 0.2)", "rgba(54, 162, 235, 0.2)",
							// "rgba(153, 102, 255, 0.2)", "rgba(201, 203, 207, 0.2)"
						// ],
						// "borderColor": ["rgb(255, 99, 132)", "rgb(255, 159, 64)", "rgb(255, 205, 86)",
							// "rgb(75, 192, 192)", "rgb(54, 162, 235)", "rgb(153, 102, 255)", "rgb(201, 203, 207)"
						// ],
						// "borderWidth": 1
					// }]
				// },
				// "options": {
					// "scales": {
						// "xAxes": [{
							// "ticks": {
								// "display": false,
								// "beginAtZero": true
							// }
						// }]
					// }
				// }
			// });
			
		},
		complete:function(){
		}
	});

	function stopAjax(ajax){  
	    //如果ajax未完成，則中止該ajax  
	        if(ajax) {ajax.abort();}  
	    }  
	}

});