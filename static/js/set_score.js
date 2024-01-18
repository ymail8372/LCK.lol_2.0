function set_score(team1_score, team2_score) {
	str = 0
	if (team1_score == 0 && team2_score == 0) {
		str = "vs";
	}
	else {
		str = team1_score + " : " + team2_score;
	}
	
	document.write(str);
}