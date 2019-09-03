
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

		getSummary(text, algorithm, percentage);
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


});