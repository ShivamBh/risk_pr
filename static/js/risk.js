$(document).ready(function() {

	var ratingSpan = $(".rating-span");
	//console.log(ratingSpan);
	var shield =$("#shield-core")
	var secLevel = $(".sec-level-color");	

	// amber = e58b58, yellow = fde364, red = c63542, green = 6FC076
	
	console.log(secLevel);
	if (secLevel.text() == "Green") {
		shield.css("fill", "#6FC076");
	}
	else if (secLevel.text() == "Red") {
		shield.css("fill", "#c63542");
	}
	else if (secLevel.text() == "Yellow") {
		shield.css("fill", "#fde364");
	}

	else {
		shield.css("fill", "#e58b58");
	}

	


	ratingSpan.each(function() {
		// console.log($(this).siblings().attr('src'));
		// console.log($(this).siblings().attr('src'));
		if($(this).text() === "Ex") {
			$(this).siblings().attr("src", "/static/img/red_thermo.svg");
		}
		if($(this).text() === "H") {
			$(this).siblings().attr("src", "/static/img/orange_thermo.svg");
		}
		if($(this).text() === "M") {
			$(this).siblings().attr("src", "/static/img/yellow_thermo.svg");
		}
		if($(this).text() === "L") {
			$(this).siblings().attr("src", "/static/img/green_thermo.svg");
		}

	});



});