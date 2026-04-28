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
function toggleSidebar() {
  document.getElementById("sidebar").classList.toggle("collapsed");
}