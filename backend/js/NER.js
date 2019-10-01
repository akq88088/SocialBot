$(document).ready(function(){
	const textUploader = document.querySelector('#ner_file');
	textUploader.addEventListener('change', function(e) {
		var reader = new FileReader();

		reader.onload = function(){
			var content = reader.result;
			getNER(content);
		};

		reader.readAsText(e.target.files[0]);
	});

	$("#train_ner").click(function(){
		words = [];
		$.each($(".word"),function(){
			words.push($(this).text());
		});
		pos = [];
		$.each($(".pos"),function(){
			pos.push($(this).text());
		});
		tags = [];
		$.each($(".tag"), function(){
			tags.push($(this).val());
		});

		trainNER(words, pos, tags);
	});
});

var getNER = function(text){
		// stopAjax(sum_currAjax);

		sum_currAjax = $.ajax({
			method: "POST",
			url: "../cgi-bin/to_NER.py",
			async: true, //非同步化
			// dataType:"json",
			data: {
				"text" : text
			},
			beforeSend:function(){
				$("#context").val("實體判別中...");
				$("#NER_result > tbody").html("");
			},
			success: function(res){
				$("#context").val(text);
				res  = JSON.parse(res);
				for(i=0; i<res.segment.length; i++){
					for(j=0; j<res.segment[i].length; j++){
						let option="<select class='form-control tag'>\
									<option value='x'>-</option>\
									<option value='per'>人</option>\
									<option value='obj'>物</option>\
									<option value='time'>時</option>\
									<option value='place'>地</option>\
									</select>"
						$("#NER_result > tbody").append("<tr>");
						$("#NER_result > tbody").append("<td class='word'>"+ res.segment[i][j] +"</td>");
						$("#NER_result > tbody").append("<td class='pos'>"+ res.pos[i][j] +"</td>");
						$("#NER_result > tbody").append("<td>"+ option+ "</td>");
						$("#NER_result").find("select").last().val(res.ner[i][j]);
					}
				}
				console.log("ner done!");
			},
			complete:function(){
			}
		});
	}

var trainNER = function(words, pos, tags){
		// stopAjax(sum_currAjax);

		sum_currAjax = $.ajax({
			method: "POST",
			url: "../cgi-bin/train_NER.py",
			async: true, //非同步化
			// dataType:"json",
			data: {
				"words": JSON.stringify(words),
				"pos" : JSON.stringify(pos),
				"tags": JSON.stringify(tags)
			},
			beforeSend:function(){
				$("#train_ner").attr('disabled','disabled');
			},
			success: function(res){
				alert('訓練完成!')
			},
			complete:function(){
				$("#train_ner").removeAttr('disabled');
				getNER($("#context").val());
			}
		});
	}
