

function switchLanguage(lang) {
    window.location.href = `/switch_language/${lang}`;
}

document.addEventListener("DOMContentLoaded", () => {
    const navButtons = document.querySelectorAll(".nav-btn");
    const sections = document.querySelectorAll("section");

    // Set default section to "home"
    document.getElementById("home").classList.add("active");
    document.querySelector('.nav-btn[data-section="home"]').classList.add("active");

    navButtons.forEach(button => {
        button.addEventListener("click", () => {
            // Hide all sections and remove active class from all buttons
            sections.forEach(section => section.classList.remove("active"));
            navButtons.forEach(btn => btn.classList.remove("active"));

            // Show the selected section and mark the button as active
            const targetSection = button.getAttribute("data-section");
            document.getElementById(targetSection).classList.add("active");
            button.classList.add("active");
        });
    });
///////////////
});
