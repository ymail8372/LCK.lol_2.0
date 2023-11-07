const leagues = document.querySelectorAll("#champion_menu #league_selection .league");
const patch_selections = document.querySelectorAll("#champion_menu .patch_selection");
const patches = document.querySelectorAll("#champion_menu .patch_selection .patch");

var selected_league = "LCK_summer";
var selected_patch = "13.14";

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
			if (patch.textContent == selected_patch) {
				patch.classList.add("selected_patch");
			}
		});
	}
});

leagues.forEach(function(league) {
	league.addEventListener("click", function() {
		selected_league = league.classList[1];
		leagues.forEach(function(league) {
			if (league.classList.contains(selected_league)) {
				league.querySelector("img").style.opacity = 1;
			}
			else {
				league.querySelector("img").style.opacity = 0.2;
			}
		});
		patch_selections.forEach(function(patch_selection) {
			if (patch_selection.classList.contains(selected_league)) {
				patch_selection.style.display = "flex";
				patch_selection.querySelector(".patch").dispatchEvent(new MouseEvent("click"));
			}
			else {
				patch_selection.style.display = "none";
			}
		});
	});
});

patches.forEach(function(patch) {
	patch.addEventListener("click", function() {
		patches.forEach(function(patch) {
			patch.classList.remove("selected_patch");
		});
		patch.classList.add("selected_patch");
	});
});
