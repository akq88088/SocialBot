
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
		if(!text){
			alert('請輸入欲分析之內容');
		}
		$('#TextSum_and_SA').show();
		$('#QA').show();

		// getNER(text);
		getSummary(text, algorithm, percentage);
		getSentiment(text);
		getQA_test(text);
	});
	
	textUploader.addEventListener('change', function(e) {
		console.log(e.target.files); // get file object
		var reader = new FileReader();

		reader.onload = function(){
			var content = reader.result;
			$('#paste_text').val(content);
		};

		reader.readAsText(e.target.files[0]);
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
		window.location.href = 'report.php';
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
						"backgroundColor": ["rgba(255, 99, 71, 0.5)", "rgba(228, 157, 56, 0.5)", "rgba(0, 71, 171, 0.5)", "rgba(232, 226, 72, 0.5)", "rgba(58, 139, 126, 0.5)", "rgba(116, 172, 197, 0.5)"],
						"borderWidth": 0
					}]
				};
				var options = {
					"responsive": true,
					"maintainAspectRatio": false,
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
						}],
						"yAxes": [{
							"scaleFontSize": 18,
							"barPercentage": 0.4
						}]
					},
					"layout":{
						"padding":{
							"left":28
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
						ctx.drawImage(img, 0, bar._model.y - 12, 30, 20);
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
	var getQA_test = function(text){

		$.ajax({
			method: "POST",
			url: "../cgi-bin/QA_test.py",
			async: true, //非同步化
			// dataType:"json",
			data: {
				"text":text
				// data
			},
			beforeSend:function(){
				//$("#summary").val("出題中...");
			},
			success: function(data){
				console.log('ner success');
				var que_ans_dict = JSON.parse(data);
				console.log(que_ans_dict["0"]);
				var que_ans_row = "";
				var iRun = 0;
				var que_ans_div = [];
				var que_ans_dict_len = que_ans_dict.length;
				var temp = [];
				Object.keys(que_ans_dict).forEach(function(key) {
					que = que_ans_dict[key][0];
					ans = que_ans_dict[key][1];
					temp.push(que);
					temp.push(ans);
				//for (var i in que_ans_dict){
					if((iRun + 1) % 2 == 0 || iRun == que_ans_dict_len - 1){
						console.log("s---")
						console.log(iRun.toString());
						console.log(temp[0]);
						console.log(temp[1]);
						console.log(temp[2]);
						console.log(temp[3]);
						console.log("e---");
						if(temp.length == 4){
						que_ans_row = (que_ans_row + "\
						<div class='row'>\
						<div class='col-md-6 btm-mg'>\
						<label>問題 : </label>\
						<span>" + temp[0] + "</span>\
						<br>\
						<label>答案 : </label>\
						<span>" + temp[1] + "</span>\
						</div>\
						<div class='col-md-6 btm-mg'>\
						<label>問題 : </label>\
						<span>" + temp[2] + "</span>\
						<br>\
						<label>答案 : </label>\
						<span>" + temp[3] + "</span>\
						</div>\
						</div>"
						)
						}
						else if(temp.length == 2){
						que_ans_row = (que_ans_row + "\
						<div class='row'>\
						<div class='col-md-6 btm-mg'>\
						<label>問題 : </label>\
						<span>" + temp[0] + "</span>\
						<br>\
						<label>答案 : </label>\
						<span>" + temp[1] + "</span>\
						</div>\
						</div>"
						)
						}
						else{

						}
						temp = [];
					}
					iRun = iRun + 1;
				});
				var node = document.getElementsByClassName("alert alert-light radius-border orange-block")[0]
				node.innerHTML = que_ans_row;
				// 成功回傳後要做甚麼
			},
			complete:function(){
				// 全部執行完要做什麼
				console.log('ner finish')
			}
		});
	}

});