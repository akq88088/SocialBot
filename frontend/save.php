<?php
	require_once("dbtools.inc.php");
		
	$text = $_POST['text'];
	$model = $_POST['model'];
	$project_name = $_POST['project_name'];
	$summary = $_POST['summary'];
	$sentiment = $_POST['sentiment'];
	$QA = $_POST['QA'];
	$email = $_POST['email'];
		
	$link = create_connection();
	$sql = "INSERT INTO `project` (`owner`,`model`,`input`,`summary`,`sentiment`,`QA`,`project-name`)
			 VALUES ('$email','$model','$text','$summary','$sentiment','$QA','$project_name')
			 ON DUPLICATE KEY UPDATE `model`='$model', `input`='$text',`summary`='$summary',`sentiment`='$sentiment', `QA`='$QA'";
	$result = execute_sql($link, "socialbot", $sql);
?>