var crmajax = function(method, url, data, successCallback, errorCallback) {
	$.ajax({
		type: method,
		url: url,
		data: data,
		dataType: "json",   //返回格式为json
		traditional: true,
		cache:false, 
		success: function(ret) {
			successCallback && successCallback(ret);
		},
		error: function(err) {
			errorCallback && errorCallback(err);
		}
	});
}
function opensearch(obj) {
	var bar = document.getElementById("searchbar");
	if (bar.style.display == "none") {
		bar.style.display = "block";
		obj.value = "关闭查询";
	} else {
		bar.style.display = "none";
		obj.value = "查询>>";
	}
}
function selectOption(menuname, values) {
	$("#"+menuname).val(values);
//	var menu = document.getElementById(menuname);
//	if (menu) {
//		for (var i = 0; i <= menu.options.length; i++) {
//			if (values) {
//				if (menu.options[i].value == values) {
//					menu.options[i].selected = true;
//					break;
//				}
//			}
//		}
//	}
}
//选择国家
function selectcountry(id) {
	if(id == "1") {
		document.getElementById("othercountrys").style.display = "none"
		document.getElementById("mycountry").style.display = ""
	} else {
		document.getElementById("othercountrys").style.display = ""
		document.getElementById("mycountry").style.display = "none"
	}
}
function selectCheckBox(boxname, thevalue) {
	if (thevalue){
	var boxes = document.getElementsByName(boxname);
	for (var i = 0; i < boxes.length; i++) {
		if (thevalue) {
			if (thevalue.toString() == boxes[i].value.toString()) {
				boxes[i].checked = true;
			}
		}
	}
	}
}

function getcity(city){
	var selectprovince = $("#p").val();
	if ($("#c").length>0){
		if (selectprovince) {
			$.ajax({
				type: "GET",
				url: "getsite.html?sitecode=" + selectprovince,
				dataType: "json",
				success: function(data) {
					$("#c").empty();
					html = "<option value=''>--请选择城市--</option>";
					$("#c").append(html);
					for (var i = 0; i < data.length; i++) {
						html = "<option value='" + data[i]['code'] + "'>" + data[i]['label'] + "</option>";
						$("#c").append(html);
					}
					if (city){
						selectOption("c",city.substr(0,16));
						getcityarea(city);
					}
				},
				error: function(data) {
					alert("错误!青重试.");
				}
			});
		} else {
			$("#c").empty();
			html = "<option value=''>--请选择城市--</option>";
			$("#c").append(html);
		}
	}
}

function getcityarea(areac){
	var selectprovince = $("#c").val();
	if ($("#d").length>0){
		if (selectprovince) {
			$.ajax({
				type: "GET",
				url: "getsite.html?sitecode=" + selectprovince,
				dataType: "json",
				success: function(data) {
					$("#d").empty();
					html = "<option value=''>--请选择市区--</option>";
					$("#d").append(html);
					for (var i = 0; i < data.length; i++) {
						html = "<option value='" + data[i]['code'] + "'>" + data[i]['label'] + "</option>";
						$("#d").append(html);
					}
					if (areac){
						selectOption("d",areac);
					}
				},
				error: function(data) {
					alert("错误!青重试.");
				}
			});
		} else {
			$("#d").empty();
			html = "<option value=''>--请选择市区--</option>";
			$("#d").append(html);
		}
	}
}