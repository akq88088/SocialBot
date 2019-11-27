<div class="container" id="qa_remain_transfer_dict_reload">
						<h6 class="my-4">保 留 字 字 典</h6>
						<div class="row">
							<div class="col-lg-12 btm-mg-1">
								<div class="alert alert-light radius-border project yellow-block" style="height:550px;overflow-y:auto" >
								    <div class="row">
									    <div class="col-lg-6" style="height:600px;overflow:auto;">
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
												echo "<table owner=$email_1 border='1' align='center' id='t1_1_a' class='table table-dark'><tr align='center'>";
												
												$link = create_connection();
												$sql = "SELECT ID,字詞,實體 FROM `qa_remain_transfer_dict` where `p_id` = '$p_id'";
												$mysql_class = execute_sql($link, "socialbot", $sql);
												$remain_transfer_dict = $mysql_class->fetch_all();
												if(!empty($remain_transfer_dict)){
												if(count($remain_transfer_dict) % 2 == 0){
													$remain_transfer_dict = array_chunk($remain_transfer_dict,count($remain_transfer_dict) / 2);
												}
												else{
													$remain_transfer_dict = array_chunk($remain_transfer_dict,count($remain_transfer_dict) / 2 + 1);
													
												}
												$result = $remain_transfer_dict[0];
												}
												else{
													$result = array();
												}
												$iRun = 1;
												
												while ($field = $mysql_class->fetch_field())   // 顯示欄位名稱
													{
													echo "<td>" . $field->name . "</td>";
													$iRun += 1;
													}
												echo "</tr>";
												$k=-1;
												for($i = 0;$i < count($result);$i ++)
												{
													$k++;
													echo "<tr id_qa_remain_transfer_dict='$k'>";
													for ($j = 0; $j < count($result[$i]); $j++)
													{
														echo "<td>" . $result[$i][$j] . "</td>";
													}
											?>
												<td><a class="remove_a_qa_remain_transfer_dict" row=<?php echo $k;?> href="javascript:;">刪除</a></td>
												<td><a class="modify_a_qa_remain_transfer_dict" row=<?php echo $k;?> href="javascript:;">修改</a></td>
											<?php		
													echo "</tr>";
												}
												echo "</table>";
											?>
									    </div>
										<div class="col-lg-6" style="height:600px;overflow:auto;">
											<?php
												$mysql_class = execute_sql($link, "socialbot", $sql);
												//表格內容
												echo "<table owner=$email_1 border='1' align='center' id='t1_2_a' class='table table-dark'><tr align='center'>";
												$iRun = 1;
												if(empty($remain_transfer_dict) || count($remain_transfer_dict) < 2){
													$result = array();
												}
												else{
													$result = $remain_transfer_dict[1];
												}
												while ($field = $mysql_class->fetch_field())   // 顯示欄位名稱
													{
													echo "<td>" . $field->name . "</td>";
													$iRun += 1;
													}
												echo "</tr>";
												for($i = 0;$i < count($result);$i ++)
												{
													$k++;
													echo "<tr id_qa_remain_transfer_dict='$k'>";
													for ($j = 0; $j < count($result[$i]); $j++)
													{
														echo "<td>" . $result[$i][$j] . "</td>";
													}
											?>
												<td><a class="remove_a_qa_remain_transfer_dict" row=<?php echo $k;?> href="javascript:;">刪除</a></td>
												<td><a class="modify_a_qa_remain_transfer_dict" row=<?php echo $k;?> href="javascript:;">修改</a></td>
											<?php		
													echo "</tr>";
												}
												echo "</table>";
											?>
									    </div>
									</div>
								</div>
								<h6 class="my-4">修 改 字 典</h6>
								<div class="alert alert-light radius-border project yellow-block">
									<?php
										echo "<table border='1' align='center' id='t1_b' class='table table-dark tabel-responsive'><tr class='CaseRow_qa_remain_transfer_dict' align='center' >";
										$link = create_connection();
										$sql = "SELECT ID,字詞,實體 FROM `qa_remain_transfer_dict` where `p_id` = '$p_id'";
										$mysql_class = execute_sql($link, "socialbot", $sql);
										echo "<td>datatype</td>";
										$iRun = 1;
										while ($field = $mysql_class->fetch_field())   // 顯示欄位名稱
											{
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