let date = new Date();
let show_date = date.getMonth()+1 + "/" + date.getDate();

const prev_button = document.querySelector(".controler_left");
const next_button = document.querySelector(".controler_right");

let block = document.querySelectorAll("#schedule .block");

let weekdays = ['월', '화', '수', '목', '금', '토', '일'];

function show_slide() {
	let check = 0;
	
	for (let i = 0; i < block.length; i ++) {
		if (block[i].classList.contains(show_date)) {
			block[i].style.display = "block"; // 해당 block이 보이도록 설정
			block[i].querySelector('.weekday').innerHTML = weekdays[date.getDay()]; // 요일 설정
			
			check = 1;
		}
		else {
			block[i].style.display = "none";
		}
	}
	
	if (check == 0) {
		block[block.length-1].style.display = "block";
		document.querySelector('.date').innerHTML = date.getMonth()+1 + "월 " + date.getDate()  + "일";
		document.querySelector('.weekday_none').innerHTML = weekdays[date.getDay()];
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
	
