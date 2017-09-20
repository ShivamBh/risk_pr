$(document).ready(function() {

	var mquery = Modernizr.mq('only screen and (min-width: 320px) and (max-width: 659px) ')

	if mquery {
		var open = false
		$(".nav-mob").click(function(e) {
			$(".site-header").css("display","block");
			open = true;
			e.stopPropagation();
			
			console.log("click");
		});

		$('html').click(function() {
			$(".site-header").css("display","none");
		})	
	}
	

	// $(".container").on('click', function(e) {
	// 	if (open) {
	// 		$(".site-header").css("display","none");
	// 		open = false
	// 	}

		
	// });

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