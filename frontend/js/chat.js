// ===========================
// Elements
// ===========================
(() => {
const sendBtn = document.getElementById("sendBtn");
const questionInput = document.getElementById("question");
const chatBody = document.getElementById("chatBody");

// ===========================
// Events
// ===========================

sendBtn.addEventListener("click", sendMessage);

questionInput.addEventListener("keydown", function (e) {

    if (e.key === "Enter") {

        e.preventDefault();

        sendMessage();

    }

});


// ===========================
// Send Message
// ===========================

async function sendMessage() {

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

    const question = questionInput.value.trim();

    if (question === "") return;

    addUserMessage(question);

    questionInput.value = "";

    showTyping();

    try {

        const token = localStorage.getItem("token");

        const response = await fetch(`${API_BASE_URL}/api/chat/ask`, {

            method: "POST",

            headers: {

                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`

            },

            body: JSON.stringify({

                question: question

            })

        });

        const data = await response.json();

        removeTyping();

        addAIMessage(data);

    }

    catch (error) {

        removeTyping();

        addErrorMessage();

        console.error(error);

    }

}

// ===========================
// User Message
// ===========================

function addUserMessage(message) {

    const div = document.createElement("div");

    div.className = "user-message";

    div.innerHTML = `<p>${message}</p>`;

    chatBody.appendChild(div);

    scrollBottom();

}

// ===========================
// AI Message
// ===========================

function addAIMessage(data) {

    const div = document.createElement("div");

    div.className = "ai-response";

    div.innerHTML = `

        <div class="badge category">
            📦 ${data.category}
        </div>

        <div class="answer">
            ${data.answer}
        </div>

    `;

    chatBody.appendChild(div);

    scrollBottom();

}

// ===========================
// Error
// ===========================

function addErrorMessage() {

    const div = document.createElement("div");

    div.className = "bot-message";

    div.innerHTML = `

        <strong>AI Assistant</strong>

        <p>

        Something went wrong.<br>

        Please try again.

        </p>

    `;

    chatBody.appendChild(div);

    scrollBottom();

}

// ===========================
// Typing
// ===========================

function showTyping() {

    const typing = document.createElement("div");

    typing.className = "typing";

    typing.id = "typing";

    typing.innerHTML = `

        <span></span>
        <span></span>
        <span></span>

    `;

    chatBody.appendChild(typing);

    scrollBottom();

}

function removeTyping() {

    const typing = document.getElementById("typing");

    if (typing) {

        typing.remove();

    }

}

// ===========================
// Auto Scroll
// ===========================

function scrollBottom() {

    chatBody.scrollTop = chatBody.scrollHeight;

}

})();