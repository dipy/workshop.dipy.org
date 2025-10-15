// Hero section carousel functionality

// Setup hero background carousel
function setupHomeCarousel(containerSelector, itemSelector) {
  const container = document.querySelector(containerSelector);
  const items = document.querySelectorAll(itemSelector);
  const indicators = document.querySelectorAll('.hero-carousel-indicator');

  if (!container || items.length === 0) return;

  // If there's only one item, just make it active and skip carousel logic
  if (items.length === 1) {
    items[0].classList.add('active');
    return;
  }

  let currentIndex = 0;

  function showSlide(index) {
    // Remove active class from all slides
    items.forEach(item => item.classList.remove('active'));
    indicators.forEach(indicator => indicator.classList.remove('active'));

    // Add active class to current slide
    if (items[index]) {
      items[index].classList.add('active');
    }
    if (indicators[index]) {
      indicators[index].classList.add('active');
    }

    currentIndex = index;
  }

  function nextSlide() {
    const nextIndex = (currentIndex + 1) % items.length;
    showSlide(nextIndex);
  }

  // Auto advance every 5 seconds
  setInterval(nextSlide, 5000);

  // Add click handlers to indicators
  indicators.forEach((indicator, index) => {
    indicator.addEventListener('click', () => showSlide(index));
  });

  // Show first slide
  showSlide(0);
}

// Make function globally available
window.setupHomeCarousel = setupHomeCarousel;
