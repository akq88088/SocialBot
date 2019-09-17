<!DOCTYPE html>
<html>
<head>
</head>
<body>
<?php
	//啟動session
	session_start();
	
	require_once("dbtools.inc.php");
	header("charset=utf-8");

	//清空Session
	session_unset();

	//使用php header來轉址 返回登入頁面
	header("Location:login.php");
?>
</body>
</html>