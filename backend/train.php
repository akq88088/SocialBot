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
	<link rel="stylesheet" href="./css/button.css">
	<link rel="stylesheet" href="./css/emotion_recognition.css">
	<link rel="stylesheet" href="./css/NER.css">
	<!-- JQuery -->
	<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" crossorigin="anonymous"></script>
	<script src="http://code.jquery.com/jquery-3.3.1.min.js" crossorigin="anonymous"></script>
	<!-- Bootstrap JS -->
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" crossorigin="anonymous"></script>
	<!-- Customer JS -->
	<script src="./js/train.js" crossorigin="anonymous"></script>
	<script src="./js/NER.js"></script>
	<script src="./js/emotion_recognition.js"></script>
	<script src="./js/QA.js"></script>
	
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
			$email_1 = hash('md5',$email);
			$link = create_connection();
			$p_name = mysqli_real_escape_string($link, $_GET['name']);
			$sql = "SELECT * FROM model WHERE p_name='$p_name'";
			$result = execute_sql($link, "socialbot", $sql);
			$_SESSION['p_id'] = $result->fetch_assoc()['p_id'];
			$p_id = $_SESSION['p_id'];
			$link = create_connection();
			$sql = "SELECT * FROM `qa_rule` where `p_id` = '$p_id'";
			$result = execute_sql($link, "socialbot", $sql);
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
				<div>
					<div class="row">
						<div class="col-md-2">
							<h5 class="my-5" id='project_name' pid=<?php echo $_SESSION['p_id'];?>><?php echo $_GET['name'];?></h1>
						</div>
					</div>
				</div>
				<div id="QA" class="collapse show">
					<div class="container">
						<h6 class="my-4">匯 入 資 料</h6>
						<div class="row">
							<div class="col-lg-12 btm-mg-1">
								<div class="radius-border project blue-block">
									<p><label for="inputfile">上傳檔案</label><P>
									<P><input type="file" id="QA_file"></p>
									<div class="col-md-2 offset-md-10">
										<button class="btn radius-border" id="submit">開始訓練</button>
										<button class="btn radius-border" id="rule">產生規則</button>
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
								<?php
				
									//表格內容
									echo "<table owner=$email_1 border='1' align='center' id='table' class='table table-dark'><tr align='center'>";
									$iRun = 0;
									while ($field = $result->fetch_field())   // 顯示欄位名稱
										{
										if($iRun == 1 || $iRun == 2){
											$iRun += 1;
											continue;
										}
										echo "<td>" . $field->name . "</td>";
										$iRun += 1;
										}
									echo "</tr>";
									$j=-1;
									while ($row = $result->fetch_row())
									{
										$j++;
										echo "<tr id='$j'>";
										$iRun = 0;
										for ($i = 0; $i < $result->field_count; $i++)
										{
											if($iRun == 1 || $iRun == 2){
												$iRun += 1;
												continue;
											}
											$a[$j][$i] = $row[$i];
											echo "<td>" . $a[$j][$i] . "</td>";
											$iRun += 1;
										}
								?>
									<td><a class="remove_a" row=<?php echo $j;?> href="javascript:;">刪除</a></td>
									<td><a class="modify_a" row=<?php echo $j;?> href="javascript:;">修改</a></td>
								<?php		
										echo "</tr>";
									}
									echo "</table>";
								?>
								</div>
								<h6 class="my-4">修 改 規 則</h6>
								<div class="alert alert-light radius-border project yellow-block">
									<?php
										echo "<table border='1' align='center' id='t1' class='table table-dark tabel-responsive'><tr class='CaseRow' align='center' >";
										$result = execute_sql($link, "socialbot", $sql);
										echo "<td>datatype</td>";
										$iRun = 0;
										while ($field = $result->fetch_field())   // 顯示欄位名稱
											{
											if($iRun == 1 || $iRun == 2){
												$iRun += 1;
												continue;
											}
											echo "<td>" . $field->name . "</td>";
											$iRun += 1;
											}
										echo "</tr>";
										echo "</table>";
									?>
								</div>
							</div>
						</div>
					</div>
					<a class="add_a" href="javascript:;">新增一列</a>
					<a href='javascript:;' id='determine_sql'>
					確定修改
					</a>
					<br><br><br><br><br>
				</div>
				<div id="NER" class="collapse">
					<div class="container">
						<h6 class="my-4">匯 入 資 料</h6>
						<div class="row">
							<div class="col-lg-12 btm-mg-1">
								<div class="radius-border project blue-block">
									<p><label for="inputfile">上傳檔案</label></p>
									<p><input type="file" id="ner_file"></p>
									<div class="col-md-2 offset-md-10">
										<button class="btn radius-border train" id="train_ner">開始訓練</button>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div class="container">
						<h6 class="my-4">實 體 辨 識 結 果</h6>
						<div class="alert alert-light radius-border darkblue-block" id="import">
							<div class="row">
								<div class="col-lg-6" style="max-height:600px;overflow:auto;">
									<p>原文</p>
									<textarea class="form-control blue-border radius-border" id="context" disabled="disabled" rows="12"></textarea>
								</div>
								<div class="col-lg-6" style="max-height:600px;overflow:auto;">
									<p>字詞屬性標記</p>
									<table class="table" id="NER_result">
										<thead>
											<tr>
												<th><span class="glyphicon glyphicon-font"></span> 字詞</th>
												<th><span class="glyphicon glyphicon-list"></span> 詞性</th>
												<th><span class="glyphicon glyphicon-list"></span> 實體</th>
											</tr>
										</thead>
										<tbody>
											<tr>
												<td>大自然</td>
												<td>n</td>
												<td>人</td>
											</tr>
											<tr>
												<td>會</td>
												<td>v</td>
												<td></td>
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
									<P><input type="file" id="upload_text" accept=".txt,.csv"></p>
									<div class="col-md-2 offset-md-10">
										<button class="btn radius-border train" id="train">開始訓練</button>
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
													<td>高興</td>
												</tr>
												<tr>
													<td>小山羊到河邊喝水</td>
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