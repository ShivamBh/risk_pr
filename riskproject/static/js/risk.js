function main() {

	//tabs
	
	
	
	

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

	var sec_level = $(".sec-level-rating-text h3");
	var sec_color = $("sec-level-rating-color");

		if (sec_level.text() === "Green") {
			$("sec-level-rating-color").css("background-color", "C73542");
		}

		$( function() {
			$( "#datepicker_from" ).datepicker({dateFormat: "yy-mm-dd"});
	    	$( "#datepicker_to" ).datepicker({dateFormat: "yy-mm-dd"});
	  } );

	//console.log($("sec-level-rating-color"));
	 }


window.onload = main;