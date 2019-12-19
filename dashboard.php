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
	<link rel="stylesheet" href="css/global.css">
	<link rel="stylesheet" href="css/dashboard.css">
	<!-- JQuery -->
	<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" crossorigin="anonymous"></script>
	<script src="http://code.jquery.com/jquery-3.3.1.min.js" crossorigin="anonymous"></script>
	<!-- Bootstrap JS -->
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" crossorigin="anonymous"></script>
	
	<!-- Chart JS -->
	<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.2/Chart.min.js"></script>
	
	<!-- Customer JS -->
	<script src="./js/global.js" crossorigin="anonymous"></script>	
	<script src="./js/dashboard.js" crossorigin="anonymous"></script>
	
	<!--Read .docx JS-->
	<script src="https://cdnjs.cloudflare.com/ajax/libs/docxtemplater/3.1.9/docxtemplater.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/2.6.1/jszip.js"></script>

	<script>
		function toLogout() {
			window.location.replace("../frontend/Logout.php")
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
			$link = create_connection();
			$p_name = mysqli_real_escape_string($link, $_GET['name']);
			$sql = "SELECT `project-name` FROM `member` INNER JOIN `project` WHERE `member_id` = `ID` and `project-name` = '$p_name'";
			$result = execute_sql($link, "social_bot", $sql);
			//$_SESSION['p_id'] = $result->fetch_assoc()['p_id'];
			
			$sql_model = "SELECT `p_name` FROM `model`";
			$result_model = execute_sql($link, "social_bot", $sql_model);
			
			$j=0;
			while ($row = $result_model->fetch_row()) 
			{
				for ($i = 0; $i < $result_model->field_count; $i++)
					$model[$j] = $row[$i];
				$j++;
			}
	?>
	
	<!-- header -->
	<div class="container-fluid header">
		<div class="row">
			<div class="col-md-1 ta-c" id="back" role="button">< 返回</div>
			<div class="col-md-4 offset-md-3 ta-c" id="title"><h5>語 料 應 用 與 分 析 工 具</h5></div>
			<div class="col-md-2 offset-md-1 ta-c" id="email"><?php echo $email;?></div>
			<div class="col-md-1 ta-c" id="logout" role="button" onclick="toLogout();">登出</div>
		</div>	
	</div>

	<!-- Page Content -->
	<div class="container">
			<div class="row">
				<div class="col-md-2">
					<h5 class="my-5" id='project_name'><?php echo $_GET['name'];?></h1>
				</div>
				<div class="col-md-1 offset-md-9">
					<button class="btn my-5" id="report" name=<?php echo $_GET['name'] ?>>問題回報</button>
				</div>
			</div>
		
		<!-- 匯入資料 -->
	
		<div class="container">
			<div>
				<h6 class="my-4">匯 入 資 料</h6>
			</div>
			<div class="alert alert-light radius-border blue-block" id="import">
				<div class="row">
					<div class="col-lg-6">
						<p>選擇文字模型</p>
						<div>
							<select class="form-control blue-border" name="model_select" id="model_select" >
								<option disabled selected hidden>請選擇模型</option>
								<?php
									while($j--)
									{?>
										<option><?php echo $model[$j];?></option>
								<?php } ?>
							</select>
						</div>
					</div>
					<div class="col-lg-6">
						<p>貼上文字內容</p>
						
						<div class="form-group">
							<textarea class="form-control blue-border radius-border" id="paste_text" rows="12" placeholder='請以 ! ? 。作為一句話結尾&#13&#10例如 : "今天天氣很好，所以我想出去玩。"'></textarea>
						</div>
						
						<p>上傳檔案</p>
						<div class="form-group">
							<input type="file" class="form-control-file" id="upload_text" accept=".txt,.csv,.docx">
						</div>
						
						<div class="row">
							<div class="col-md-12 ta-r">
								<button type="submit" class="btn radius-border" id="analyze">分析</button>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>


		<!-- 文本摘要與情感分析 -->
		<div class="container" id="TextSum_and_SA">
			<div>
				<h6 class="my-4">摘 要 與 情 緒 分 析</h6>	
			</div>
			<div class="alert alert-light radius-border red-block" >
				<div class="row">
					<div class="col-lg-6">
						<div class="btm-mg">
							<label>摘要演算法模型</label><br>
							<div class="btn-group" role="group"">
								<button class="btn red-border active" id="textsim">相似度</button>
								<button class="btn red-border" id="textrank">TextRank</button>
								<button class="btn red-border" id="textmap">主題地圖</button>
							</div>
						</div>

						<div class="btm-mg">
							<label>摘要比例</label><br>
							<div class="btn-group" role="group">
								<button class="btn red-border" percentage="0.2">20%</button>
								<button class="btn red-border" percentage="0.3">30%</button>
								<button class="btn red-border active" percentage="0.4">40%</button>
								<button class="btn red-border" percentage="0.5">50%</button>
							</div>
						</div>

						<div class="form-group">
							<textarea class="form-control radius-border red-border" id="summary" rows="12">
								
							</textarea>
						</div>
					</div>
					<div id="sentimentResult" class='col-lg-6 btm-mg'>
						<canvas id="sentimentBar">
						</canvas>
						<div id="pics"></div>
					</div>
				</div>
			</div>
		</div>


		<!-- 出題答案 -->
		<div class="container" id="QA">
			<div>
				<h6 class="my-4">出 題 答 案</h6>	
			</div>
			<div class="alert alert-light radius-border orange-block">
				<div class="row">
					<div class="col-md-6 btm-mg">
						<label>問題 : </label>
						<span>Lorem ipsum dolor sit amet, consectetur adipiscing elit?</span>
						<br>
						<label>答案 : </label>
						<span>Lorem ipsum dolor sit amet.</span>
					</div>
					<div class="col-md-6 btm-mg">
						<label>問題 : </label>
						<span>Lorem ipsum dolor sit amet, consectetur adipiscing elit?</span>
						<br>
						<label>答案 : </label>
						<span>Lorem ipsum dolor sit amet.</span>
					</div>
				</div>

				<div class="row">
					<div class="col-md-6 btm-mg">
						<label>問題 : </label>
						<span>Lorem ipsum dolor sit amet, consectetur adipiscing elit?</span>
						<br>
						<label>答案 : </label>
						<span>Lorem ipsum dolor sit amet.</span>
					</div>
					<div class="col-md-6 btm-mg">
						<label>問題 : </label>
						<span>Lorem ipsum dolor sit amet, consectetur adipiscing elit?</span>
						<br>
						<label>答案 : </label>
						<span>Lorem ipsum dolor sit amet.</span>
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
	<input id="help_session" type="hidden" value="<?php echo $_SESSION["member_id"] ?>"></input>
</body>
</html>