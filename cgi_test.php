
<!DOCTYPE html>
<html>

<head>
	<title>Crawler</title>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
</head>
<body>
	<div>
		<input type="text" name="place">
		<input type="submit" onclick="start();" name="start">
	</div>
</body>
</html>

 <script type="text/javascript">
	function start(){
		var input = $("input[name=place]").val();

		$.ajax({
			url: "cgi-bin/cgi_test.py",
			success: function(response) {
				console.log(response);
			}
		});
	}
</script>