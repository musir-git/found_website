<?php
	$filePath = $_REQUEST["file"];
	$text = $_REQUEST["query"];
	$file = file($filePath);
	$text = urldecode($text);
	$st = "";
	$isAll = false;
	$i = 3;
	if (strpos($filePath,"allClasses")>0 || strpos($filePath,"weibo.txt")>0){
		$isAll = true;
		$i = 4;
	}
	$n = count($file);
	$result = array();
	for (;$i<$n;$i+=6){
		//print $file[$i]."<br/>";
		//$temp = strspn($file[$i],$text);
		similar_text($file[$i],$text,$temp);
		if ($temp>0)
			$result[$i.""] = $temp;
	}
	arsort($result);
	//file_put_contents("./data/temp.txt","");
	
	$allKeys = array_keys($result);
	foreach ($allKeys as $k){
		$k = (int)$k;
		$k1 = $k+3;
		for ($i=$k-3;$i<$k1;$i++){
			$st = $st.$file[$i];
		}
	}
	file_put_contents("./data/temp.txt",$st);
?>