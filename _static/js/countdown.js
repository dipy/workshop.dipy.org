function getTimeRemaining(endtime) {
    let t = Date.parse(endtime) - Date.parse(new Date());
    let seconds = Math.floor((t / 1000) % 60);
    let minutes = Math.floor((t / 1000 / 60) % 60);
    let hours = Math.floor((t / (1000 * 60 * 60)) % 24);
    let days = Math.floor(t / (1000 * 60 * 60 * 24));
    return {
        total: t,
        days: days,
        hours: hours,
        minutes: minutes,
        seconds: seconds,
    };
}

function initializeHeroCard(config) {
    const titleEl = document.getElementById("hero-card-title");
    const subtitleEl = document.getElementById("hero-card-subtitle");
    const countdownEl = document.getElementById("hero-card-countdown");
    const actionEl = document.getElementById("hero-card-action");

    if (!titleEl || !countdownEl) return;

    const daysSpan = countdownEl.querySelector(".days");
    const hoursSpan = countdownEl.querySelector(".hours");
    const minutesSpan = countdownEl.querySelector(".minutes");
    const secondsSpan = countdownEl.querySelector(".seconds");

    let currentPhase = null;

    function getPhase() {
        const now = Date.parse(new Date());
        if (Date.parse(config.regStart) > now) return "pre-registration";
        if (Date.parse(config.workshopStart) > now) return "registration-open";
        if (Date.parse(config.workshopEnd) > now) return "workshop-active";
        return "workshop-ended";
    }

    function getCountdownTarget(phase) {
        switch (phase) {
            case "pre-registration": return config.regStart;
            case "registration-open": return config.workshopStart;
            case "workshop-active": return config.workshopEnd;
            default: return null;
        }
    }

    function applyPhase(phase) {
        currentPhase = phase;

        switch (phase) {
            case "pre-registration":
                titleEl.innerHTML = "<b>Registration</b> will start in";
                subtitleEl.textContent = "Time left until registration opens:";
                subtitleEl.style.display = "";
                countdownEl.style.display = "";
                countdownEl.classList.add("initialized");
                actionEl.style.display = "none";
                break;

            case "registration-open":
                titleEl.innerHTML = "<b>Registration</b> has been started";
                subtitleEl.textContent = "Time left to register:";
                subtitleEl.style.display = "";
                countdownEl.style.display = "";
                countdownEl.classList.add("initialized");
                actionEl.innerHTML = config.registerButton;
                actionEl.style.display = "";
                break;

            case "workshop-active":
                titleEl.innerHTML = "<b>Workshop</b> has been started";
                subtitleEl.textContent = "Time left:";
                subtitleEl.style.display = "";
                countdownEl.style.display = "";
                countdownEl.classList.add("initialized");
                actionEl.style.display = "none";
                break;

            case "workshop-ended":
                titleEl.innerHTML = "<b>Workshop</b> has ended";
                subtitleEl.textContent = "See you next year!";
                subtitleEl.style.display = "";
                countdownEl.style.display = "none";
                countdownEl.classList.remove("initialized");
                actionEl.innerHTML =
                    '<a href="https://workshop.dipy.org" class="hero-register-button">' +
                    "Checkout Latest Workshop</a>";
                actionEl.style.display = "";
                break;
        }
    }

    function updateClock() {
        const phase = getPhase();

        if (phase !== currentPhase) {
            applyPhase(phase);
        }

        if (phase === "workshop-ended") {
            clearInterval(interval);
            return;
        }

        const target = getCountdownTarget(phase);
        const t = getTimeRemaining(target);

        daysSpan.innerHTML = t.days;
        hoursSpan.innerHTML = ("0" + t.hours).slice(-2);
        minutesSpan.innerHTML = ("0" + t.minutes).slice(-2);
        secondsSpan.innerHTML = ("0" + t.seconds).slice(-2);
    }

    updateClock();
    let interval = setInterval(updateClock, 1000);
}

// Legacy functions used by v1 home_template.html
function initializeClock(id, startTime, endTime, enable) {
    let clockStop = document.getElementById(id + "-stop");
    let clock = document.getElementById(id);

    if (!clock) return;

    let enableBlock = enable.map((e) => document.getElementById(e));
    let clockTitle = document.getElementById(id + "-title");
    let daysSpan = clock.querySelector(".days");
    let hoursSpan = clock.querySelector(".hours");
    let minutesSpan = clock.querySelector(".minutes");
    let secondsSpan = clock.querySelector(".seconds");

    let shouldShow = false;
    if (startTime == 0) {
        shouldShow = getTimeRemaining(endTime).total > 0;
        if (shouldShow) {
            clock.style.display = "";
            if (clockTitle) clockTitle.style.display = "block";
            enableBlock.forEach((e) => { if (e) e.style.display = "none"; });
        }
    } else {
        shouldShow = getTimeRemaining(startTime).total <= 0 && getTimeRemaining(endTime).total > 0;
        if (!shouldShow) {
            clock.style.display = "none";
        }
    }

    updateClock();
    let timeinterval = setInterval(updateClock, 1000);

    function updateClock() {
        let t = getTimeRemaining(endTime);

        daysSpan.innerHTML = t.days;
        hoursSpan.innerHTML = ("0" + t.hours).slice(-2);
        minutesSpan.innerHTML = ("0" + t.minutes).slice(-2);
        secondsSpan.innerHTML = ("0" + t.seconds).slice(-2);

        if (startTime != 0 && getTimeRemaining(startTime).total <= 0) {
            shouldShow = true;
            clock.style.display = "";
            if (clockTitle) clockTitle.style.display = "block";
            enableBlock.forEach((e) => { if (e) e.style.display = "none"; });
        }

        if (shouldShow && t.total > 0) {
            clock.classList.add("initialized");
        }

        if (t.total <= 0) {
            clearInterval(timeinterval);
            clock.classList.remove("initialized");
            if (clockTitle) clockTitle.style.display = "none";
            if (clockStop) clockStop.style.display = "block";
            enableBlock.forEach((e) => { if (e) e.style.display = "block"; });
        }
    }
}

const hideAfterDate = (datetime, id) => {
    if (Date.parse(datetime) < Date.parse(new Date())) {
        const el = document.getElementById(id);
        if (el) el.style.display = "none";
    }
};

const messageAfterDate = (datetime, id, message) => {
    if (Date.parse(datetime) < Date.parse(new Date())) {
        const element = document.getElementById(id);
        if (element) {
            element.innerHTML = message;
        }
    }
};
