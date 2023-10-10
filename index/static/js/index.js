var date = new Date();
const block = document.querySelector("#schedule_block");
var schedules = 0;
var type = 0;

const weekday = ['일', '월', '화', '수', '목', '금', '토'];

const prev_button = document.querySelector(".schedule_controler.schedule_controler_left");
const next_button =	document.querySelector(".schedule_controler.schedule_controler_right");

window.addEventListener('load', async function() {
	const schedule_response = await fetch('http://localhost:8000/get_schedules_Json');
	schedules = await schedule_response.json();
	type = schedules[schedules.length-1]['etc'];
	
	const ranking_response = await this.fetch('http://localhost:8000/get_champions_Json')
	rankings = await ranking_response.json();
	
	
	show_slide();
});

function show_slide() {
	let show_no_team = 1;
	
	block.querySelectorAll(".schedule_match").forEach(query => {
		query.style.display = "none";
	});
	
	for (let i = 0; i < schedules.length; i ++) {
		if (schedules[i]['year'] == date.getFullYear() && schedules[i]['month'] == date.getMonth()+1 && schedules[i]['day'] == date.getDate()) {
			type = schedules[i]['etc'];
			block.querySelectorAll(".schedule_date_" + date.getFullYear() + (date.getMonth()+1) + date.getDate()).forEach(query => {
				query.style.display = "flex";
			});
			show_no_team = 0;
		}
	}
	
	// If there are no schedules
	if (show_no_team) {
		block.querySelector(".schedule_no_team").style.display = "flex";
		type = " - ";
	}
	
	let date_str = (date.getMonth()+1) + "월 " + date.getDate() + "일 (" + weekday[date.getDay()] + ")";
	block.querySelector("#schedule_title #schedule_date").innerHTML = date_str;
	block.querySelector("#schedule_title #schedule_type").innerHTML = type;
};

prev_button.addEventListener("click", function() {
	date.setDate(date.getDate() - 1);
	show_slide();
});

next_button.addEventListener("click", function() {
	date.setDate(date.getDate() + 1);
	show_slide();
});
