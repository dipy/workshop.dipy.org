// Initialize Splide carousels for participants section
document.addEventListener("DOMContentLoaded", function () {
  // Participants carousel
  const participantsCarousel = document.querySelector('.participants-carousel.splide');
  if (participantsCarousel && typeof Splide !== 'undefined') {
    new Splide('.participants-carousel.splide', {
      type: 'loop',
      perPage: 5,
      perMove: 1,
      gap: '2rem',
      autoplay: true,
      interval: 2000,
      speed: 1000,
      pauseOnHover: true,
      pauseOnFocus: true,
      arrows: false,
      pagination: false,
      drag: 'free',
      focus: 'center',
      breakpoints: {
        1280: {
          perPage: 4,
        },
        1024: {
          perPage: 3,
        },
        768: {
          perPage: 2,
        },
        640: {
          perPage: 1,
        },
      },
    }).mount();
  }

  // Highlights carousel
  const highlightsCarousel = document.querySelector('#highlights-splide');
  if (highlightsCarousel && typeof Splide !== 'undefined') {
    new Splide('#highlights-splide', {
      type: 'loop',
      perPage: 1,
      perMove: 1,
      gap: '2rem',
      autoplay: true,
      interval: 3000,
      speed: 800,
      pauseOnHover: true,
      pauseOnFocus: true,
      arrows: false,
      pagination: true,
    }).mount();
  }
});
