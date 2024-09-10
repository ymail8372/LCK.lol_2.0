const leagues = document.querySelectorAll("#champion_menu #league_selection .league");
const patch_selections = document.querySelectorAll("#champion_menu .patch_selection");
const patches = document.querySelectorAll("#champion_menu .patch_selection .patch");

var queryString = window.location.search;
var searchParam = new URLSearchParams(queryString);

var selected_league = searchParam.get('league');
var selected_patch = searchParam.get('patch');

// initalize
leagues.forEach(function(league) {
	if (league.classList.contains(selected_league.replace(" ", "_"))) {
		league.querySelector("img").style.opacity = 1;
	}
});
patch_selections.forEach(function(patch_selection) {
	if (patch_selection.classList.contains(selected_league.replace(" ", "_"))) {
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

// campion_menus
var champion_menus = document.querySelectorAll("#champions .champion_menu div");
champion_menus = Array.from(champion_menus);
champion_menus.pop()
champion_menus.shift()
const champion_table_URL = "/champion_table";

champion_menus.forEach(function(champion_menu) {
	champion_menu.addEventListener("click", function() {
		if (champion_menu.classList.length == 1 || champion_menu.classList[1] == 'ascending') {
			req_URL = champion_table_URL + "?year=" + "2024" + "&league=" + selected_league + "&patch=" + selected_patch + "&sort=" + champion_menu.classList[0] + "_descending";
			champion_menus.forEach(function(champion_menu) {
				champion_menu.classList.remove('descending');
				champion_menu.classList.remove('ascending');
			});
			champion_menu.classList.add('descending');
		}
		else {
			req_URL = champion_table_URL + "?year=" + "2024" + "&league=" + selected_league + "&patch=" + selected_patch + "&sort=" + champion_menu.classList[0] + "_ascending";
			champion_menus.forEach(function(champion_menu) {
				champion_menu.classList.remove('descending');
				champion_menu.classList.remove('ascending');
			});
			champion_menu.classList.add('ascending');
		}
		
		show_champions();
	});
});

// axios
const champions_table = document.querySelector("#champions .champion_table");

const show_champions = () => {
	axios.get(req_URL)
	.then(response => {
		champions_table.innerHTML = response.data;
		alternating_patternize();
	})
	.catch(error => {
		console.error("There is error on Axios", error);
	});
};

// onload
window.onload = function() {
	req_URL = champion_table_URL + "?year=" + "2024" + "&league=" + selected_league + "&patch=" + selected_patch;
	
	show_champions();
};
