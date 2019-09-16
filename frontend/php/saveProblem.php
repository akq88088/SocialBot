<?php
	header("Content-Type: text/html;charset=utf-8"); 
	session_start();
	// $name = $_SESSION['name'];
	$name = '中文';
	$text = $_POST['text'];
	$type = $_POST['type'];
	$img = $_POST['img'];
	
	$img_path = tempnam('Screenshot','');
	unlink($img_path);
	$img_path = str_replace('.tmp','.png',$img_path);
	$img_path = str_replace('\\','/',$img_path);
	file_put_contents($img_path, file_get_contents($img));
	
	
	$dbhost = "120.125.85.96";
	$dbuser = "socialbot";
	$dbpass = "mcuiii";
	$db = "socialbot";
	$conn = new mysqli($dbhost, $dbuser, $dbpass, $db) or die("Connect failed: %s\n". $conn -> error);
	
	$sql = "INSERT INTO problem(name,description,type,screenshot_path) VALUES('".$name."','".$text."','".$type."','".$img_path."')";
	// $sql = "SELECT * FROM member";
	echo $sql;
	$result = mysqli_query($conn, $sql);
	echo $result;
	echo $img_path;
	echo $text;
	echo getcwd();
	echo $type;
	echo $img;
	
?>