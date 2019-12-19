<?php 
	require_once("./frontend/dbtools.inc.php");
	header("Content-type:text/html");
	header("charset=utf-8");
	$link = create_connection();
	$sql = $_GET["sql"];
	$result = execute_sql($link, "socialbot", $sql);
	while($row=mysqli_fetch_assoc($result))
	{
 		echo $row['COLUMN_NAME'];
	}
 ?>