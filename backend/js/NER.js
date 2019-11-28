$(document).ready(function(){
	var pid = $('#project_name').attr('pid');

	const textUploader = document.querySelector('#ner_file');
	textUploader.addEventListener('change', function(e) {
		// console.log(e.target.files); // get file object
		var reader = new FileReader();
		if(e.target.files[0].name.includes('.docx')){
			reader.onload = function(){
				var zip = new JSZip(reader.result);
			    var doc = new window.docxtemplater().loadZip(zip);
			    var content = doc.getFullText();
			    getNER(content, pid);
			    $('#paste_text').val(content);
			};
		    reader.readAsBinaryString(e.target.files[0]);
		}else{
			reader.onload = function(){
				var content = reader.result;
				getNER(content, pid);
				$('#paste_text').val(content);
			};
			reader.readAsText(e.target.files[0]);
		}
		e.target.value=null;
	});

	$("#train_ner").click(function(){
		var words = [];
		$.each($(".word"),function(){
			words.push($(this).text());
		});
		var pos = [];
		$.each($(".pos"),function(){
			pos.push($(this).text());
		});
		var tags = [];
		$.each($(".tag"), function(){
			tags.push($(this).val());
		});

		trainNER(words, pos, tags, pid);
	});
});

var getNER = function(text, pid){
		// stopAjax(sum_currAjax);

		sum_currAjax = $.ajax({
			method: "POST",
			url: "../cgi-bin/to_NER.py",
			async: true, //非同步化
			// dataType:"json",
			data: {
				"text" : text,
				"pid" : pid
			},
			beforeSend:function(){
				$("#context").val("實體判別中...");
				$("#NER_result > tbody").html("");
			},
			success: function(res){
				$("#context").val(text);
				console.log(pid);
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

var trainNER = function(words, pos, tags, pid){
		// stopAjax(sum_currAjax);

		sum_currAjax = $.ajax({
			method: "POST",
			url: "../cgi-bin/train_NER.py",
			async: true, //非同步化
			// dataType:"json",
			data: {
				"words": JSON.stringify(words),
				"pos" : JSON.stringify(pos),
				"tags": JSON.stringify(tags),
				"pid" : pid
			},
			beforeSend:function(){
				$("#train_ner").attr('disabled','disabled');
			},
			success: function(res){
				alert('訓練完成!');
			},
			complete:function(){
				$("#train_ner").removeAttr('disabled');
				getNER($("#context").val());
			}
		});
	}
