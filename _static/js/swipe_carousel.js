const swipeCarousel = document.querySelector(".swipe-carousel-container");
const scCards = document.querySelectorAll(".sc-card");
const scInfos = document.querySelectorAll(".swipe-carousel-info");
let scCurrentIndex = 0;
let isAnimating = false;
let intervalId;

const updateCarousel = (newIndex) => {
    if (isAnimating) return;

    isAnimating = true;

    scCurrentIndex = (newIndex + scCards.length) % scCards.length;
    scCards.forEach((card, i) => {
        const offset = (i - scCurrentIndex + scCards.length) % scCards.length;

        card.classList.remove("center", "left", "right", "hidden");

        if (offset === 0) {
            card.classList.add("center");
        } else if (offset === 1) {
            card.classList.add("right");
        } else if (offset === scCards.length - 1) {
            card.classList.add("left");
        } else {
            card.classList.add("hidden");
        }

        if (offset != 0) scInfos[i].classList.add("hidden");
        else scInfos[i].classList.remove("hidden");
    });

    isAnimating = false;
};

const startCarousel = () => {
    intervalId = setInterval(() => {
        updateCarousel(scCurrentIndex + 1);
    }, 5000);
};

const stopCarousel = () => clearInterval(intervalId);
swipeCarousel.addEventListener("mouseenter", stopCarousel);
swipeCarousel.addEventListener("mouseleave", startCarousel);
updateCarousel(scCurrentIndex);
startCarousel();
