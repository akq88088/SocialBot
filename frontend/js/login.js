$(document).ready(function(){
	$('#Signin').on('click', function(){
		var email= $('input[name="Email"]').val();
		var passwd = $('input[name="Passwd"]').val();
		$.ajax({
			method: "POST",
			url: "../checkpassword.php",
			async: true, //非同步化
			// dataType:"json",
			data: {
				"email" : email,
				"password" : password,
			},
			success: function(text){
			},
			complete:function(){
			}
		});
	});
});