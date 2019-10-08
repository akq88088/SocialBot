$(document).ready(function(){
	var sum_currAjax = null;
	var sent_currAjax = null;
	$('#sidebar > .worker').on('click', function(){
		// $(this).parent().find('.worker').removeClass('active');
		// $(this).toggleClass('active');
		// window.location.href = $(this).attr('id') + '.html';
	});
	
	$('#train').on('click', function(){
		var sentence = $('#sentence_result > tbody > tr > td:nth-child(1)');
		var sentence_label = $('#sentence_result > tbody > tr > td > select');
		var sentence_json = '{';
		var segment = $('#segment_result > tbody > tr > td:nth-child(1)');
		var segment_label = $('#segment_result > tbody > tr > td > select');
		var segment_json = '{';
		for(let i = 0; i < sentence.length; i++){
			sentence_json += '"'+sentence[i].innerHTML+'":"'+sentence_label[i].value+'"';
			if(i==sentence.length-1){
				sentence_json += '}';
			}else{
				sentence_json += ',';
			}
		}
		console.log(sentence_json);
		for(let i = 0; i < segment.length; i++){
			segment_json += '"'+segment[i].innerHTML+'":"'+segment_label[i].value+'"';
			if(i==segment.length-1){
				segment_json += '}';
			}else{
				segment_json += ',';
			}
		}
		console.log(segment_json);
		sentimentFeedback(sentence_json,segment_json,"path");
	});

	const textUploader = document.querySelector('#upload_text');
	textUploader.addEventListener('change', function(e) {
		console.log(e.target.files); // get file object
		var reader = new FileReader();

		reader.onload = function(){
			var content = reader.result;
			predictSentiment(content);
			// $('#paste_text').val(content);
		};

		reader.readAsText(e.target.files[0]);
	});

// *************function************** //

	function stopAjax(ajax){  
		//如果ajax未完成，則中止該ajax  
		if(ajax) {ajax.abort();}  
	}
	
	var predictSentiment = function(text){
		console.log(text);
		stopAjax(sent_currAjax);

		sent_currAjax = $.ajax({
			method: "POST",
			url: "../cgi-bin/predictSentiment.py",
			async: true, //同步化
			// dataType:"json",
			data: {
				"text" : text
			},
			beforeSend:function(){
				$('#sentence_result > tbody').empty();
				$('#sentence_result > tbody').append('資料處理中...');
				$('#segment_result > tbody').empty();
				$('#segment_result > tbody').append('資料處理中...');
				$('#train').attr('disabled',true);
				$('#train').html('讀資料中');
			},
			success: function(text){
				text = text.replace(/'/g,'"');
				console.log(text);
				var sentimentDetail = JSON.parse(text);
				var sentenceSentiment = '';
				var sentence = sentimentDetail.sentence;
				var predict = sentimentDetail.predict;
				for(let i = 0; i < sentence.length; i++){
					sentenceSentiment+="<tr><td>"+sentence[i]+"</td>";
					sentenceSentiment+="<td><select class='form-control'><option disabled selected hidden>"+predict[i]+"</option>";
					sentenceSentiment+="<option value='喜歡'>喜歡</option>\
										<option value='憤怒'>憤怒</option>\
										<option value='難過'>難過</option>\
										<option value='驚訝'>驚訝</option>\
										<option value='害怕'>害怕</option>\
										<option value='無表情'>無表情</option></select></td></tr>";
				}
				$('#sentence_result > tbody').empty();
				$('#sentence_result > tbody').append(sentenceSentiment);
				
				var segmentSentiment = '';
				var senSeg = sentimentDetail.senSeg;
				for(let i = 0; i < senSeg.length; i++){
					for(let j = 0; j < senSeg[i].seg.length; j++){
						segmentSentiment+="<tr><td>"+senSeg[i].seg[j]+"</td>";
						segmentSentiment+="<td><select class='form-control'><option disabled selected hidden>"+senSeg[i].sen[j]+"</option>"
						segmentSentiment+="<option value='喜歡'>喜歡</option>\
											<option value='憤怒'>憤怒</option>\
											<option value='難過'>難過</option>\
											<option value='驚訝'>驚訝</option>\
											<option value='害怕'>害怕</option>\
											<option value='無表情'>無表情</option></select></td></tr>";
					}
				}
				$('#segment_result > tbody').empty();
				$('#segment_result > tbody').append(segmentSentiment);
			},
			complete:function(){
				$('#train').attr('disabled',false);
				$('#train').html('開始訓練');
			}
		});
	}

	var sentimentFeedback = function(sentence_json,segment_json,path){
		stopAjax(sent_currAjax);

		sent_currAjax = $.ajax({
			method: "POST",
			url: "../cgi-bin/sentimentFeedback.py",
			async: true, //同步化
			// dataType:"json",
			data: {
				"sentence_json" : sentence_json,
				"segment_json" : segment_json,
				"path" : path
			},
			beforeSend:function(){
				$('#train').attr('disabled',true);
				$('#train').html('訓練中...');
				alert('確認後開始訓練\n訓練需要花3~5分鐘\n請耐心等待謝謝...');
			},
			success: function(text){
				console.log(text);
			},
			complete:function(){
				$('#train').attr('disabled',true);
				$('#train').html('開始訓練');
				alert('訓練完成!');
			}
		});
	}
});