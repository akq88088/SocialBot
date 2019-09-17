<?php
	//啟動session
	session_start();
?>
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8"/>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>語料應用與分析工具</title>
	<link rel="stylesheet" href="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/css/bootstrap.min.css">
	<script src="https://cdn.staticfile.org/jquery/2.1.1/jquery.min.js"></script>
	<script src="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>
	<meta name="viewport" content="width=device-width">
	<style>
	h1{
		text-align: center;
		font-family:"標楷體";
		font-size: 36px;
		font-weight: bold;
		font-style: normal;
		font-stretch: normal;
		line-height: normal;
		letter-spacing: 15px;
		color: white;
	}
	.Rectangle1{
		width: 1300px;
		height: 792px;
		background-color: #e49d38;
		text-align: center;
	}
	.Rectangle2{
		width: 1008px;
		height: 556px;
		border-radius: 38px;
		background-color: white;
		margin:0 auto;
		text-align:center;
		display:flex;
		align-items:center;
		justify-content:center;
	}
	#Facebook{
		width: 140px;
		height: 30px;
		font-family: NotoSansCJKtc;
		font-size: 20px;
		font-weight: bold;
		font-style: normal;
		font-stretch: normal;
		line-height: normal;
		letter-spacing: normal;
		text-align: center;
		background-color: #3b5998;
		color:white;
		border-style: none;
		border-radius: 40px;
	}
	#Google{
		width: 140px;
		height: 30px;
		font-family: NotoSansCJKtc;
		font-size: 20px;
		font-weight: bold;
		font-style: normal;
		font-stretch: normal;
		line-height: normal;
		letter-spacing: normal;
		text-align: center;
		background-color:#ea4335;
		color:white;
		border-style:none;
		border-radius: 40px;
	}
	#button{
		width:100px;
		height: 25px;
		font-family: NotoSansCJKtc;
		font-size: 16px;
		font-weight: bold;
		font-style: normal;
		font-stretch: normal;
		line-height: normal;
		letter-spacing: normal;
		background-color: #e49d38;
		color:white;
		border-style: none;
		border-radius: 40px;
	}	
	</style>
</head>
<body>
	<?php
		//使用 isset()方法，判別有沒有此變數可以使用，以及為已經登入
		if(isset($_SESSION['is_login']) && $_SESSION['is_login'] == TRUE):

		//使用php header來轉址到資料庫頁面
		header('location: project.php');
		
		else:
	?>
	<div class="Rectangle1">
		<br>
			<h1>語料應用與分析工具</h1>
		<br><br>
		<div class="Rectangle2">
			<div id="center">
				<input id="Facebook" type="button" class="btn btn-default" value="Facebook" onclick="location.href='https://zh-tw.facebook.com/'"></button>
				<input id="Google" type="button" class="btn btn-default" value="Google" onclick="location.href='https://accounts.google.com/ServiceLogin/signinchooser?hl=zh-TW&passive=true&continue=https%3A%2F%2Fwww.google.com%2F%3Fhl%3Dzh-TW&flowName=GlifWebSignIn&flowEntry=ServiceLogin'"></button>
				<br><br><br>
				<form action="checkpassword.php" method="post">
					<p><input type="text" placeholder=" Email" name="email" style="width:250px;"></p>
					<p><input type="password" placeholder=" 密碼" name="password" style="width:250px;"></p>
					<br>
					<p align="right">
						<a href="register.html"><input id="button" class="btn btn-default" value="註冊"></a>
						<input type="submit" id="button" class="btn btn-default" value="登入">
					</P>
				</form>
			</div>
		</div>
	</div>
	<?php endif; ?>
</body>
</html>