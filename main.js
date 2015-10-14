map = {};
var result = {};
var times = 0;
$(".examLi").each(function(){
	var qs_id = $(this).attr("qs_id");
	if(qs_id == undefined){
		return;
	}
	var liList = $(this).find("li[hash]");
	var hash = [];
	var i = 0;
	liList.each(function(){
		hash[i++] = $(this).attr("hash");
	});
	map[qs_id] = hash;
});
function answer(){
	$(".examLi").each(function(){
		var qs_id = $(this).attr("qs_id");
		if(qs_id == undefined){
			return;
		}
		var hash = result[qs_id];

		if(hash == undefined){
			return;
		}
		var answer = $(this).find("li[hash='"+hash+"']")[0];
		console.log(answer);
		$(answer).addClass('currSolution');
	});
}
var qs_ids = Object.keys(map).join();
function goPromotion(){
	var param = {'qs_ids': qs_ids};
	for(var key in map){
		if(!(key in result)){
			hash = map[key];
			result[key] = hash[times];
		}
		param["ans_hash_"+key] = result[key];
	};
	if(times >= 3){
		answer();
		return;
	}
	$.post('https://account.bilibili.com/answer/goPromotion', param, function(data) {
		times ++;
		data = $.parseJSON(data);
		success = data.status;
		if(!success){
			for(var j in data.message){
				delete result[data.message[j]];
			}
			console.log(Object.keys(result));
			goPromotion();
		} else {
			console.log("success");
			console.log(result);
			answer();
		}
	});
}
goPromotion();



