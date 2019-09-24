<?php
	//啟動session
	session_start();
?>
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
	<!-- Customer CSS -->
	<link rel="stylesheet" href="../frontend/css/global.css">
	<link rel="stylesheet" href="../frontend/css/project.css">
	<link rel="stylesheet" href="css/button.css">
	<link rel="stylesheet" href="./css/emotion_recognition.css">
	<!-- JQuery -->
	<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" crossorigin="anonymous"></script>
	<script src="http://code.jquery.com/jquery-3.3.1.min.js" crossorigin="anonymous"></script>
	<!-- Bootstrap JS -->
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" crossorigin="anonymous"></script>
	<!-- Customer JS -->
	<script src="./js/train.js" crossorigin="anonymous"></script>
	<script src="./js/emotion_recognition.js"></script>
	
	<script>
		function toLogout() {
			window.location.replace("Logout.php")
		}
	</script>

	<title>語料專案</title>
</head>
<body>
	<?php
		require_once("dbtools.inc.php");
		
		//使用 isset()方法，判別有沒有此變數可以使用，以及為已經登入
		if(isset($_SESSION['is_login']) && $_SESSION['is_login'] == TRUE):

		$email = $_SESSION['email'];
	?>
	
	<!-- header -->
	<div class="container-fluid header">
		<div class="row">
			<div class="col-md-1 ta-c" id="back" role="button">< 返回</div>
			<div class="col-md-4 offset-md-3 ta-c" id="title"><h5>語 料 應 用 與 分 析 工 具</h5></div>
			<div class="col-md-2 offset-md-1 ta-c"><?php echo $email;?></div>
			<div class="col-md-1 ta-c" id="logout" role="button" onclick="toLogout();">登出</div>
		</div>	
	</div>
	
	<div class="container-fluid">
		<div class="row">
			<div class="col-lg-2" id="sidebar">
				<div class="worker ta-c active" target="#QA">
					出題問答
				</div>
				<div class="worker ta-c" target="#NER">
					命名實體
				</div>
				<div class="worker ta-c" target="#emotion_recognition">
					情緒辨識
				</div>
			</div>
			<div class="col-lg-10">
				<div id="QA" class="collapse show">
					<div class="container">
						<h6 class="my-4">匯 入 資 料</h6>
						<div class="row">
							<div class="col-lg-12 btm-mg-1">
								<div class="radius-border project blue-block">
									<p><label for="inputfile">上傳檔案</label><P>
									<P><input type="file" id="inputfile"></p>
									<div class="col-md-2 offset-md-10">
										<button class="btn radius-border" id="submit">開始訓練</button>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div class="container">
						<h6 class="my-4">出 題 規 則</h6>
						<div class="row">
							<div class="col-lg-12 btm-mg-1">
								<div class="alert alert-light radius-border project yellow-block">
									<table class="table">
										<thead>
											<tr>
												<th><span class="glyphicon glyphicon-font"></span> 問題</th>
												<th><span class="glyphicon glyphicon-list"></span> 出題規則</th>
												<th><span class="glyphicon glyphicon-align-left"></span> 原句</th>
												<th><span class="glyphicon glyphicon-align-left"></span> 答案</th>
											</tr>
										</thead>
										<tbody>
											<tr>
												<td>誰會說話?</td>
												<td>誰+v1+v2</td>
												<td>大自然會說話</td>
												<td>大自然</td>
											</tr>
											<tr>
												<td>孔子很注重視什麼?</td>
												<td>人1+d1+v1+什麼</td>
												<td>孔子很重視孝道</td>
												<td>孝道</td>
											</tr>
										</tbody>
									</table>
								</div>
							</div>
						</div>
					</div>
				</div>
				<div id="NER" class="collapse">
					<div class="container">
						<h6 class="my-4">匯 入 資 料</h6>
						<div class="row">
							<div class="col-lg-12 btm-mg-1">
								<div class="radius-border project blue-block">
									<p><label for="inputfile">上傳檔案</label></p>
									<p><input type="file" id="inputfile"></p>
									<div class="col-md-2 offset-md-10">
										<button class="btn radius-border" id="submit">開始訓練</button>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div class="container">
						<h6 class="my-4">出 題 規 則</h6>
						<div class="alert alert-light radius-border darkblue-block" id="import">
							<div class="row">
								<div class="col-lg-6">
									<p>原文</p>
								</div>
								<div class="col-lg-6">
									<p>字詞屬性標記</p>
									<table class="table">
										<thead>
											<tr>
												<th><span class="glyphicon glyphicon-font"></span> 字詞</th>
												<th><span class="glyphicon glyphicon-list"></span> 屬性</th>
											</tr>
										</thead>
										<tbody>
											<tr>
												<td>大自然</td>
												<td>人</td>
											</tr>
											<tr>
												<td>會</td>
												<td>v</td>
											</tr>
										</tbody>
									</table>
								</div>
							</div>
						</div>
					</div>
				</div>
				<div id="emotion_recognition" class="collapse">
					<div class="container">
						<h6 class="my-4">匯 入 資 料</h6>
						<div class="row">
							<div class="col-lg-12 btm-mg-1">
								<div class="radius-border project blue-block">
									<p><label for="inputfile">上傳檔案</label><P>
									<P><input type="file" id="upload_text" accept=".txt"></p>
									<div class="col-md-2 offset-md-10">
										<button class="btn radius-border" id="train">開始訓練</button>
									</div>
								</div>
							</div>
						</div>
					</div>

					<div class="container">
						<h6 class="my-4">情 續 辨 別</h6>
						<div class="alert alert-light radius-border red-block" id="import">
							<div class="row">
								<div class="col-lg-6" style="height:600px;overflow:auto;">
									<p>句子情緒辨別</p>
										<table class="table" id="sentence_result">
											<col width="70%">
											<col width="30%">
											<thead>
												<tr>
													<th><span class="glyphicon glyphicon-font"></span> 句子</th>
													<th><span class="glyphicon glyphicon-list"></span> 情緒</th>
												</tr>
											</thead>
											<tbody>
												<tr>
													<td>小山羊高興地跑來跑去</td>
													<td>小山羊到河邊喝水</td>
												</tr>
												<tr>
													<td>高興</td>
													<td>無表情</td>
												</tr>
											</tbody>
										</table>
								</div>
								<div class="col-lg-6" style="height:600px;overflow:auto;">
									<p>字詞情緒標記</p>
									<table class="table" id="segment_result">
										<col width="70%">
										<col width="30%">
										<thead>
											<tr>
												<th><span class="glyphicon glyphicon-font"></span> 字詞</th>
												<th><span class="glyphicon glyphicon-list"></span> 情緒</th>
											</tr>
										</thead>
										<tbody>
											<tr>
												<td>小山羊</td>
												<td>無表情</td>
											</tr>
											<tr>
												<td>高興</td>
												<td>喜歡</td>
											</tr>
										</tbody>
									</table>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
	<?php
		else:
			header('location: ../frontend/login.php');
		endif;
	?>
</body>
</html>