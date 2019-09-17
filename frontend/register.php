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
	<title>語料專案</title>
</head>
<body>
<?php
	
	/* 引入檔案 */
	require_once("dbtools.inc.php");
	
	/* 取得表單資料 */
	$email = $_POST['email'];
	$password = $_POST['password'];
	$name = $_POST['name'];

	/* 建立資料連接 */
	$link = create_connection();
	
	/* 將使用者的email 和 資料庫的email 欄位做比對 */
	$sql = "SELECT * FROM `member` Where `email` = '$email'" ;
	$result = execute_sql($link, "socialbot", $sql);
	
	if(mysqli_num_rows($result) != 0 || $email == NULL || $password == NULL)
	{
		/* 釋放記憶體空間 */
		mysqli_free_result($result);
		
		header('location: register_false.php');
	}
	else
	{
		/* 釋放記憶體空間 */
		mysqli_free_result($result);
		
		/* 將資料寫入資料庫 */
		$sql = "INSERT INTO `member` (member_id, email, password, name)
			VALUES ('".hash('md5',$email)."','$email','".md5($password)."', '$name')";
	
		$result = execute_sql($link, "socialbot", $sql);
	
		/* 關閉資料連結 */
		mysqli_close($link);
		
		header('location: register_finish.php');
	}
?>
</body>
</html>