document.addEventListener("DOMContentLoaded", function () {
    // Wait a bit for the page to fully load
    setTimeout(() => {
        createCustomNavbar();
        setupScrollBehavior();
        addScrollSpy();
        addSmoothScrollHandlers();
    }, 100);

    const header = document.querySelector(".bd-header");
    let lastScrollTop = 0;
    const scrollThreshold = 100; // Show navbar after scrolling this many pixels

    // Function to handle scroll events
    function handleScroll() {
        const currentScroll =
            window.pageYOffset || document.documentElement.scrollTop;

        // Show navbar when scrolling down past threshold
        if (currentScroll > scrollThreshold) {
            header.classList.add("show");
        } else {
            header.classList.remove("show");
        }

        lastScrollTop = currentScroll;
    }

    // Add scroll event listener
    window.addEventListener("scroll", handleScroll);

    // Initial check for scroll position
    handleScroll();
});

function setupScrollBehavior() {
    const navbar = document.querySelector(".custom-navbar");
    if (!navbar) return;

    let lastScrollTop = 0;
    let ticking = false;

    function updateNavbarVisibility() {
        const scrollTop =
            window.pageYOffset || document.documentElement.scrollTop;

        // Show navbar when scrolling down past 150px
        if (scrollTop > 150) {
            navbar.classList.add("visible", "sticky");
        } else {
            navbar.classList.remove("visible", "sticky");
        }

        lastScrollTop = scrollTop;
        ticking = false;
    }

    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateNavbarVisibility);
            ticking = true;
        }
    }

    // Use passive event listener for better performance
    window.addEventListener("scroll", requestTick, { passive: true });
}

function createCustomNavbar() {
    // Find all H1 elements in the main content area
    const h1Elements = document.querySelectorAll(
        ".bd-main h1, .bd-content h1, main h1, .document h1"
    );

    console.log("Found H1 elements:", h1Elements.length); // Debug log

    if (h1Elements.length === 0) {
        console.log("No H1 elements found, trying alternative selectors...");
        // Try alternative selectors
        const altH1 = document.querySelectorAll("h1");
        console.log("Alternative H1 search found:", altH1.length);
        if (altH1.length > 0) {
            createNavbarFromElements(altH1);
        }
        return;
    }

    createNavbarFromElements(h1Elements);
}

function createNavbarFromElements(h1Elements) {
    // Find the navbar or create one
    let navbarCenter = document.querySelector(".navbar-center");

    if (!navbarCenter) {
        // Try to find alternative navbar locations
        const navbar = document.querySelector(".navbar, .bd-navbar, nav");
        if (navbar) {
            navbarCenter = document.createElement("div");
            navbarCenter.className = "navbar-center";
            navbar.appendChild(navbarCenter);
        } else {
            console.log("No navbar found, creating one...");
            createNavbarContainer();
            navbarCenter = document.querySelector(".navbar-center");
        }
    }

    if (!navbarCenter) {
        console.error("Could not create navbar container");
        return;
    }

    // Create navbar navigation list
    const navList = document.createElement("ul");
    navList.className = "navbar-nav";

    h1Elements.forEach((h1, index) => {
        // Skip the main title (usually the first H1)
        if (index === 0 && h1.textContent.includes("Welcome")) {
            return;
        }

        // Create ID for the section if it doesn't exist
        if (!h1.id) {
            // Generate ID from text content
            const text = h1.textContent.trim().toLowerCase();
            h1.id = text
                .replace(/[^a-z0-9]/g, "-")
                .replace(/-+/g, "-")
                .replace(/^-|-$/g, "");
        }

        // Create navigation item
        const navItem = document.createElement("li");
        navItem.className = "nav-item";

        const navLink = document.createElement("a");
        navLink.className = "nav-link";
        navLink.href = `#${h1.id}`;
        // Remove leading/trailing # and whitespace
        let cleanText = h1.textContent
            .trim()
            .replace(/^#+\s*|\s*#+$/g, "")
            .trim();
        navLink.textContent = cleanText;
        navLink.setAttribute("data-target", h1.id);

        navItem.appendChild(navLink);
        navList.appendChild(navItem);
    });

    // Clear existing content and add our custom nav
    navbarCenter.innerHTML = "";
    navbarCenter.appendChild(navList);

    console.log("Navbar created with", navList.children.length, "items");
}

function createNavbarContainer() {
    // Create a navbar if one doesn't exist
    const body = document.body;
    const navbar = document.createElement("nav");
    navbar.className = "navbar custom-navbar";
    navbar.innerHTML = `
        <div class="navbar-brand">Navigation</div>
        <div class="navbar-center"></div>
    `;

    // Insert at the top of the body
    body.insertBefore(navbar, body.firstChild);
}

function addSmoothScrollHandlers() {
    // Add click handlers to all navigation links
    const navLinks = document.querySelectorAll(".navbar-nav .nav-link");

    navLinks.forEach((link) => {
        link.addEventListener("click", function (e) {
            e.preventDefault();

            const targetId = this.getAttribute("data-target");
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                // Calculate offset for fixed navbar
                const navbarHeight =
                    document.querySelector(".custom-navbar").offsetHeight || 80;
                const offsetTop = targetElement.offsetTop - navbarHeight - 20;

                window.scrollTo({
                    top: offsetTop,
                    behavior: "smooth",
                });

                // Update active state
                updateActiveNavLink(this);
            }
        });
    });
}

function addScrollSpy() {
    // Add scroll spy to highlight current section
    const navLinks = document.querySelectorAll(".navbar-nav .nav-link");
    const sections = document.querySelectorAll("h1[id]");

    if (sections.length === 0) return;

    let ticking = false;

    function updateActiveSection() {
        const scrollPos = window.scrollY + 200; // Offset for navbar
        let current = "";

        sections.forEach((section) => {
            const sectionTop = section.offsetTop;
            const nextSection = section.nextElementSibling;
            const sectionHeight = nextSection
                ? nextSection.offsetTop - sectionTop
                : document.body.scrollHeight - sectionTop;

            if (
                scrollPos >= sectionTop &&
                scrollPos < sectionTop + sectionHeight
            ) {
                current = section.id;
            }
        });

        // Update active nav link
        navLinks.forEach((link) => {
            link.classList.remove("active");
            if (link.getAttribute("data-target") === current) {
                link.classList.add("active");
            }
        });

        ticking = false;
    }

    function requestScrollTick() {
        if (!ticking) {
            requestAnimationFrame(updateActiveSection);
            ticking = true;
        }
    }

    window.addEventListener("scroll", requestScrollTick, { passive: true });
}

function updateActiveNavLink(activeLink) {
    // Remove active class from all links
    const navLinks = document.querySelectorAll(".navbar-nav .nav-link");
    navLinks.forEach((link) => link.classList.remove("active"));

    // Add active class to clicked link
    activeLink.classList.add("active");
}

function addSmoothScrollHandlers() {
    // Add click handlers to all navigation links
    const navLinks = document.querySelectorAll(".navbar-nav .nav-link");

    navLinks.forEach((link) => {
        link.addEventListener("click", function (e) {
            e.preventDefault();

            const targetId = this.getAttribute("data-target");
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                // Calculate offset for fixed navbar
                const navbarHeight =
                    document.querySelector(".navbar").offsetHeight || 60;
                const offsetTop = targetElement.offsetTop - navbarHeight - 20;

                window.scrollTo({
                    top: offsetTop,
                    behavior: "smooth",
                });

                // Update active state
                updateActiveNavLink(this);
            }
        });
    });
}

function addScrollSpy() {
    // Add scroll spy to highlight current section
    const navLinks = document.querySelectorAll(".navbar-nav .nav-link");
    const sections = document.querySelectorAll("h1[id]");

    if (sections.length === 0) return;

    window.addEventListener("scroll", function () {
        let current = "";
        const scrollPos = window.scrollY + 100; // Offset for navbar

        sections.forEach((section) => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;

            if (
                scrollPos >= sectionTop &&
                scrollPos < sectionTop + sectionHeight
            ) {
                current = section.id;
            }
        });

        // Update active nav link
        navLinks.forEach((link) => {
            link.classList.remove("active");
            if (link.getAttribute("data-target") === current) {
                link.classList.add("active");
            }
        });
    });
}

function updateActiveNavLink(activeLink) {
    // Remove active class from all links
    const navLinks = document.querySelectorAll(".navbar-nav .nav-link");
    navLinks.forEach((link) => link.classList.remove("active"));

    // Add active class to clicked link
    activeLink.classList.add("active");
}

const fadeOut = (element, duration = 500) => {
    element.style.transition = `opacity ${duration}ms ease-in-out`;
    element.style.opacity = 0;

    setTimeout(() => {
        element.style.display = "none";
    }, duration);
};

const fadeIn = (element, duration = 500) => {
    element.style.display = "block";
    // Force reflow to ensure transition applies
    void element.offsetHeight;
    element.style.transition = `opacity ${duration}ms ease-in-out`;
    element.style.opacity = 1;
};

const setupHomeCarousel = (carousel_holder_class, carousel_item_class) => {
    var speed = 2000;
    var delay = 7000;

    const carousel_holders = document.querySelectorAll(carousel_holder_class);

    carousel_holders.forEach((holder) => {
        let itemSlides = holder.querySelectorAll(carousel_item_class);
        let currSlide = 0;

        itemSlides.forEach((slide, index) => {
            slide.style.display = index === currSlide ? "block" : "none";
        });
        itemSlides[currSlide].style.opacity = 1; // Ensure current slide is visible

        currSlide = (currSlide + 1) % itemSlides.length;

        setInterval(() => {
            itemSlides.forEach((slide) => {
                if (slide.style.display === "block") {
                    fadeOut(slide, speed);
                }
            });
            fadeIn(itemSlides[currSlide], speed);

            currSlide = (currSlide + 1) % itemSlides.length;
        }, delay);
    });
};
