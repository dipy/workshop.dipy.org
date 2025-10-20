/**
 * Schedule Carousel - Mobile navigation for workshop schedule
 */

(function() {
    let currentSlide = 0;
    let totalSlides = 0;
    let scheduleGrid = null;
    let prevButton = null;
    let nextButton = null;
    let dots = null;
    let startX = 0;
    let currentX = 0;
    let isDragging = false;

    function initCarousel() {
        scheduleGrid = document.querySelector('.schedule-grid');
        prevButton = document.querySelector('.schedule-nav-prev');
        nextButton = document.querySelector('.schedule-nav-next');
        dots = document.querySelectorAll('.schedule-dot');

        if (!scheduleGrid || !prevButton || !nextButton) {
            return;
        }

        totalSlides = document.querySelectorAll('.schedule-day-column').length;

        prevButton.addEventListener('click', prevSlide);
        nextButton.addEventListener('click', nextSlide);

        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => goToSlide(index));
        });

        scheduleGrid.addEventListener('touchstart', handleTouchStart, { passive: true });
        scheduleGrid.addEventListener('touchmove', handleTouchMove, { passive: true });
        scheduleGrid.addEventListener('touchend', handleTouchEnd);

        scheduleGrid.addEventListener('mousedown', handleMouseDown);
        scheduleGrid.addEventListener('mousemove', handleMouseMove);
        scheduleGrid.addEventListener('mouseup', handleMouseUp);
        scheduleGrid.addEventListener('mouseleave', handleMouseUp);

        updateCarousel();
    }

    function goToSlide(index) {
        if (index < 0 || index >= totalSlides) {
            return;
        }
        currentSlide = index;
        updateCarousel();
    }

    function nextSlide() {
        if (currentSlide < totalSlides - 1) {
            currentSlide++;
            updateCarousel();
        }
    }

    function prevSlide() {
        if (currentSlide > 0) {
            currentSlide--;
            updateCarousel();
        }
    }

    function updateCarousel() {
        const offset = -currentSlide * 100;
        scheduleGrid.style.transform = `translateX(${offset}%)`;

        prevButton.disabled = currentSlide === 0;
        nextButton.disabled = currentSlide === totalSlides - 1;

        dots.forEach((dot, index) => {
            if (index === currentSlide) {
                dot.classList.add('active');
            } else {
                dot.classList.remove('active');
            }
        });

        // Update current day text
        const dayText = document.querySelector('.schedule-current-day-text');
        if (dayText) {
            dayText.textContent = `Day ${currentSlide + 1}`;
        }
    }

    function handleTouchStart(e) {
        startX = e.touches[0].clientX;
        isDragging = true;
    }

    function handleTouchMove(e) {
        if (!isDragging) return;
        currentX = e.touches[0].clientX;
    }

    function handleTouchEnd() {
        if (!isDragging) return;
        isDragging = false;

        const diff = startX - currentX;
        const threshold = 50;

        if (Math.abs(diff) > threshold) {
            if (diff > 0) {
                nextSlide();
            } else {
                prevSlide();
            }
        }
    }

    function handleMouseDown(e) {
        startX = e.clientX;
        isDragging = true;
        scheduleGrid.style.cursor = 'grabbing';
    }

    function handleMouseMove(e) {
        if (!isDragging) return;
        currentX = e.clientX;
    }

    function handleMouseUp() {
        if (!isDragging) return;
        isDragging = false;
        scheduleGrid.style.cursor = 'grab';

        const diff = startX - currentX;
        const threshold = 50;

        if (Math.abs(diff) > threshold) {
            if (diff > 0) {
                nextSlide();
            } else {
                prevSlide();
            }
        }
    }

    function handleKeyDown(e) {
        if (window.innerWidth > 768) return;

        if (e.key === 'ArrowLeft') {
            prevSlide();
        } else if (e.key === 'ArrowRight') {
            nextSlide();
        }
    }

    document.addEventListener('keydown', handleKeyDown);

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCarousel);
    } else {
        initCarousel();
    }

    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            if (window.innerWidth <= 768) {
                updateCarousel();
            } else {
                if (scheduleGrid) {
                    scheduleGrid.style.transform = '';
                }
            }
        }, 250);
    });
})();
