$(document).ready(function(){
	const textUploader = document.querySelector('#ner_file');
	textUploader.addEventListener('change', function(e) {
		console.log(e.target.files); // get file object
		var reader = new FileReader();

		reader.onload = function(){
			var content = reader.result;
			getNER(content);
		};

		reader.readAsText(e.target.files[0]);
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
			},
			success: function(res){
				$("#context").val(text);
				res  = JSON.parse(res);
				$("#NER_result > tbody").html("");
				for(i=0; i<res.segment.length; i++){
					for(j=0; j<res.segment[i].length; j++){
						let option="<select class='form-control'>\
									<option value='x'>-</option>\
									<option value='per'>人</option>\
									<option value='obj'>物</option>\
									<option value='time'>時</option>\
									<option value='place'>地</option>\
									</select>"
						$("#NER_result > tbody").append("<tr>");
						$("#NER_result > tbody").append("<td>"+ res.segment[i][j] +"</td>");
						$("#NER_result > tbody").append("<td>"+ res.pos[i][j] +"</td>");
						$("#NER_result > tbody").append("<td>"+ option+ "</td>");
						$("#NER_result").find("select").last().val(res.ner[i][j]);
						$("#NER_result > tbody").append("</tr>");
					}
				}
				console.log("ner done!");
			},
			complete:function(){
			}
		});
	}
