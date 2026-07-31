// ================= Dashboard Doughnut Chart =================

const ctx = document.getElementById("myChart");

if (ctx && window.income !== undefined && window.expense !== undefined) {

    new Chart(ctx, {
        type: "doughnut",

        data: {
            labels: ["Income", "Expense"],

            datasets: [{
                data: [window.income, window.expense],
                backgroundColor: ["#22C55E", "#EF4444"]
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            plugins: {
                legend: {
                    position: "bottom"
                }
            }
        }
    });

}



// ================= Smooth Scroll =================

document.querySelectorAll(".menu-btn").forEach(btn => {

    btn.addEventListener("click", function (e) {

        const href = this.getAttribute("href");

        if (href && href.startsWith("#")) {

            e.preventDefault();

            const target = document.querySelector(href);

            if (target) {

                target.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });

            }
        }

    });

});



// ================= Active Menu =================

const sections = document.querySelectorAll(
    "#dashboard,#transactions,#reports"
);

const buttons = document.querySelectorAll(".menu-btn");

function setActiveMenu() {

    let current = "dashboard";

    sections.forEach(section => {

        const rect = section.getBoundingClientRect();

        if (rect.top <= 150 && rect.bottom >= 150) {

            current = section.id;

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
window.addEventListener("load", setActiveMenu);



// ================= Sidebar Toggle =================

const menuToggle = document.getElementById("menu-toggle");
const sidebar = document.getElementById("sidebar");
const mainContent = document.getElementById("main-content");

if (menuToggle && sidebar && mainContent) {

    menuToggle.addEventListener("click", () => {

        if (window.innerWidth <= 768) {

            sidebar.classList.toggle("active");

        } else {

            sidebar.classList.toggle("collapsed");
            mainContent.classList.toggle("expanded");

        }

    });

}

// ================= PROFILE DROPDOWN =================

const profileBtn = document.getElementById("profileBtn");
const profileMenu = document.getElementById("profileMenu");

if(profileBtn && profileMenu){

    profileBtn.addEventListener("click",function(e){

        e.stopPropagation();

        profileMenu.classList.toggle("show");

    });

    document.addEventListener("click",function(){

        profileMenu.classList.remove("show");

    });

}