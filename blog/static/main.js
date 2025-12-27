document.addEventListener("DOMContentLoaded", () => {
    const track = document.querySelector(".featured-track");
    const cards = document.querySelectorAll(".featured-card");

    if (!track || cards.length === 0) return;

    let index = 0;
    const cardWidth = cards[0].offsetWidth + 20;

    setInterval(() => {
        index++;
        if (index >= cards.length) {
            index = 0;
        }
        track.style.transform = `translateX(-${index * cardWidth}px)`;
    }, 4000);
});
