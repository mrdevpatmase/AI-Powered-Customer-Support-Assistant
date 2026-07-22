// ===========================
// DOM Elements
// ===========================

const chatButton = document.getElementById("chatButton");
const chatPopup = document.getElementById("chatPopup");
const closeChat = document.getElementById("closeChat");
const startChatBtn = document.querySelector(".hero-btn");

const loginBtn = document.querySelector(".customer-login");
const logoutBtn = document.getElementById("logoutBtn");

// ===========================
// Navbar Buttons
// ===========================

const token = localStorage.getItem("token");

const user = JSON.parse(localStorage.getItem("user"));

const welcomeUser = document.getElementById("welcomeUser");

if (token && user) {

    welcomeUser.innerHTML = `Hi, <strong>${user.name}</strong> 👋`;

} else {

    welcomeUser.innerHTML = "";

}

if (token) {
    loginBtn.style.display = "none";
    logoutBtn.style.display = "inline-flex";
} else {
    loginBtn.style.display = "inline-flex";
    logoutBtn.style.display = "none";
}

// ===========================
// Open Chat
// ===========================

function openChat(e) {

    if (e) e.preventDefault();

    const token = localStorage.getItem("token");
    const user = JSON.parse(localStorage.getItem("user"));

    if (!token || !user) {
        window.location.href = "login.html";
        return;
    }

    if (user.role === "admin") {
        window.location.href = "admin.html";
        return;
    }

    chatPopup.classList.add("active");
}

// ===========================
// Logout
// ===========================

logoutBtn.addEventListener("click", logout);

function logout() {

    localStorage.removeItem("token");
    localStorage.removeItem("user");

    window.location.href = "index.html";
}

// ===========================
// Close Chat
// ===========================

function closeChatWindow() {

    chatPopup.classList.remove("active");

}

// ===========================
// Events
// ===========================

// Floating Chat Button
chatButton.addEventListener("click", openChat);

// Hero Button
startChatBtn.addEventListener("click", openChat);

// Close Button
closeChat.addEventListener("click", closeChatWindow);

// ===========================
// Close Chat When Clicking Outside
// ===========================

document.addEventListener("click", function (event) {

    const clickedInsidePopup = chatPopup.contains(event.target);
    const clickedChatButton = chatButton.contains(event.target);
    const clickedHeroButton = startChatBtn.contains(event.target);

    if (
        !clickedInsidePopup &&
        !clickedChatButton &&
        !clickedHeroButton &&
        chatPopup.classList.contains("active")
    ) {
        closeChatWindow();
    }

});

// ===========================
// ESC Key Support
// ===========================

document.addEventListener("keydown", function (event) {

    if (event.key === "Escape") {

        closeChatWindow();

    }

});

if (localStorage.getItem("openChat") === "true") {

    localStorage.removeItem("openChat");
    chatPopup.classList.add("active");

}