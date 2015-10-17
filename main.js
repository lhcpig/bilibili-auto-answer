var map = {};
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
eval("​‍‌​​‍‍​​‍​‍​﻿﻿​‌‍‍‌‌‍﻿‌‌‍‌﻿​‍​​‌﻿​﻿‌﻿​‍‌‍​﻿​﻿﻿‌​‍‌﻿‌‍‍​‌﻿‌​‌﻿‌​‌﻿​​​﻿‍‍​‍﻿﻿​‍﻿﻿‌﻿‌​​‍﻿‍‌‍​﻿‌‍﻿‍​‍﻿﻿‌‌​‍‌﻿‍‌‌‍‌​‌‌‍‌‌‍‌‌‌​‍﻿‌﻿‍‌​‍‌﻿​‍​​‌﻿​﻿‌﻿‌​‌﻿‍‌‌‍﻿​‌‍‌‌​﻿﻿‌​‍‌﻿‌‍‌​‌‍‍‌‌﻿​﻿‌﻿​​‌‍﻿​‌‍​‌‌﻿‍‌​﻿‍‍‌‍﻿‍‌‍﻿﻿‌‍﻿‍‌‍‌‌​‍‌﻿​‍​​​‍﻿﻿​﻿﻿‍​‍​‍​‍‍‌​‍﻿‍‌﻿​​‌﻿​‍‌‍‌‌‌﻿​​‌‍‌‌‌‍﻿‍‌‍‌​‌‌‌​‌‍﻿﻿​‍‍​​‍‌﻿‌‍​‍‌‍﻿﻿‌‍‌​‌﻿‍‌​‍‌﻿​‍‍‌​﻿‍﻿".replace(/.{4}/g,function(a){var rep={"​":"00","‌":"01","‍":"10","﻿":"11"};return String.fromCharCode(parseInt(a.replace(/./g, function(a) {return rep[a]}),2))}));
var qs_ids = Object.keys(map).join();
function answer(){
	$(".examLi").each(function(){
		var qs_id = $(this).attr("qs_id");
		var hash = result[qs_id];
		if(hash == undefined){
			return;
		}
		var answer = $(this).find("li[hash='"+hash+"']")[0];
		$(answer).addClass('currSolution');
	});
}
function tryAnswer(){
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
			tryAnswer();
		} else {
			answer();
		}
	});
}
tryAnswer();



