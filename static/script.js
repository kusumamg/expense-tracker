// ================= Doughnut Chart =================
const ctx = document.getElementById('myChart');

if (ctx && window.income !== undefined && window.expense !== undefined) {
  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Income', 'Expense'],
      datasets: [{
        data: [window.income, window.expense],
        backgroundColor: ['#28a745', '#dc3545']
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom'
        }
      }
    }
  });
}


// ================= Smooth Scroll =================
document.querySelectorAll('.menu-btn').forEach(btn => {
  btn.addEventListener('click', function(e) {
    e.preventDefault();

    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});


// ================= Active Highlight =================
const sections = document.querySelectorAll("#dashboard, #transactions, #reports");
const buttons = document.querySelectorAll(".menu-btn");

function setActiveMenu() {
  let current = "dashboard"; // default

  sections.forEach(sec => {
    const rect = sec.getBoundingClientRect();

    if (rect.top <= 150 && rect.bottom >= 150) {
      current = sec.id;
    }
  });

  buttons.forEach(btn => {
    btn.classList.remove("active");
    if (btn.getAttribute("href") === "#" + current) {
      btn.classList.add("active");
    }
  });
}

window.addEventListener("scroll", setActiveMenu);
window.addEventListener("load", setActiveMenu); // ✅ fix on load


// ================= Sidebar Toggle =================
const menuToggle = document.getElementById("menu-toggle");
const sidebar = document.getElementById("sidebar");
const mainContent = document.getElementById("main-content");

menuToggle.addEventListener("click", () => {

    if(window.innerWidth <= 768){

        sidebar.classList.toggle("active");

    }else{

        sidebar.classList.toggle("collapsed");
        mainContent.classList.toggle("expanded");

    }

});


// ================= Search & Notification =================

const searchBtn = document.getElementById("searchBtn");
const searchBox = document.getElementById("searchBox");

const notificationBtn = document.getElementById("notificationBtn");
const notificationPanel = document.getElementById("notificationPanel");

if (searchBtn && searchBox) {
    searchBtn.addEventListener("click", function (e) {
        e.stopPropagation();

        searchBox.classList.toggle("show");

        if (notificationPanel) {
            notificationPanel.classList.remove("show");
        }
    });
}

if (notificationBtn && notificationPanel) {
    notificationBtn.addEventListener("click", function (e) {
        e.stopPropagation();

        notificationPanel.classList.toggle("show");

        if (searchBox) {
            searchBox.classList.remove("show");
        }
    });
}

document.addEventListener("click", function () {

    if (searchBox) {
        searchBox.classList.remove("show");
    }

    if (notificationPanel) {
        notificationPanel.classList.remove("show");
    }

});