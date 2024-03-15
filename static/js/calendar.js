const daysTag = document.querySelector(".days"),
    currentDate = document.querySelector(".current-date"),
    prevIcon = document.getElementById("prev-month"),
    nextIcon = document.getElementById("next-month"),
    dayViewBtn = document.getElementById("day-view-btn"),
    weekViewBtn = document.getElementById("week-view-btn"),
    monthViewBtn = document.getElementById("month-view-btn");
let date = new Date(),
    currYear = date.getFullYear(),
    currMonth = date.getMonth(),
    viewMode = 'month'; // Default view mode
const months = ["January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December"];
const toggleView = (view) => {
    viewMode = view;
    renderCalendar();
    if (view === 'week') {
        weekViewBtn.classList.add("active");
        monthViewBtn.classList.remove("active");
        dayViewBtn.classList.remove("active");
    } else if (view === 'day') {
        dayViewBtn.classList.add("active");
        weekViewBtn.classList.remove("active");
        monthViewBtn.classList.remove("active");
    } else if (view === 'month') {
        monthViewBtn.classList.add("active");
        weekViewBtn.classList.remove("active");
        dayViewBtn.classList.remove("active");
    }
};
const renderCalendar = () => {
    let firstDayOfMonth = new Date(currYear, currMonth, 1).getDay(),
        lastDateOfMonth = new Date(currYear, currMonth + 1, 0).getDate(),
        lastDayOfMonth = new Date(currYear, currMonth, lastDateOfMonth).getDay(),
        lastDateOfLastMonth = new Date(currYear, currMonth, 0).getDate(),
        daysInWeek = 7;
    firstDayOfMonth = firstDayOfMonth === 0 ? 6 : firstDayOfMonth - 1;
    let liTag = "",
        daysToRender = viewMode === 'month' ? lastDateOfMonth : daysInWeek;
    if (viewMode === 'week') {
        let currentDate = new Date(),
            currentDayOfWeek = currentDate.getDay(),
            currentDay = currentDate.getDate(),
            daysFromStartOfWeek = currentDayOfWeek === 0 ? 6 : currentDayOfWeek - 1,
            startOfWeek = currentDay - daysFromStartOfWeek;
        for (let i = startOfWeek; i < startOfWeek + daysInWeek; i++) {
            liTag += i >= 1 && i <= lastDateOfMonth ? `<li>${i}</li>` : `<li class="inactive"></li>`;
        }
    } else if (viewMode === 'month') {
        for (let i = firstDayOfMonth; i > 0; i--) {
            liTag += `<li class="inactive">${lastDateOfLastMonth - i + 1}</li>`;
        }
        for (let i = 1; i <= lastDateOfMonth; i++) {
            let isToday = i === date.getDate() && currMonth === new Date().getMonth()
                && currYear === new Date().getFullYear() ? "active" : "";
            liTag += `<li class="${isToday}">${i}</li>`;
        }
        for (let i = lastDayOfMonth; i < 6; i++) {
            liTag += `<li class="inactive">${i - lastDayOfMonth + 1}</li>`;
        }
    } else if (viewMode === 'day') {
        const today = new Date();
        const dayOfWeek = today.getDay();
        const currentDate = today.getDate();
        for (let i = 0; i < dayOfWeek - 1; i++) {
            liTag += `<li class="inactive"></li>`;
        }
        liTag += `<li class="active">${currentDate}</li>`;
    }
    currentDate.innerText = `${months[currMonth]} ${currYear}`;
    daysTag.innerHTML = liTag;
};
const changeMonth = (direction) => {
    currMonth = direction === 'prev' ? currMonth - 1 : currMonth + 1;
    if (currMonth < 0 || currMonth > 11) {
        date = new Date(currYear, currMonth);
        currYear = date.getFullYear();
        currMonth = date.getMonth();
    } else {
        date = new Date(currYear, currMonth);
    }
    renderCalendar();
};
weekViewBtn.addEventListener("click", () => toggleView('week'));
monthViewBtn.addEventListener("click", () => toggleView('month'));
dayViewBtn.addEventListener("click", () => toggleView('day'));
prevIcon.addEventListener("click", () => changeMonth('prev'));
nextIcon.addEventListener("click", () => changeMonth('next'));
renderCalendar();
