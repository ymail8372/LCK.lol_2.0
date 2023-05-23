var date = new Date();
const block = document.querySelector(".block");
var schedules = 0;
var type = 0;

const weekday = ['월', '화', '수', '목', '금', '토', '일'];

const prev_button = document.querySelector(".controler_left");
const next_button = document.querySelector(".controler_right");

window.addEventListener('load', async function() {
	const response = await fetch('http://localhost:8000/get_schedules');
	schedules = await response.json();
	type = schedules[schedules.length-1]['etc'];
	
	show_slide();
});

function show_slide() {
	let show_no_team = 1;
	
	block.querySelectorAll(".teams").forEach(query => {
		query.style.display = "none";
	});
	
	for (let i = 0; i < schedules.length; i ++) {
		if (schedules[i]['year'] == date.getFullYear() && schedules[i]['month'] == date.getMonth()+1 && schedules[i]['day'] == date.getDate()) {
			type = schedules[i]['etc'];
			block.querySelector(".date_" + date.getFullYear() + (date.getMonth()+1) + date.getDate()).style.display = "block";
			show_no_team = 0;
			break;
		}
	}
	
	// If there are no schedules
	if (show_no_team) {
		block.querySelector(".no_team").style.display = "block";
		type = " - ";
	}
	
	let date_str = (date.getMonth()+1) + "월 " + date.getDate() + "일 (" + weekday[date.getDay()] + ")";
	block.querySelector(".title .date").innerHTML = date_str;
	block.querySelector(".title .type").innerHTML = type;
};

prev_button.addEventListener("click", function() {
	date.setDate(date.getDate() - 1);
	show_slide();
});

next_button.addEventListener("click", function() {
	date.setDate(date.getDate() + 1);
	show_slide();
});
