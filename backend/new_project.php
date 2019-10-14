<?php 
	require_once("dbtools.inc.php");

	$link = create_connection();

	if(!isset($_POST['p_name']) || strlen($_POST['p_name'])<1){
		echo "0";
	}else{
		$p_name = $_POST['p_name'];
		$p_id = substr(md5(hash('md5', $p_name)),0,8);
		$sql = "INSERT INTO model(p_id, p_name) VALUES('$p_id', '$p_name')";
		if(execute_sql($link, "socialbot", $sql) == 1){
			echo "1";
			if(!is_dir("../cgi-bin/module/model/$p_id")){
				if (mkdir("../cgi-bin/module/model/$p_id")){
					echo "2";
				}else echo "0";
			}
		}else{
			echo "0";
		}
	}

?>