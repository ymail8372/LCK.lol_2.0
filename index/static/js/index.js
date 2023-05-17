let date_object = new Date();
let date = date_object.getMonth()+1 + "/" + date_object.getDate();

let block = document.querySelector(".block");

const prev_button = document.querySelector(".controler_left");
const next_button = document.querySelector(".controler_right");

let weekdays = ['월', '화', '수', '목', '금', '토', '일'];

function show_slide() {
	console.log(schedules);
};

window.addEventListener('load', function() {
	show_slide();
});


prev_button.addEventListener("click", function() {
	date.setDate(date.getDate() - 1);
	show_date = date.getMonth()+1 + "/" + date.getDate();
	show_slide();
});

next_button.addEventListener("click", function() {
	date.setDate(date.getDate() + 1);
	show_date = date.getMonth()+1 + "/" + date.getDate();
	show_slide();
});
	
