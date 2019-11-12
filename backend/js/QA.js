String.prototype.lTrim = function() {
    return this.replace(/(^[\s]*)/g, "");
}
//去除右空白
String.prototype.rTrim = function() {
    return this.replace(/([\s]*$)/g, "");
}
var article_remain = Array()
var que_remain = Array()
var flag_que_remain_dict = Array()
var boson_flag = Array()
var p_name = ""
var owner = ""
var content = "" 
var call_progress = ""
$(document).ready(function(){
	p_name = $("#project_name")[0].textContent
	owner = $("table,[owner]")[0].getAttribute("owner");
	const textUploader = document.querySelector('#QA_file');
	textUploader.addEventListener('change', function(e) {
		var reader = new FileReader();

		reader.onload = function(){
			content = ""
			content = reader.result;
		};

		reader.readAsText(e.target.files[0]);
	});
	$("#submit").on('click',function() {
		QA_upload(content);
	});
	var load_check_rule_data = function(){
		$.ajax({
			method: "POST",
			url: "../cgi-bin/get_check_rule_data.py",
			async: true, //非同步化
			// dataType:"json",
			data: {
				data:"data",
				"p_name":p_name
			},
			beforeSend:function(){
			},
			success: function(t){
				var data = JSON.parse(t)
				article_remain = data['article_remain']
				que_remain = data['que_remain']
				flag_que_remain_dict = data['flag_que_remain_dict']
				boson_flag = data['boson_flag']
			},
			complete:function(){
			}
		});
	}
	load_check_rule_data();//改放到前面?
	var QA_upload = function(data){
		$.ajax({
			method: "POST",
			url: "../cgi-bin/QA_upload_connect.py",
			async: true, //非同步化
			// dataType:"json",
			data: {
				"data":data,
				"owner":owner,
				"p_name":p_name
			},
			beforeSend:function(){
				// 送出前要做什麼
			},
			success: function(text){
				alert("檔案上傳完成!")
				window.location.reload();
				// 成功回傳後要做甚麼
			},
			complete:function(){
				// 全部執行完要做什麼
			}
		});
	}
	$("#rule").on('click',function() {
		rule_generate(owner,p_name)
	});
	var rule_generate = function(owner,p_name){
		$.ajax({
			method: "POST",
			url: "../cgi-bin/QA_rule_generate_connect.py",
			async: true, //非同步化
			// dataType:"json",
			data: {
				"owner" : owner,
				"p_name" : p_name
			},
			beforeSend:function(){
			},
			success: function(text){
				alert("規則產生完成!")
				window.location.reload();
			},
			complete:function(){
				
				// console.log("rule generate complete")
			}
		});
	}
	var call_rule_progress = function(owner,p_name){
		$.ajax({
			method: "POST",
			url: "../cgi-bin/QA_call_progress.py",
			async: true, //非同步化
			// dataType:"json",
			data: {
				"owner" : owner,
				"p_name" : p_name
			},
			beforeSend:function(){
				console.log('rule p run')
			},
			success: function(rate){
				console.log(rate)
			},
			complete:function(){
				console.log("rule progress complete")
			}
		});
	}
		$(".add_a").on('click',function() {
			var tr = "<tr class='CaseRow'><td>新增</td><td>-1</td><td></td><td></td><td></td><td>X</td><td>X</td><td>X</td><td><a class='modify_b' href='javascript:;'>修改</a></td><td><a href='javascript:;' onclick='cancel(this)'>取消</a></td></tr>";
			$('#t1').append(tr);//向table中追加tr
			$(".modify_b").off("click");
				$(".modify_b").on("click",function() {
					var button_id = $(this).attr('id');
					var tab=document.getElementById(button_id);			
					$('#t1').append(tab);//向table中追加tr
					if($(this).text() == "確定"){
						var rule = "";
						var que = "";
						var ans = "";
						$(this).parent().siblings("td:eq(2)").each(function() {  // 获取当前行的第二列单元格
							obj_text = $(this).find("input:text");    // 判断单元格下是否有文本框
							rule = obj_text.val();
						});	
						$(this).parent().siblings("td:eq(3)").each(function() {  // 获取当前行的第二列单元格
							obj_text = $(this).find("input:text");    // 判断单元格下是否有文本框
							que = obj_text.val();
						});	
						$(this).parent().siblings("td:eq(4)").each(function() {  // 获取当前行的第二列单元格
							obj_text = $(this).find("input:text");    // 判断单元格下是否有文本框
							ans = obj_text.val();
						});
						check_flag = check_rule(rule,que,ans);
						// check_flag = true
						if(check_flag){
							str = $(this).text()=="修改"?"確定":"修改";  
							$(this).text(str);   // 按钮被点击后，在“编辑”和“确定”之间切换
							$(this).parent().siblings("td:eq(2)").each(function() {  // 获取当前行的第二列单元格
								obj_text = $(this).find("input:text");    // 判断单元格下是否有文本框
								if(!obj_text.length)   // 如果没有文本框，则添加文本框使之可以编辑
									$(this).html("<input type='text' value='"+$(this).text()+"'>");
								else   // 如果已经存在文本框，则将其显示为文本框修改的值
									$(this).html(obj_text.val()); 
							});
							$(this).parent().siblings("td:eq(3)").each(function() {  // 获取当前行的第二列单元格
								obj_text = $(this).find("input:text");    // 判断单元格下是否有文本框
								if(!obj_text.length)   // 如果没有文本框，则添加文本框使之可以编辑
									$(this).html("<input type='text' value='"+$(this).text()+"'>");
								else   // 如果已经存在文本框，则将其显示为文本框修改的值
									$(this).html(obj_text.val()); 
							});
							$(this).parent().siblings("td:eq(4)").each(function() {  // 获取当前行的第二列单元格
								obj_text = $(this).find("input:text");    // 判断单元格下是否有文本框
								if(!obj_text.length)   // 如果没有文本框，则添加文本框使之可以编辑
									$(this).html("<input type='text' value='"+$(this).text()+"'>");
								else   // 如果已经存在文本框，则将其显示为文本框修改的值
									$(this).html(obj_text.val()); 
							
							});
						}
					}
					else{
					str = $(this).text()=="修改"?"確定":"修改";  
					$(this).text(str);   // 按钮被点击后，在“编辑”和“确定”之间切换
					$(this).parent().siblings("td:eq(2)").each(function() {  // 获取当前行的第二列单元格
						obj_text = $(this).find("input:text");    // 判断单元格下是否有文本框
						if(!obj_text.length)   // 如果没有文本框，则添加文本框使之可以编辑
							$(this).html("<input type='text' value='"+$(this).text()+"'>");
						else   // 如果已经存在文本框，则将其显示为文本框修改的值
							$(this).html(obj_text.val()); 
					});
					$(this).parent().siblings("td:eq(3)").each(function() {  // 获取当前行的第二列单元格
						obj_text = $(this).find("input:text");    // 判断单元格下是否有文本框
						if(!obj_text.length)   // 如果没有文本框，则添加文本框使之可以编辑
							$(this).html("<input type='text' value='"+$(this).text()+"'>");
						else   // 如果已经存在文本框，则将其显示为文本框修改的值
							$(this).html(obj_text.val()); 
					});
					$(this).parent().siblings("td:eq(4)").each(function() {  // 获取当前行的第二列单元格
						obj_text = $(this).find("input:text");    // 判断单元格下是否有文本框
						if(!obj_text.length)   // 如果没有文本框，则添加文本框使之可以编辑
							$(this).html("<input type='text' value='"+$(this).text()+"'>");
						else   // 如果已经存在文本框，则将其显示为文本框修改的值
							$(this).html(obj_text.val()); 
					
					});}
				});
		});
	

	
		$(".modify_a").on("click",function() {
			var button_id = $(this).attr('row')
			var b_check_id = $("#t1>tbody>tr")
			var b_exist = false
			for(i = 1;i < b_check_id.length;i ++){
				var b_child = b_check_id[i].childNodes
				if(b_check_id[i].id == button_id){
					b_exist = true
					break
				}
			}
			if(b_exist){
				return
			}
			var tab=document.getElementById(button_id);
			var tab_b = tab.cloneNode(true);
			tab_b.setAttribute("class","CaseRow");
			for(i = 0;i < 4;i ++){
				var lchind = tab_b.lastChild;
				tab_b.removeChild(lchind);
			}
			var td = document.createElement("td");
			var t = document.createTextNode("修改");
			td.appendChild(t);
			tab_b.insertBefore(td,tab_b.firstChild);

			var td = document.createElement("td");
			var a = document.createElement("a");
			var t = document.createTextNode("修改");
			a.setAttribute("class","modify_b");
			a.setAttribute("row",button_id);
			a.setAttribute("href","javascript:;")
			a.appendChild(t);
			td.appendChild(a);
			tab_b.appendChild(td)

			var td = document.createElement("td");
			var a = document.createElement("a");
			var t = document.createTextNode("取消");
			a.setAttribute("class","cancel");
			a.setAttribute("row",button_id);
			a.setAttribute("href","javascript:;")
			a.setAttribute("onclick","cancel(this)")
			a.appendChild(t);
			td.appendChild(a);
			tab_b.appendChild(td)
			$('#t1').append(tab_b);
			$(".modify_b").off("click");
				$(".modify_b").on("click",function() {
					var button_id = $(this).attr('id');
					var tab=document.getElementById(button_id);			
					$('#t1').append(tab);//向table中追加tr
					if($(this).text() == "確定"){
						var rule = "";
						var que = "";
						var ans = "";
						$(this).parent().siblings("td:eq(2)").each(function() {  // 获取当前行的第二列单元格
							obj_text = $(this).find("input:text");    // 判断单元格下是否有文本框
							// rule = obj_text.val();
							rule = $(this).text()
						});	
						$(this).parent().siblings("td:eq(3)").each(function() {  // 获取当前行的第二列单元格
							obj_text = $(this).find("input:text");    // 判断单元格下是否有文本框
							que = obj_text.val();
						});	
						$(this).parent().siblings("td:eq(4)").each(function() {  // 获取当前行的第二列单元格
							obj_text = $(this).find("input:text");    // 判断单元格下是否有文本框
							ans = obj_text.val();
						});
						check_flag = check_rule(rule,que,ans);
						// check_flag = true
						if(check_flag){
							str = $(this).text()=="修改"?"確定":"修改";  
							$(this).text(str);   // 按钮被点击后，在“编辑”和“确定”之间切换
							$(this).parent().siblings("td:eq(3)").each(function() {  // 获取当前行的第二列单元格
								obj_text = $(this).find("input:text");    // 判断单元格下是否有文本框
								if(!obj_text.length)   // 如果没有文本框，则添加文本框使之可以编辑
									$(this).html("<input type='text' value='"+$(this).text()+"'>");
								else   // 如果已经存在文本框，则将其显示为文本框修改的值
									$(this).html(obj_text.val()); 
							});
							$(this).parent().siblings("td:eq(4)").each(function() {  // 获取当前行的第二列单元格
								obj_text = $(this).find("input:text");    // 判断单元格下是否有文本框
								if(!obj_text.length)   // 如果没有文本框，则添加文本框使之可以编辑
									$(this).html("<input type='text' value='"+$(this).text()+"'>");
								else   // 如果已经存在文本框，则将其显示为文本框修改的值
									$(this).html(obj_text.val()); 
							
							});
						}
					}
					else{
					str = $(this).text()=="修改"?"確定":"修改";  
					$(this).text(str);   // 按钮被点击后，在“编辑”和“确定”之间切换
					$(this).parent().siblings("td:eq(3)").each(function() {  // 获取当前行的第二列单元格
						obj_text = $(this).find("input:text");    // 判断单元格下是否有文本框
						if(!obj_text.length)   // 如果没有文本框，则添加文本框使之可以编辑
							$(this).html("<input type='text' value='"+$(this).text()+"'>");
						else   // 如果已经存在文本框，则将其显示为文本框修改的值
							$(this).html(obj_text.val()); 
					});
					$(this).parent().siblings("td:eq(4)").each(function() {  // 获取当前行的第二列单元格
						obj_text = $(this).find("input:text");    // 判断单元格下是否有文本框
						if(!obj_text.length)   // 如果没有文本框，则添加文本框使之可以编辑
							$(this).html("<input type='text' value='"+$(this).text()+"'>");
						else   // 如果已经存在文本框，则将其显示为文本框修改的值
							$(this).html(obj_text.val()); 
					
					});}
				});
		});

	$(function(){
		$(".remove_a").click(function() {
			var button_id = $(this).attr('row');
			var b_check_id = $("#t1>tbody>tr")
			var b_exist = false
			for(i = 1;i < b_check_id.length;i ++){
				var b_child = b_check_id[i].childNodes
				if(b_check_id[i].id == button_id){
					b_exist = true
					break
				}
			}
			if(b_exist){
				return
			}
			var tab=document.getElementById(button_id);
			var tab_b = tab.cloneNode(true);
			tab_b.setAttribute("class","CaseRow");
			for(i = 0;i < 4;i ++){
				var lchind = tab_b.lastChild;
				tab_b.removeChild(lchind);
			}
			var td = document.createElement("td");
			var t = document.createTextNode("刪除");
			td.appendChild(t);
			tab_b.insertBefore(td,tab_b.firstChild);
			var td = document.createElement("td");
			var a = document.createElement("a");
			var t = document.createTextNode("取消");
			a.setAttribute("row",button_id);
			a.setAttribute("href","javascript:;");
			a.setAttribute("onclick","cancel(this)");
			a.appendChild(t);
			td.appendChild(a);
			tab_b.appendChild(td)
			$('#t1').append(tab_b);
		});
	});

	$('#determine_sql').on('click', function(){
		var obj_text = $("#t1").find("input:text");
		if(obj_text.length){
			alert("請將規則修改完畢後再按確認修改");
			return
		}
		var result_dict = Array();
		var df = $(".CaseRow");
		for(i = 0;i < df.length;i ++){
			var td_list = df[i].childNodes;
			var text_list = Array();
			for(j = 0;j < td_list.length;j ++){
				text_list.push(td_list[j].textContent);
			}
			result_dict[i] = text_list;
		}
		var result_json = JSON.stringify(result_dict);
		sql_modify_call(result_json,owner);
	});

	var sql_modify_call = function(data,owner){
		$.ajax({
			method: "POST",
			url: "../cgi-bin/QA_train_connect.py",
			async: true, //非同步化
			// dataType:"json",
			data: {
				"data" : data,
				"owner" : owner,
				"p_name" : p_name
			},
			beforeSend:function(){
			},
			success: function(text){
				window.location.reload();
			},
			complete:function(){
				// window.location.reload();
			}
		});
	}
	$("#remove_qa_training").on('click',function() {
		remove_qa_training(owner,p_name)
	});
	var remove_qa_training = function(owner,p_name){
		$.ajax({
			method: "POST",
			url: "../cgi-bin/QA_remove_qa_training.py",
			async: true, //非同步化
			// dataType:"json",
			data: {
				"owner" : owner,
				"p_name" : p_name
			},
			beforeSend:function(){
			},
			success: function(text){
				alert("訓練資料刪除完成!")
				window.location.reload();
			},
			complete:function(){
				
				// console.log("rule generate complete")
			}
		});
	}
	$("#remove_qa_rule").on('click',function() {
		remove_qa_rule(owner,p_name)
	});
	var remove_qa_rule = function(owner,p_name){
		$.ajax({
			method: "POST",
			url: "../cgi-bin/QA_remove_qa_rule.py",
			async: true, //非同步化
			// dataType:"json",
			data: {
				"owner" : owner,
				"p_name" : p_name
			},
			beforeSend:function(){
			},
			success: function(text){
				alert("規則刪除完成!")
				window.location.reload();
			},
			complete:function(){
				
				// console.log("rule generate complete")
			}
		});
	}
});
function test(temp)
{
console.log(que_remain)
console.log(article_remain)
}
function is_ch(temp)
{
var re=/[^/u4e00-/u9fa5]/;
if (re.test(temp)) return false ;
return true ;
}
function is_que_remain(temp)
{
temp = remove_number(temp)
var result = false
for(i = 0;i < que_remain.length;i ++){
	if(que_remain[i] == temp){
		result = true
		break
	}
}
return result
}
function is_article_remain(temp)
{
temp = remove_number(temp)
var result = false
for(i = 0;i < article_remain.length;i ++){
	if(article_remain[i] == temp){
		result = true
		break
	}
}
return result
}
function is_boson_flag(temp)
{
temp = remove_number(temp)
var result = false
for(i = 0;i < boson_flag.length;i ++){
	if(boson_flag[i] == temp){
		result = true
		break
	}
}
return result
}
function is_number(data)
{
if(isNaN(data)){
  return false
}
else{
  return true
}
}
function remove_number(word)
{
var s = ""
for(j=0;j<word.length;j++){
  if(is_number(word.substring(j,j+1))){
    continue;
  }
  s += word.substring(j,j+1)
}
return s
}
function p_flag_sort_check(data)
{
flag_num_dict = Array()
result = Array()
article_list = Array()
data = data.split("+")
for(i=0;i<data.length;i ++){
  data[i] = data[i].lTrim().rTrim()
}
ori_rule = data.join(" + ")
var flag = ""
for(i=0;i<data.length;i ++){
  flag = data[i]
  flag_no_num = remove_number(flag)
  temp = flag_num_dict[flag_no_num]
  if(typeof temp === "undefined"){
    flag_num_dict[flag_no_num] = 2
    flag = flag_no_num + '1'
  }
  else{
    flag = flag_no_num + flag_num_dict[flag_no_num].toString()
    flag_num_dict[flag_no_num] += 1
  }
  data[i] = flag
}
new_rule = data.join(" + ")
if(ori_rule != new_rule){
  alert("請給每個字正確的編號，規則應該要看起來像這樣 : " + new_rule)
  return false
}
else{
  return true
}
}
function check_rule(rule,que,ans)
{
var rule_list = rule.split("+");
var que_list = que.split("+");
for(i = 0;i < rule_list.length;i ++){
  rule_list[i] = rule_list[i].lTrim().rTrim()
  var temp = rule_list[i]
  temp = remove_number(temp)
  if(!is_boson_flag(temp) && !is_article_remain(temp)){
	alert("規則只能填入boson的詞性標記或是文章保留字");
	return false
  }
}
for(i = 0;i < que_list.length;i ++){
  que_list[i] = que_list[i].lTrim().rTrim()
  var temp = que_list[i]
  temp = remove_number(temp)
  if(!is_boson_flag(temp) && !is_que_remain(temp)){
	alert("規則只能填入boson的詞性標記或是出題保留字");
	return false
  }
}
if(rule_list.length <= 1 || que_list.length <= 1){
  alert("請以加號隔開字詞");
  return false
}
if(!p_flag_sort_check(rule)){
  return false
}
var error = true;
for(i = 0;i < article_remain.length;i ++){
  var temp = rule.search(article_remain[i])
  if(temp != -1){
     error = false
     break
  }
}
if(error){
  alert("規則裡必須包含文章保留字")
  return false
}
error = true;
for(i = 0;i < que_remain.length;i ++){
  var temp = que.search(que_remain[i])
  if(temp != -1){
     error = false
     break
  }
}
if(error){
  alert("問題規則裡必須包含出題保留字")
  return false
}
var temp = rule.search(ans)
if(temp == -1){
  alert("答案必須是規則裡的文章保留字")
  error = true
}
if(error)
  return false
return true
}
function cancel(obj)
{
	var isDelete=confirm("確定要取消該筆資料的變動嗎？");
	if(isDelete)
	{
		var tr=obj.parentNode.parentNode;
		var tbody=tr.parentNode;
		tbody.removeChild(tr);
	}
}
function get_p_name()
{
return "a"
}