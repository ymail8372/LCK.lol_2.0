let date = new Date();
let show_date = date.getMonth()+1 + "/" + date.getDate();

const prev_button = document.querySelector(".controler_left");
const next_button = document.querySelector(".controler_right");

let schedule_block = document.querySelectorAll("#schedule .schedule_block");

function show_slide() {
	let check = 0;
	
	for (let i = 0; i < schedule_block.length; i ++) {
		if (schedule_block[i].classList.contains(show_date)) {
			schedule_block[i].style.display = "block";
			check = 1;
		}
		else {
			schedule_block[i].style.display = "none";
		}
	}
	
	if (check == 0) {
		schedule_block[schedule_block.length-1].style.display = "block";
		document.querySelector('.date').innerHTML = date.getMonth()+1 + "월 " + date.getDay()  + "일";
	}
};

window.addEventListener('load', function() {
	show_slide();
});
  

function move_slide(num) {
	if (num == 0) {
		date.setDate(date.getDate() - 1);
		show_date = date.getMonth()+1 + "/" + date.getDate();
	}
	else {
		date.setDate(date.getDate() + 1);
		show_date = date.getMonth()+1 + "/" + date.getDate();
	}
	
	return 0;
}

prev_button.addEventListener("click", function() {
	move_slide(0);
	show_slide();
});

next_button.addEventListener("click", function() {
	move_slide(1);
	show_slide();
});
	
