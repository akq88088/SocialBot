
<div class="container" id="qa_reload">
						<h6 class="my-4">出 題 規 則</h6>
						<div class="row">
							<div class="col-lg-12 btm-mg-1">
								<div class="alert alert-light radius-border project yellow-block" style="height:550px;overflow-y:auto" >
								<?php
									session_start();
									require_once("dbtools.inc.php");
		
									//使用 isset()方法，判別有沒有此變數可以使用，以及為已經登入
									if(isset($_SESSION['is_login']) && $_SESSION['is_login'] == TRUE){
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
									}
									//表格內容
									echo "<table owner=$email_1 border='1' align='center' id='t_a' class='table table-dark'><tr align='center'>";
									$iRun = 0;
									$result = execute_sql($link, "socialbot", $sql);
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
										echo "<table border='1' align='center' id='t_b' class='table table-dark tabel-responsive'><tr class='CaseRow' align='center' >";
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