$(document).ready(function() {

	var ratingSpan = $(".rating-span");
	//console.log(ratingSpan);

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