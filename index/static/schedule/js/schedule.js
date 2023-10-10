var today = new Date();
const months = document.querySelectorAll('#schedule_block #months .month');
const months_blocks = document.querySelectorAll("#schedule_block #schedules .schedule")

function show_month_schedule(selected_month) {
	console.log(selected_month);
	months_blocks.forEach(function(month_block) {
		console.log(month_block.id);
		if (month_block.classList[1] == selected_month) {
			month_block.style.display = "flex";
		}
		else {
			month_block.style.display = "none";
		}
	});
};

months.forEach(function(month) {
	month.addEventListener("click", function() {
		show_month_schedule(month.id);
	})
});
