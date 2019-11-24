<?php
	//啟動session
	session_start();
	$csrftoken = substr(hash("md5", rand()),0, 16); 
	$_SESSION['csrf'] = $csrftoken;
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
		width: 556px;
		height: 338px;
		border-radius: 38px;
		background-color: white;
		margin:0 auto;
		text-align:center;
		display:flex;
		align-items:center;
		justify-content:center;
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
	<div class="Rectangle1">
		<br>
		<h1>語料應用與分析工具</h1>
		<br><br>
		<div class="Rectangle2">
			<div id="center">
				<form action="regist.php" method="post">
					<input type="hidden" name="csrftoken" value=<?php echo $csrftoken;?>/>
					<p> Email： <input type="text" name="email"/><br></p>
					<p>Password：<input type="password" name="password"/><br></p>
					<p> Name： <input type="text" name="name"/><br></p>
					<br>
					<p align="right">
						<input id="button" type="submit" class="btn btn-default" value="註冊">
					</p>
				</form>	
			</div>
		</div>
	</div>
</body>
</html>