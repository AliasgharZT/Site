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

// Check if the legal modal has been shown before
if (!sessionStorage.getItem("legalModalShown")) {
    // Create overlay and modal
    const overlay = document.createElement("div");
    overlay.id = "overlay";
    overlay.style.position = "fixed";
    overlay.style.top = "0";
    overlay.style.left = "0";
    overlay.style.width = "100%";
    overlay.style.height = "100%";
    overlay.style.backgroundColor = "rgba(0, 0, 0, 0.7)";
    overlay.style.zIndex = "1000";
    overlay.style.display = "flex";
    overlay.style.justifyContent = "center";
    overlay.style.alignItems = "center";

    const legalModal = document.createElement("div");
    legalModal.id = "legal-modal";
    const englishText = `
        <div class="modal-content">
            <h3>Terms and Conditions of Use</h3>
            <p>
                <strong>By using this site, you agree to:</strong><br><br>
                <div class="rules">
                    <div>1. This site will not misuse your personal information.</div>
                    <div>2. You must refrain from any misuse of the site's name or content.</div>
                    <div>3. You are responsible for any content you enter on the site.</div>
                    <div>4. This site may use cookies to improve user experience.</div>
                    <div>5. Legal actions will be taken for rule violations.</div>
                </div>
                <br>
                <b>By clicking the "Accept" button, you accept all terms and conditions above.</b>
            </p>
            <button id="change-language-btn">Change to فارسی</button><br>
            <button id="accept-btn">Accept</button>
            <button id="decline-btn">Decline</button>
        </div>`;

    const persianText = `
        <div class="modal-content">
            <h3>قوانین و شرایط استفاده از سایت</h3>
            <p>
                <strong>با استفاده از این سایت، شما موافقت می‌کنید که:</strong><br><br>
                <div class="rules">
                    <div>۱. این سایت به هیچ وجه از اطلاعات شخصی شما سوءاستفاده نخواهد کرد.</div>
                    <div>۲. شما موظف هستید از هرگونه سوءاستفاده از نام یا محتوای سایت خودداری کنید.</div>
                    <div>۳. شما مسئول هرگونه محتوایی هستید که در سایت وارد می‌کنید.</div>
                    <div>۴. این سایت ممکن است از کوکی‌ها برای بهبود تجربه کاربری استفاده کند.</div>
                    <div>۵. در صورت تخلف، اقدامات قانونی لازم انجام خواهد شد.</div>
                </div>
                <br>
                <b>با کلیک روی دکمه "قبول"، شما تمامی شرایط فوق را می‌پذیرید.</b>
            </p>
            <button id="change-language-btn">Change to English</button><br>
            <button id="accept-btn">قبول</button>
            <button id="decline-btn">رد</button>
        </div>`;

    legalModal.innerHTML = englishText;
    overlay.appendChild(legalModal);
    document.body.appendChild(overlay);

    const style = document.createElement("style");
    style.innerHTML = `
        .modal-content {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            max-width: 500px;
            width: 90%;
            text-align: center;
            color: #333;
            overflow: auto;
            max-height: 80vh;
        }
        .modal-content h3 {
            margin-bottom: 15px;
            font-size: 1.5rem;
            color: #000;
        }
        .modal-content p {
            text-align: left;
            line-height: 1.6;
            font-size: 0.9rem;
        }
        .modal-content p[dir="rtl"] {
            text-align: right;
        }
        .modal-content .rules {
            text-align: left;
        }
        .modal-content .rules[dir="rtl"] {
            text-align: right;
        }
        .modal-content button {
            margin: 10px;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1rem;
        }
        .modal-content button#accept-btn {
            background-color: green;
            color: white;
        }
        .modal-content button#decline-btn {
            background-color: red;
            color: white;
        }
        .modal-content button#change-language-btn {
            background-color: blue;
            color: white;
        }
        @media (max-width: 768px) {
            .modal-content {
                width: 80%;
            }
        }
    `;
    document.head.appendChild(style);

    let isEnglish = true;

    const updateContent = () => {
        legalModal.innerHTML = isEnglish ? englishText : persianText;
        if (!isEnglish) {
            document.querySelector(".modal-content").setAttribute("dir", "rtl");
        } else {
            document.querySelector(".modal-content").removeAttribute("dir");
        }

        document.getElementById("change-language-btn").addEventListener("click", toggleLanguage);
        document.getElementById("accept-btn").addEventListener("click", () => {
            overlay.style.display = "none";
            sessionStorage.setItem("legalModalShown", "true");
        });

        document.getElementById("decline-btn").addEventListener("click", () => {
            alert(isEnglish ? "You must accept the terms to access the site." : "شما باید شرایط را بپذیرید تا به سایت دسترسی داشته باشید.");
        });
    };

    const toggleLanguage = () => {
        isEnglish = !isEnglish;
        updateContent();
    };

    updateContent();
}



});
