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
	<!-- JQuery -->
	<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" crossorigin="anonymous"></script>
	<script src="http://code.jquery.com/jquery-3.3.1.min.js" crossorigin="anonymous"></script>
	<!-- Bootstrap JS -->
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" crossorigin="anonymous"></script>
	<!-- Customer JS -->
	<script src="../frontend/js/global.js" crossorigin="anonymous"></script>
	<script src="./js/data_training.js" crossorigin="anonymous"></script>

	<script>
		function toLogout() {
			window.location.replace("../frontend/Logout.php")
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
			<div class="col-md-4 offset-md-4 ta-c" id="title"><h5>語 料 應 用 與 分 析 工 具</h5></div>
			<div class="col-md-2 offset-md-1 ta-c"><?php echo $email;?></div>
			<div class="col-md-1 ta-c" id="logout" role="button" onclick="toLogout();">登出</div>
		</div>
	</div>
	
	<div class="container-fluid">
		<div class="row" id=content>
			<div class="col-lg-2" id="sidebar">
				<div class="worker ta-c" id="frontend">
					語料應用
				</div>
				<div class="worker ta-c active" id="backend">
					資料訓練後台
				</div>
			</div>
			<div class="col-lg-10">
				<div class="container">
					<h6 class="my-4">新 增 訓 練 模 型</h6>
					<div class="row">
						<div class="col-lg-3 btm-mg-1">
							<div class="radius-border c-project">
								<div class="radius-border ta-c" id="add_project_btn">+</div>
							</div>
						</div>
					</div>
				</div>
				<div class="container">
					<h6 class="my-4">資 料 訓 練 模 型</h6>
					<div class="row">
						<div class="col-lg-3 btm-mg-1">
							<div class="radius-border c-project">
								<div class="c-time">2019-09-02</div>
								<div class="model">國小讀本</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
	<?php
		else:
			header('location: ../frontend/login.php');
		endif;
	?>
</body>
</html>