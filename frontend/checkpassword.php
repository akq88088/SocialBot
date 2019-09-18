<!DOCTYPE html>
<html>
<head>
</head>
<body>
<?php
	//啟動session
	session_start();
	
	require_once("dbtools.inc.php");
	header("Content-type:text/html");
	header("charset=utf-8");
	
	//取得表單資料
	$email = $_POST["email"];
	$password = $_POST["password"];
	
	//建立資料連接
	$link = create_connection();
	
	//將Email與密碼和資料庫的紀錄作比對
	$sql = "SELECT * FROM `member` Where `email` = '$email' AND `password` = '".md5($password)."'";
	$result = execute_sql($link, "socialbot", $sql);
	
	//若Email與密碼錯誤，就顯示對話方塊要求查明後再登入
	if(mysqli_num_rows($result) == 0)
	{
		//釋放記憶體空間
		mysqli_free_result($result);
		
		//關閉資料連接
		mysqli_close($link);
		
		//將session加入一個失敗的紀錄
		$_SESSION['is_login'] = false;
		
		header("location:login_false.php");
	}
	//否則將資料寫入Cookie，然後導向到會員專區網頁
	else
	{
		$row=mysqli_fetch_assoc($result);
		//比對登入的帳號
		$_SESSION['email'] = $email;
		$_SESSION['member_id'] = $row['member_id'];
		
		//將session加入一個已經登入的紀錄
		$_SESSION['is_login'] = true;
		
		header("location:project.php");
	}
?>