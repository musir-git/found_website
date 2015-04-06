$(document).ready(function(){
		$(".showNameLink").mouseover(mouseOver);
		$(".showNameLink").mouseout(mouseOut);
		$("select").click(mouseClick);
		$("#queryButton").click(queryClick);
	}
)
function queryClick(){
	var fromFile = $("#hiddenThings").val();
	var text = $("#inputText").val();
	if (text.length>0){
		text = encodeURIComponent(text);
		$.post("query.php",{"file":fromFile,"query":text},function(data){
			var url = "train.php?things=./data/temp.txt";
			window.opener = null;
			window.open(url,"_top","");
		});
	}
}
function mouseOver(event){
	$(".showNameLink").css("color","#60f0f0");
}

function mouseOut(event){
	$(".showNameLink").css("color","black");
}

function mouseClick(event){
	$("select").click(mouseClick1);
}

function mouseClick1(event){
	var page = $("select").val();
	var url = "train.php?page="+page;
	window.open(url,"_top","");
	window.close();
}
