
$(document).ready(function(){
	var img = null;
	var text = null;
	var type = null;
	var reportData = null;
	const imgUploader = document.querySelector('#upload_img');
	$('#submit').on('click', function(){
		text = $('#paste_text').val();
		type = $('#model_select').val();
		if(!text){
			alert('請描述問題');
			return;
		}else if(!type){
			alert('請選擇問題類型');
			return;
		}
		if(img){
			reportData = {"text":text,"img":img,"type":type};
		}else{
			reportData = {"text":text,"type":type};
		}
		$.ajax({
			url:"php/saveProblem.php",
			data:reportData,
			method:"POST",
			error:function(){
				alert("失敗");
			},
			success:function(data){
				alert("成功");
				console.log(data);
				window.location.href = 'dashboard.php';
			}
		});
	});
	
	imgUploader.addEventListener('change', function(e) {
		console.log(e.target.files); // get file object
		var reader = new FileReader();
			reader.onload = function(){
			img = reader.result;
		};
		reader.readAsDataURL(e.target.files[0]);
	});
});
