var date = new Date();
date.setHours(0, 0, 0, 0);
const block = document.querySelector("#schedule_block");
var schedules = 0;

const weekday = ['일', '월', '화', '수', '목', '금', '토'];

const prev_button = document.querySelector(".schedule_controler.schedule_controler_left");
const next_button =	document.querySelector(".schedule_controler.schedule_controler_right");

window.addEventListener('load', async function() {
	show_slide();
});

function show_slide() {
	let date_title = (date.getMonth()+1) + "월 " + date.getDate() + "일 (" + weekday[date.getDay()] + ")";
	//let date_match = String(date.getFullYear()) + String(date.getMonth()+1) + String(date.getDate());
	let no_team = 1;
	
	block.querySelectorAll(".schedule_match").forEach(match => {
		if (match.classList[1].split("_")[2] == "team") {
			return;
		}
		match_date = new Date(match.classList[1].split("_")[2].slice(0, 4), String(parseInt(match.classList[1].split("_")[2].slice(4, 6))-1), match.classList[1].split("_")[2].slice(6, 8));
		if (match_date.getFullYear() == date.getFullYear() && match_date.getMonth() == date.getMonth() && match_date.getDate() == date.getDate()) {
			match.style.display = "flex";
			no_team = 0;
		}
	});
	
	// If there are no schedules
	if (no_team) {
		block.querySelector(".schedule_no_team").style.display = "flex";
	}
	
	block.querySelector("#schedule_title #schedule_date").innerHTML = date_title;
}

function hide_slide() {
	block.querySelectorAll(".schedule_match").forEach(match => {
		match.style.display = "none";
	});
}

prev_button.addEventListener("click", function() {
	hide_slide()
	date.setDate(date.getDate() - 1);
	show_slide();
});

next_button.addEventListener("click", function() {
	hide_slide()
	date.setDate(date.getDate() + 1);
	show_slide();
});
