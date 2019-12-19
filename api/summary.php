<?php
if(isset($_POST['algorithm']) && isset($_POST['percentage']) && isset($_POST['text'])){
	$algorithm = $_POST['algorithm'];
	$percentage = $_POST['percentage'];
	$text = $_POST['text'];
}

$ch = curl_init();

curl_setopt($ch, CURLOPT_URL,"http://120.125.85.96/www/SocialBot/cgi-bin/getSummary.py");
curl_setopt($ch, CURLOPT_POST, 1);

// in real life you should use something like:
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query(array('algorithm' => $algorithm, 'percentage' => $percentage, 'text' => $text)));
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false); //SSL憑證關閉
curl_exec ($ch);
curl_close ($ch);
?>