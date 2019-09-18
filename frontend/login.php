<?php
	//啟動session
	session_start();
?>
<!DOCTYPE html>
<html lang="zh-Hant-TW">
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
	<link rel="stylesheet" href="css/login.css">
	<!-- JQuery -->
	<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" crossorigin="anonymous"></script>
	<script src="http://code.jquery.com/jquery-3.3.1.min.js" crossorigin="anonymous"></script>
	<!-- Bootstrap JS -->
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" crossorigin="anonymous"></script>
	
	<!-- Chart JS -->
	<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.2/Chart.min.js"></script>
	
	<!-- Customer JS -->
	<script src="./js/global.js" crossorigin="anonymous"></script>	
	<script src="./js/login.js" crossorigin="anonymous"></script>

	<title>語料應用平台登入</title>
</head>
<body>
	<?php
		//使用 isset()方法，判別有沒有此變數可以使用，以及為已經登入
		if(isset($_SESSION['is_login']) && $_SESSION['is_login'] == TRUE):

		//使用php header來轉址到資料庫頁面
		header('location: project.php');
		
		else:
	?>
	<div class="container">
		<div class="row" id="title">
			<div class="col-6 offset-3">
				<h4>語 料 應 用 與 分 析 工 具</h4>
			</div>
		</div>
		<div class="row">
			<div class="col-8 offset-2">
				<div class="radius-border" id="panel">
					<div class="row">
						<div class="col-5 btn ta-c radius-border" id="Facebook">
							Facebook			
						</div>
						<div class="col-2"></div>
						<div class="col-5 btn ta-c radius-border" id="Google">
							Google
						</div>
					</div>
					<div class="form-group">
						<input type="text" class="form-control radius-border" placeholder="Email" name="Email"></input>
						<input type="text" class="form-control radius-border" placeholder="密碼" name="Passswd"></input>
					</div>
					<div class="row">
						<div class="col-8 offset-4">
							<div class="row bottom-clear">
								<div class="col-5 btn ta-c radius-border" id="Signup">
									註冊		
								</div>
								<div class="col-1"></div>
								<div class="col-5 btn ta-c radius-border" id="Signin">
									登入
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
			
		</div>
	</div>
	<?php endif; ?>
</body>
</html>