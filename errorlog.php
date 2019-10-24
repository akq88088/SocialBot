<?php 	
// Use fopen function to open a file
$file = fopen("D:/xampp/apache/logs/error.log", "r");

// Read the file line by line until the end
while (!feof($file)) {
	$value = fgets($file);
	print $value;
	print "<br>";
}

// Close the file that no longer in use
fclose($file);
?>