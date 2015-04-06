<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8"/>
		<title>你的东西还没找到吗？</title>
		<link href="lost.css" type="text/css" rel="stylesheet"/>
		<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.0/jquery.min.js"></script>
		<script src="lost.js" type="text/javascript"></script>
	</head>
	<?php
		@$things = $_REQUEST["things"];
		if (!isset($things))
			$things = "./data/lost.txt";
		$file = file($things);
		$lines = count($file);
		$needPage = count($file)/120;
		$needPage1 = (int)$needPage;
		if ($needPage-$needPage1>0)
			$needPage = $needPage1+1;
		else
			$needPage = $needPage1;
		@$thisPage = $_REQUEST["page"];
		if (!isset($thisPage) || $thisPage==null || $thisPage=="null")
			$thisPage = 1;
	?>
	<body>
		<input type="hidden" class="things" id="hiddenThings" value="<?= $things ?>"/>
		<div class="showBigDiv">
			<div class="showLeftDiv">						<!--设置在左边边框和内容的显示-->
				<div class="showFindLink">
					<a class="showLink" href="find.php">@失物招领</a>
				</div>
				<div class="showFindLink">
					<a class="showLink" href="train.php">@返回主页</a>
				</div>
				<div class="showFindLink">
					<a class="showLink" href="lost.php?things=./data/lostClasses/campuscard.txt">##校园卡</a>
				</div>
				<div class="showFindLink">
					<a class="showLink" href="lost.php?things=./data/lostClasses/key.txt">##钥匙</a>
				</div>
				<div class="showFindLink">
					<a class="showLink" href="lost.php?things=./data/lostClasses/IDcard.txt">##身份证</a>
				</div>
				<div class="showFindLink">
					<a class="showLink" href="lost.php?things=./data/lostClasses/bankcard.txt">##银行卡</a>
				</div>
				<div class="showFindLink">
					<a class="showLink" href="lost.php?things=./data/lostClasses/flashdisk.txt">##U盘</a>
				</div>
				<div class="showFindLink">
					<a class="showLink" href="lost.php?things=./data/lostClasses/wallet.txt">##钱包</a>
				</div>
				<div class="showFindLink">
					<a class="showLink" href="lost.php?things=./data/lostClasses/cellphone.txt">##手机</a>
				</div>
				<div class="showFindLink">
					<a class="showLink" href="lost.php">##当前所有信息</a>
				</div>
			</div>
			
			<div class="showCenterDiv">					<!--设置在中间，中间边框和内容信息的显示-->
			<br/>
			<div style="color:red;margin-bottom:10px;">
				寻物启事
			</div>
			<div class="showMessage">
				<textarea id="inputText" rows="5" cols="60"></textarea>
				<br/><br/>
				<button style="float:right" type="button" id="queryButton">查询</button>
			</div>
			<?php
				$i=$thisPage*120-120;
				$endI = $i+120;
				for (;$i<$endI && $i<$lines;$i=$i+6)
				{
			?>
				<div class="showMessage">					<!--显示一条信息-->
					<div class="showHeadImage">									<!--显示头像-->
						<a href="<?= $file[$i+2] ?>"><img src="<?= $file[$i+5] ?>" alt="headphoto"/></a>
					</div>
					<div class="showContent">
						<a class="showNameLink" href="<?= $file[$i+2] ?>">		<!--显示名称-->
							<?= $file[$i+1] ?>
						</a>
						<p>									<!--显示内容-->
							<?= $file[$i+3] ?>
						</p>
						<?php
							if (strlen($file[$i+4])>5)
							{
						?>
						<p>									<!--显示图片-->
							<?php
								$slid = explode("/",$file[$i+4]);
								$slid[count($slid)-2] = "bmiddle";
								$newPicture = implode("/",$slid);
							?>
							<a href="<?= $newPicture ?>"><img src="<?= $file[$i+4] ?>" alt="photo"/></a>
						</p>
						<?php
							}
						?>
						<p>									<!--显示时间-->
							<?= $file[$i] ?>
						</p>
					</div>
				</div>
			<?php
				}
			?>
				<!--显示下一页-->
				<div class="showNextPage">
					<?php
						if ($thisPage>=2)
						{
					?>
					<a href="lost.php?page=<?= ($thisPage-1)."&amp;things=".$things ?>">上一页</a>
					<?php
						}
					?>
					<?php
						if ($thisPage+1<=$needPage)
						{
					?>
					<a href="lost.php?page=<?= ($thisPage+1)."&amp;things=".$things ?>">下一页</a>
					<?php
						}
					?>
					<select name="nextPage">
					<?php
						for ($ii=1;$ii<=$needPage;$ii++)
						{
							if ($ii != $thisPage)
							{
					?>
						<option value="<?= $ii."&amp;things=".$things ?>">第<?= $ii ?>页</option>
					<?php
							}
							else
							{
					?>
						<option value="<?= $ii."&amp;things=".$things ?>" selected="selected">第<?= $ii ?>页</option>
					<?php
							}
						}
					?>
					</select>
				</div>
			</div>
		</div>
		
	</body>
</html>
