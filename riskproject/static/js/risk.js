$(document).ready(function() {

// Rating and color
var ratings_text = $(".ratings-hidden");
var ratings_color = $(".rating-color");


ratings_color.each(function() {

	if ($(this).find("h6").text() == "L") {
		$(this).css("background-color", "#62D277");
	}
	else if ($(this).find("h6").text() == "M") {
		$(this).css("background-color", "#E5D643");
	}
	else if ($(this).find("h6").text() == "H") {
		$(this).css("background-color", "#E68C58");
	}
	else {
		$(this).css("background-color", "#C73542");
	}
	
	console.log($(this).find("h6").text());
});

 });