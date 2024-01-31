const player_ranking = document.querySelectorAll("#player_ranking_block table td:first-child");

window.onload = function() {
	player_ranking.forEach(function(ranking) {
		if (ranking.textContent == "1") {
			ranking.style.background = "#AADDFF";
		}
	});
};