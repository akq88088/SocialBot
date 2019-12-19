<?php
	//啟動session
	session_start();
?>
<!DOCTYPE html>
<html lang="zh">
<head>
	<meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">

	<!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css" crossorigin="anonymous">
	<!-- CustomScrollbar CSS -->
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/malihu-custom-scrollbar-plugin/3.1.5/jquery.mCustomScrollbar.min.css">
	<!-- Customer CSS -->
	<link rel="stylesheet" href="css/global.css">
	<link rel="stylesheet" href="css/report.css">
	<!-- JQuery -->
	<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" crossorigin="anonymous"></script>
	<script src="http://code.jquery.com/jquery-3.3.1.min.js" crossorigin="anonymous"></script>
	<!-- Bootstrap JS -->
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" crossorigin="anonymous"></script>
	<!-- Customer JS -->
	<script src="./js/global.js" crossorigin="anonymous"></script>	
	<script src="./js/report.js" crossorigin="anonymous"></script>	

	<script>
		function toLogout() {
			window.location.replace("Logout.php")
		}
	</script>
	
	<title>語料專案</title>
</head>
<body>
	<?php
		require_once("dbtools.inc.php");
		
		//使用 isset()方法，判別有沒有此變數可以使用，以及為已經登入
		if(isset($_SESSION['is_login']) && $_SESSION['is_login'] == TRUE):

		$email = $_SESSION['email'];
		$member_id = $_SESSION['member_id'];
		$link = create_connection();
		$sql = "SELECT * FROM `project` WHERE ID ='$member_id'";
		$result = execute_sql($link, "membership", $sql);
	?>

	<!-- header -->
	<div class="container-fluid header">
		<div class="row">
			<div class="col-md-1 ta-c" id="back" role="button">< 返回</div>
			<div class="col-md-4 offset-md-3 ta-c" id="title"><h5>語 料 應 用 與 分 析 工 具</h5></div>
			<div class="col-md-2 offset-md-1 ta-c"><?php echo $email;?></div>
			<div class="col-md-1 ta-c" id="logout" role="button" onclick="toLogout();">登出</div>
		</div>	
	</div>

	<!-- Page Content -->
	<div class="container">
		
		<!-- 問題回報 -->
		<div class="container">
			<div>
				<h6 class="my-4">問 題 回 報</h6>	
			</div>
			<div class="alert alert-light radius-border green-block" id="import">
				<div class="row">
					<div class="col-lg-6 btm-mg">
						<p>問題類型</p>
						<div>
							<select class="form-control green-border" id="model_select">
								<option disabled selected hidden>請選擇問題類型</option>
								<option>文本摘要內容錯誤</option>
								<option>情緒辨識錯誤</option>
								<option>問題答案錯誤</option>
								<option>其他</option>
							</select>
						</div>
					</div>
					<div class="col-lg-6 btm-mg">
						<p>問題說明</p>
						
						<div class="form-group">
							<textarea class="form-control radius-border green-border" id="paste_text" rows="12" placeholder="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras dapibus vulputate diam eu pretium. Mauris elit orci, ultricies id fermentum vel, porta et eros. Vestibulum condimentum lectus in convallis feugiat. Sed vulputate fringilla felis. Aliquam ut arcu et dui feugiat scelerisque eu quis diam. Mauris placerat congue dui sit amet blandit. Phasellus condimentum libero vel velit auctor, sit amet tincidunt velit varius."></textarea>
						</div>

						<p>上傳截圖</p>
						<div class="form-group">
							<input type="file" class="form-control-file" id="upload_img" accept=".png,.jpg">
						</div>
					</div>
				</div>
				<div class="col-md-2 offset-md-10">
					<button class="btn radius-border" id="submit" name=<?php echo $_GET['name'];?>>送出</button>
				</div>
			</div>
		</div>
	</div>
	
	<?php
		else:
			header('location: login.php');
		endif;
	?>
</body>
</html>
	
