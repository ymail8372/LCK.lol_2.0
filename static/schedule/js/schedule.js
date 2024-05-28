var today = new Date();
const months = document.querySelectorAll('#schedule_block #month_selection .activated');
const month_blocks = document.querySelectorAll("#schedule_block #schedules .schedule");
const team_selections = document.querySelectorAll("#schedule_block .team_selection");
const team_buttons = document.querySelectorAll("#schedule_block .team_selection .team button");
const schedules = document.querySelectorAll("#schedule_block #schedules .schedule");

// initalize
var temp_month = String(today.getMonth() + 1);
if (temp_month.length == 1) {
	temp_month = "0" + temp_month;
}
var selected_month = "month_" + temp_month;
month_blocks.forEach(function(month_block) {
	if (month_block.classList.contains(selected_month)) {
		month_block.style.display = "flex";
	}
});
team_selections.forEach(function(team_selection) {
	console.log(selected_month);
	if (team_selection.classList.contains(selected_month)) {
		team_selection.style.display = "flex";
	}
});
months.forEach(function(month) {
	if (month.id == selected_month) {
		month.classList.add("selected_month");
	}
});
window.onload = function() {
	alternating_patternize();
};

function show_month_teams() {
	team_selections.forEach(function(team_selection) {
		if (team_selection.classList.contains(selected_month)) {
			team_selection.style.display = "flex";
		}
		else {
			team_selection.style.display = "none";
		}
	});
};

function alternating_patternize() {
	let gray = 1;
	schedules.forEach(function(schedule) {
		schedule.style.background = "#F7F7F7";
		if (schedule.style.display == "flex") {
			if (gray) {
				schedule.style.background = "#E7E7E7";
				gray = 0;
			}
			else {
				gray = 1;
			}
		}
	});
};

var selected_teams = [];
function show_schedule() {
	schedules.forEach(function(schedule) {
		schedule.style.display = "none";
		if (schedule.classList.contains(selected_month)) {
			if (selected_teams.length == 0) {
				schedule.style.display = "flex";
				alternating_patternize();
			}
			else {
				for(let i = 0; i < selected_teams.length; i ++) {
					if (schedule.classList.contains(selected_teams[i]) || schedule.classList.contains(selected_teams[i])) {
						schedule.style.display = "flex";
						alternating_patternize();
						break;
					}
				}
			}
		}
	});
};

months.forEach(function(month) {
	month.addEventListener("click", function() {
		selected_month = month.id;
		show_schedule();
		show_month_teams();
		
		months.forEach(function(month) {
			month.classList.remove("selected_month");
		});
		month.classList.add("selected_month");
	})
});

const all_buttons = document.querySelectorAll("#schedule_block .team_selection .team button .all");
team_buttons.forEach(function(button) {
	button.addEventListener("click", function() {
		let button_img = button.querySelector("img");
		let selected_team = button_img.className;
		if (selected_team == "all") {
			selected_teams = [];
			
			// only make all_button's opacity == 1
			team_buttons.forEach(function(button) {
				let button_img = button.querySelector("img");
				if (button_img.style.opacity == 1) {
					button_img.style.opacity = 0.4;
				}
			});
			all_buttons.forEach(function(all_button) {
				all_button.style.opacity = 1;
			});
		}
		else {
			if (button_img.style.opacity == 1) {
				button_img.style.opacity = 0.4;
				selected_teams = selected_teams.filter(team => team !== selected_team);
			}
			else {
				button_img.style.opacity = 1;
				if (selected_teams.indexOf(selected_team) == -1) {
					selected_teams.push(selected_team);
				}
			}
			
			if (selected_teams.length == 0) {
				all_buttons.forEach(function(all_button) {
					all_button.style.opacity = 1;
				});
			}
			else {
				all_buttons.forEach(function(all_button) {
					all_button.style.opacity = 0.4;
				});
			}
		}
		console.log(selected_teams)
		show_schedule();
	});
});
