String.prototype.lTrim = function() {
    return this.replace(/(^[\s]*)/g, "");
}
//去除右空白
String.prototype.rTrim = function() {
    return this.replace(/([\s]*$)/g, "");
}
String.prototype.format = function(k) {
	a = this;
	for (k in arguments) {
	  a = a.replace("{" + k + "}", arguments[k])
	}
	return a
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
		$(".modify_a_qa_speech").on("click",function() {
			var button_id = $(this).attr('row')
			var b_check_id = $("#t2_b>tbody>tr")
			var b_exist = false
			for(i = 1;i < b_check_id.length;i ++){
				if(b_check_id[i].getAttribute("id_qa_speech") == button_id){
					b_exist = true
					break
				}
			}
			if(b_exist){
				return
			}
			var tab = $("tr[id_qa_speech='" + button_id + "']")[0]
			var tab_b = tab.cloneNode(true);
			tab_b.setAttribute("class","CaseRow_qa_speech");
			for(i = 0;i < 2;i ++){
				var lchind = tab_b.lastChild;
				tab_b.removeChild(lchind);
			}
			var td = document.createElement("td");
			var t = document.createTextNode("修改");
			td.appendChild(t);
			tab_b.insertBefore(td,tab_b.firstChild);

            var td = document.createElement("td");
			var t = document.createTextNode("");
            td.appendChild(t);
            tab_b.appendChild(td)

			var td = document.createElement("td");
			var a = document.createElement("a");
			var t = document.createTextNode("修改");
			a.setAttribute("class","modify_b_qa_speech");
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
			$('#t2_b').append(tab_b);
			$(".modify_b_qa_speech").off("click");
				$(".modify_b_qa_speech").on("click",function() {
					var button_id = $(this).attr('id');
					var tab=document.getElementById(button_id);			
					$('#t2_b').append(tab);//向table中追加tr
					if($(this).text() == "確定"){
						$(this).parent().siblings("td:eq(3)").each(function() {  // 获取当前行的第二列单元格
							obj_text = $(this).find("input:text");    // 判断单元格下是否有文本框
							// rule = obj_text.val();
						});	
						check_flag = check_remain();
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
					});}
				});
		});

	$(function(){
		$(".remove_a_qa_speech").click(function() {
			var button_id = $(this).attr('row');
			var b_check_id = $("#t2_b>tbody>tr")
			var b_exist = false
			for(i = 1;i < b_check_id.length;i ++){
				var b_child = b_check_id[i].childNodes
				if(b_check_id[i].getAttribute("id_qa_speech") == button_id){
					b_exist = true
					break
				}
			}
			if(b_exist){
				return
			}
			var tab = $("tr[id_qa_speech='" + button_id + "']")[0]
			var tab_b = tab.cloneNode(true);
			tab_b.setAttribute("class","CaseRow_qa_speech");
			for(i = 0;i < 4;i ++){
				var lchind = tab_b.lastChild;
				tab_b.removeChild(lchind);
            }
            var td = document.createElement("td");
			var t = document.createTextNode("");
            td.appendChild(t);
            tab_b.appendChild(td)

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
			$('#t2_b').append(tab_b);
		});
	});

	$('#determine_sql_qa_speech').on('click', function(){
		var obj_text = $("#t2_b").find("input:text");
		if(obj_text.length){
			alert("請將規則修改完畢後再按確認修改");
			return
		}
		var result_dict = Array();
		var df = $(".CaseRow_qa_speech");
		for(i = 0;i < df.length;i ++){
			var td_list = df[i].childNodes;
			var text_list = Array();
			for(j = 0;j < td_list.length;j ++){
				text_list.push(td_list[j].textContent);
			}
			result_dict[i] = text_list;
		}
		var result_json = JSON.stringify(result_dict);
		alert(result_json)
		sql_modify_call(result_json,owner);
	});

	var sql_modify_call = function(data,owner){
		$.ajax({
			method: "POST",
			url: "../cgi-bin/QA_speech_train_connect.py",
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
});
function check_remain(obj)
{
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