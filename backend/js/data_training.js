$(document).ready(function(){
	$('#sidebar > .worker').on('click', function(){
		$(this).parent().find('.worker').removeClass('active');
		$(this).toggleClass('active');
	});

	$('#frontend').on('click', function(){
		window.location.href = '../frontend/project.php';
	});

	$('.new-project').on('click', function(){
		var project_name = prompt("請輸入模型名稱", "");
		$.ajax({
			url:"new_project.php",
			data:{
				'p_name':project_name
			},
			dataType:"text",
			method:"POST",
			error:function(){
				alert("建立失敗，請重新嘗試");
			},
			success:function(res){
				res = res.trim();
				console.log(res);
				if(res!="0"){
					window.location.href = 'train.php?name='+project_name;
				}else{
					alert('專案名稱重複或是資料庫錯誤，請重新嘗試!');
				}
			}
		});
	});

	$('.old-project').on('click', function(){
		var project_name = $(this).find('.model').text();
		window.location.href = 'train.php?name='+project_name;
	});
});