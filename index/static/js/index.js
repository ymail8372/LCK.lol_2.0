var date = new Date();
date.setHours(0, 0, 0, 0);
var schedules = 0;

const weekday = ['일', '월', '화', '수', '목', '금', '토'];

const prev_button = document.querySelector(".schedule_controler.schedule_controler_left");
const next_button =	document.querySelector(".schedule_controler.schedule_controler_right");

// window onload
window.onload = () => {
	show_schedule();
};

// axios
const schedule_block_URL = "/schedule_block";
const schedule_block = document.querySelector("#schedule_block");

const show_schedule = () => {
	var req_URL = schedule_block_URL + "?year=" + date.getFullYear() + "&month=" + (date.getMonth() + 1) + "&date=" + date.getDate()
	axios.get(req_URL)
	.then(response => {
		schedule_block.innerHTML = response.data;
	})
	.catch(error => {
		console.error("There is error on Axios", error);
	});
	};

prev_button.addEventListener("click", function() {
	date.setDate(date.getDate() - 1);
	show_schedule();
});

next_button.addEventListener("click", function() {
	date.setDate(date.getDate() + 1);
	show_schedule();
});
