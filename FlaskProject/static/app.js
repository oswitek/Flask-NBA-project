document.addEventListener('DOMContentLoaded', function () {
	const gameCards = document.querySelectorAll('.game-card');

	gameCards.forEach((card) => {
		card.addEventListener('click', function (event) {
			const content = this.querySelector('.collapsible-content');
			if (content) {
				content.classList.toggle('active');
			}
		});
	});
});
