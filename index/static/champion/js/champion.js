const leagues = document.querySelectorAll("#champion_menu #league_selection .league");
const patch_selections = document.querySelectorAll("#champion_menu .patch_selection");
const patches = document.querySelectorAll("#champion_menu .patch_selection .patch");
var champion_menus = document.querySelectorAll("#champions .champion_menu div");
champion_menus = Array.from(champion_menus);
champion_menus.pop()
champion_menus.shift()
const champions_table = document.querySelector("#champions .champion_table");
var champions = champions_table.querySelectorAll(".champion");

var queryString = window.location.search;
var searchParam = new URLSearchParams(queryString);

var selected_league = searchParam.get('league');
var selected_patch = searchParam.get('patch');

// initalize
leagues.forEach(function(league) {
	if (league.classList.contains(selected_league)) {
		league.querySelector("img").style.opacity = 1;
	}
});
patch_selections.forEach(function(patch_selection) {
	if (patch_selection.classList.contains(selected_league)) {
		patch_selection.style.display = "flex";
		patch_selection.querySelectorAll(".patch").forEach(function(patch) {
			if (patch.textContent == selected_patch || patch.classList.contains(selected_patch)) {
				patch.classList.add("selected_patch");
			}
		});
	}
});

// patternize
function alternating_patternize() {
	let gray = 1;
	champions = champions_table.querySelectorAll(".champion");
	champions.forEach(function(champion) {
		champion.style.background = "#F7F7F7";
		if (gray) {
			champion.style.background = "#E7E7E7";
			gray = 0;
		}
		else {
			gray = 1;
		}
	});
};

// ajax
var xhr = new XMLHttpRequest();
var base_URL = "/champion_table";

champion_menus.forEach(function(champion_menu) {
	champion_menu.addEventListener("click", function() {
		// set CSS
		if (champion_menu.classList.length == 1 || champion_menu.classList[1] == 'ascending') {
			req_URL = base_URL + "?league=" + selected_league + "&patch=" + selected_patch + "&sort=" + champion_menu.classList[0] + "_descending";
			champion_menus.forEach(function(champion_menu) {
				champion_menu.classList.remove('descending');
				champion_menu.classList.remove('ascending');
			});
			champion_menu.classList.add('descending');
		}
		else {
			req_URL = base_URL + "?league=" + selected_league + "&patch=" + selected_patch + "&sort=" + champion_menu.classList[0] + "_ascending";
			champion_menus.forEach(function(champion_menu) {
				champion_menu.classList.remove('descending');
				champion_menu.classList.remove('ascending');
			});
			champion_menu.classList.add('ascending');
		}
		
		// set AJAX
		xhr.open("GET", req_URL);
		xhr.onreadystatechange = function() {
			if (xhr.readyState === 4 && xhr.status === 200) {
				champions_table.innerHTML = xhr.responseText;
				alternating_patternize();
			}
		};
		xhr.send();
		
	});
});

// onload
window.onload = function() {
	req_URL = base_URL + "?league=" + selected_league + "&patch=" + selected_patch;
	
	// set AJAX
	xhr.open("GET", req_URL);
	xhr.onreadystatechange = function() {
		if (xhr.readyState === 4 && xhr.status === 200) {
			champions_table.innerHTML = xhr.responseText;
			alternating_patternize();
		}
	};
	xhr.send();
};
