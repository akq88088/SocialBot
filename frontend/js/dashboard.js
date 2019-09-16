
$(document).ready(function(){
	// $('#TextSum_and_SA').hide();
	// $('#QA').hide();
	const textUploader = document.querySelector('#upload_text');
	var sum_currAjax = null;
	var sent_currAjax = null;
	$('#analyze').on('click', function(){
		var text = $('#paste_text').val();
		var algorithm = $('.btn-group > button.active')[0].id;
		var percentage = $('.btn-group > button.active')[1].getAttribute("percentage");

		$('#TextSum_and_SA').show();
		$('#QA').show();

		// getNER(text);
		getSummary(text, algorithm, percentage);
		getSentiment(text);
	});
	
	textUploader.addEventListener('change', function(e) {
		console.log(e.target.files); // get file object
		var reader = new FileReader();
		reader.onload = function(){
			var content = reader.result;
			console.log(content);
			$('#paste_text').val(content);
		};
		content = reader.readAsText(e.target.files[0]);
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

	function stopAjax(ajax){  
	    //如果ajax未完成，則中止該ajax  
	    if(ajax) {ajax.abort();}  
	}  

	var getSummary = function(text, algorithm, percentage){
		stopAjax(sum_currAjax);

		sum_currAjax = $.ajax({
			method: "POST",
			url: "../cgi-bin/getSummary.py",
			async: true, //非同步化
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
				$("#summary").val(text);
				console.log('summary done!');
			},
			complete:function(){
			}
		});
	}

	// var getNER = function(text){
	// 	// stopAjax(sum_currAjax);

	// 	ner_currAjax = $.ajax({
	// 		method: "POST",
	// 		url: "../cgi-bin/test_NER.py",
	// 		async: true, //非同步化
	// 		// dataType:"json",
	// 		data: {
	// 			"text" : text,
	// 		},
	// 		beforeSend:function(){
	// 			$("#summary").val("計算摘要中...");
	// 		},
	// 		success: function(text){
	// 			$("#summary").val(text);
	// 			console.log('summary done!');
	// 		},
	// 		complete:function(){
	// 		}
	// 	});
	// }

	var test = function(text){

		$.ajax({
			method: "POST",
			url: "path",
			async: true, //非同步化
			// dataType:"json",
			data: {
				// data
			},
			beforeSend:function(){
				// 送出前要做什麼
			},
			success: function(text){
				// 成功回傳後要做甚麼
			},
			complete:function(){
				// 全部執行完要做什麼
			}
		});
	}

	var getSentiment = function(text){
		stopAjax(sent_currAjax);

		sent_currAjax = $.ajax({
			method: "POST",
			url: "../cgi-bin/getSentiment.py",
			async: true, //同步化
			// dataType:"json",
			data: {
				"text" : text
			},
			beforeSend:function(){
			},
			success: function(text){
				$('#sentimentBar').remove();
				$('#sentimentResult').append('<canvas id="sentimentBar"></canvas>');
				text = text.replace(/'/g,'"');
				// console.log(text);
				var senRatio = JSON.parse(text);
				var labels=[],data=[];
				Object.keys(senRatio).forEach(function(key) {
					labels.push(key);
					data.push(senRatio[key]);
				});
				// console.log(senRatio);
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
				var options = {
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
					},
					"layout":{
						"padding":{
							"left":20
						}
					}
				};
				Chart.defaults.global.legend.display = false;
				Chart.defaults.scale.gridLines.display = false;
				for (var i in barData.labels) {
					var lab = barData.labels[i];
					var $img = $("<img/>").attr("id", lab).attr("src", "../img/" + lab + ".png");
					$("#pics").append($img);
				}
				var originalDraw = Chart.controllers.bar.prototype.draw;
				Chart.controllers.bar.prototype.draw = function(ease) {
					originalDraw.call(this, ease);
					drawFlags(this);
				};
				function drawFlags(t) {
					var chartInstance = t.chart;
					var dataset = chartInstance.config.data.datasets[0];
					var meta = chartInstance.controller.getDatasetMeta(0);
					var x0 = chartInstance.scales.x0.left;
					ctx.save();
					meta.data.forEach(function(bar, index) {
						var lab = bar._model.label;
						var img = document.getElementById(lab);
						ctx.drawImage(img, 0, bar._model.y - 6, 20, 12);
						ctx.stroke();
					});
					ctx.restore();
				}
				var ctx = document.getElementById("sentimentBar").getContext("2d");
				var myBar = new Chart(ctx, {
					"type": "horizontalBar",
					"data": barData,
					"options": options
				});
			},
			complete:function(){
			}
		});
	}


});