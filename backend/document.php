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
	<!-- CustomScrollbar CSS -->
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/malihu-custom-scrollbar-plugin/3.1.5/jquery.mCustomScrollbar.min.css">
	<!-- Customer CSS -->
	<link rel="stylesheet" href="../frontend/css/global.css">
	<link rel="stylesheet" href="../frontend/css/project.css">
	<link rel="stylesheet" href="./css/button.css">
	<!-- JQuery -->
	<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" crossorigin="anonymous"></script>
	<script src="http://code.jquery.com/jquery-3.3.1.min.js" crossorigin="anonymous"></script>
	<!-- Bootstrap JS -->
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" crossorigin="anonymous"></script>
	<!-- Customer JS -->
	<script src="../frontend/js/global.js" crossorigin="anonymous"></script>
	
	<script>
		function toLogout() {
			window.location.replace("../frontend/Logout.php")
		}
	</script>
	
	<title>出題問答後台教學手冊</title>
</head>
<html>
<body>
	<!-- header -->
	<div class="container-fluid header">
		<div class="row">
			<div class="col-md-1 ta-c" id="back" role="button">< 返回</div>
			<div class="col-md-4 offset-md-3 ta-c" id="title"><h5>語 料 應 用 與 分 析 工 具</h5></div>
			<div class="col-md-1 ta-c" id="logout" role="button" onclick="toLogout();">登出</div>
		</div>
	</div>
	<div><font size='5'>命名實體與情緒辨識上傳檔案格式</font></div><!--subtitle-->
	<div>包含一篇以上文章的txt、word或csv格式的檔案</div>
    <div><font size='5'>出題問答上傳檔案格式</font></div><!--subtitle-->
    <div>為包含兩欄的csv格式檔案</div>
    <div>第一欄原文句子為拿來出題的語句</div>
    <div>第二欄原文出題為針對該語句的出題</div>
    <img src='../cgi-bin/module/QA_data/出題問答檔案.png'>
    <br><br>
    <div><font size='5'>出題問答保留字字典上傳檔案格式</font></div><!--subtitle-->
    <div>為包含兩欄的csv格式檔案</div>
    <div>第一欄字詞為單一字詞</div>
    <div>第二欄實體為該字詞對應的實體</div>
    <img src='../cgi-bin/module/QA_data/保留字字典檔案.png'>
    <br><br>
    <div><font size='5'>出題問答規則修改規範</font></div><!--subtitle-->
    <div>規則格式:規則的格式為以” + ”號隔開每個字詞、實體和出題保留字，字詞與實體必須在後面加上數字</div>
    <div>，保留字則不需加上數字，該數字代表這個詞在句子中出現第幾次(Ex 誰 + v + v =>誰 + v1 + v2)。</div>
    <div>新增與修改規則時需滿足以下條件:</div>
    <div>(1)原文規則必須至少包含一個實體(Ex.人、物、地、時)</div>
    <div>(2)原文出題規則必須至少包含一個出題保留字(Ex.誰、什麼、哪裡)且該出題保留字必須對應到原文規則的實體對應關係可參考下圖</div>
    <div>    、實體與出題保留字匹配，第一行為各個實體，該行實體下面的資料，實體人對應的出題保留字為什麼人與哪裡。</div>
    <div>(3)原文出題規則答案必須為實體，該實體在原文規則有出現，且其對應的出題保留字有在原文出題規則出現。 </div>
    <img src='../cgi-bin/module/QA_data/實體與出題保留字匹配.png'>
　</body>
</html>