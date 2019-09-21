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
	<link rel="stylesheet" href="../frontend/css/global.css">
	<link rel="stylesheet" href="../frontend/css/project.css">
	<link rel="stylesheet" href="css/button.css">
	<!-- JQuery -->
	<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" crossorigin="anonymous"></script>
	<script src="http://code.jquery.com/jquery-3.3.1.min.js" crossorigin="anonymous"></script>
	<!-- Bootstrap JS -->
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" crossorigin="anonymous"></script>
	<!-- Customer JS -->
	<script src="../frontend/js/global.js" crossorigin="anonymous"></script>	
	<script src="./js/NER.js" crossorigin="anonymous"></script>

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
	
	<div class="container-fluid">
		<div class="row">
			<div class="col-lg-2" id="sidebar">
				<div class="worker ta-c" id='QA'>
					出題問答
				</div>
				<div class="worker ta-c active" id='NER'>
					命名實體
				</div>
				<div class="worker ta-c" id='emotion_recognition'>
					情緒辨識
				</div>
			</div>
			<div class="col-lg-10">
				<div class="container">
					<h6 class="my-4">匯 入 資 料</h6>
					<div class="row">
						<div class="col-lg-12 btm-mg-1">
							<div class="radius-border project blue-block">
								<p><label for="inputfile">上傳檔案</label></p>
								<p><input type="file" id="inputfile"></p>
								<div class="col-md-2 offset-md-10">
									<button class="btn radius-border" id="submit">開始訓練</button>
								</div>
							</div>
						</div>
					</div>
				</div>

				<div class="container">
					<h6 class="my-4">出 題 規 則</h6>
						<div class="alert alert-light radius-border darkblue-block" id="import">
							<div class="row">
								<div class="col-lg-6">
									<p>原文</p>
								</div>
								<div class="col-lg-6">
									<p>字詞屬性標記</p>
									<table class="table">
										<thead>
											<tr>
												<th><span class="glyphicon glyphicon-font"></span> 字詞</th>
												<th><span class="glyphicon glyphicon-list"></span> 屬性</th>
											</tr>
										</thead>
										<tbody>
											<tr>
												<td>大自然</td>
												<td>人</td>
											</tr>
											<tr>
												<td>會</td>
												<td>v</td>
											</tr>
										</tbody>
									</table>
								</div>
							</div>
						</div>
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