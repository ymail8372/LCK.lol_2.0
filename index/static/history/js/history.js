const year_links = document.querySelectorAll("#history_menu .menu_year a");

var queryString = window.location.search;
var searchParam = new URLSearchParams(queryString);

var selected_year = searchParam.get('year');
var selected_league = searchParam.get('league');

window.onload = function() {
	year_links.forEach(function(year_link) {
		if (year_link.href.includes(selected_year) && year_link.href.includes(selected_league)) {
			year_link.style.color = "#373a3c";
		}
	});
};
