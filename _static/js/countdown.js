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

function initializeClock(id, startTime, endTime, enable) {
    let clockStop = document.getElementById(id + "-stop");
    let clock = document.getElementById(id);

    let enableBlock = enable.map((e) => document.getElementById(e));
    let clockTitle = document.getElementById(id + "-title");
    let daysSpan = clock.querySelector(".days");
    let hoursSpan = clock.querySelector(".hours");
    let minutesSpan = clock.querySelector(".minutes");
    let secondsSpan = clock.querySelector(".seconds");

    // Check if this countdown should be shown
    let shouldShow = false;
    if (startTime == 0) {
        // This is the "registration will start" countdown - only show if end time is in future
        shouldShow = getTimeRemaining(endTime).total > 0;
        if (shouldShow) {
            clockTitle.style.display = "block";
            enableBlock.forEach((e) => (e.style.display = "none"));
        }
    } else {
        // This is the main countdown - show if registration has started
        shouldShow = getTimeRemaining(startTime).total <= 0 && getTimeRemaining(endTime).total > 0;
    }

    // Initialize immediately on page load
    updateClock();
    let timeinterval = setInterval(updateClock, 1000);

    function updateClock() {
        let t = getTimeRemaining(endTime);

        daysSpan.innerHTML = t.days;
        hoursSpan.innerHTML = ("0" + t.hours).slice(-2);
        minutesSpan.innerHTML = ("0" + t.minutes).slice(-2);
        secondsSpan.innerHTML = ("0" + t.seconds).slice(-2);

        // Check if countdown should be visible and mark as initialized
        if (startTime != 0 && getTimeRemaining(startTime).total <= 0) {
            shouldShow = true;
            clockTitle.style.display = "block";
            enableBlock.forEach((e) => (e.style.display = "none"));
        }

        // Only add initialized class if this countdown should be shown
        if (shouldShow && t.total > 0) {
            clock.classList.add("initialized");
        }

        if (t.total <= 0) {
            clearInterval(timeinterval);
            clock.classList.remove("initialized");
            clockTitle.style.display = "none";
            if (clockStop) {
                clockStop.style.display = "block";
            }
            enableBlock.forEach((e) => (e.style.display = "block"));
        }
    }
}

const hideAfterDate = (datetime, id) => {
    if (Date.parse(datetime) < Date.parse(new Date())) {
        document.getElementById(id).style.display = "none";
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
