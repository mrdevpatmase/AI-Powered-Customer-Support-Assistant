const token = localStorage.getItem("token");

const user = JSON.parse(localStorage.getItem("user"));

if (
    !token ||
    !user ||
    user.role !== "admin"
) {
    window.location.href = "admin-login.html";
}
function logout(){

    localStorage.removeItem("token");

    localStorage.removeItem("user");

    window.location.href="admin-login.html";

}
const API_URL = "/api";


if (!token) {
    window.location.href = "login.html";
}

let allHistory = [];

// ===============================
// Load Dashboard
// ===============================

document.addEventListener("DOMContentLoaded", () => {

    loadDashboard();

    loadHistory();

    document
        .getElementById("searchInput")
        .addEventListener("input", filterHistory);

    document
        .getElementById("categoryFilter")
        .addEventListener("change", filterHistory);

    document
        .getElementById("logoutBtn")
        .addEventListener("click", logout);

});

// ===============================
// Dashboard Cards
// ===============================

async function loadDashboard() {

    try {

        const response = await fetch(`${API_URL}/admin/dashboard`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        const data = await response.json();

        document.getElementById("totalUsers").textContent = data.total_users;
        document.getElementById("totalQueries").textContent = data.total_queries;
        document.getElementById("shipping").textContent = data.shipping;
        document.getElementById("refund").textContent = data.refund;
        document.getElementById("payment").textContent = data.payment;
        document.getElementById("orders").textContent = data.orders;

    } catch (error) {

        console.error(error);

        alert("Unable to load dashboard.");

    }

}

// ===============================
// Chat History
// ===============================

async function loadHistory() {

    try {

        const response = await fetch(`${API_URL}/admin/history`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        allHistory = await response.json();

        renderTable(allHistory);

    } catch (error) {

        console.error(error);

        alert("Unable to load chat history.");

    }

}

// ===============================
// Render Table
// ===============================

function renderTable(data) {

    const table = document.getElementById("historyTable");

    table.innerHTML = "";

    if (data.length === 0) {

        table.innerHTML = `
            <tr>
                <td colspan="7" style="text-align:center;padding:30px;">
                    No chat history found.
                </td>
            </tr>
        `;

        return;
    }

    data.forEach(chat => {

        let badgeClass = "";

        switch (chat.priority.toLowerCase()) {

            case "high":
                badgeClass = "high";
                break;

            case "medium":
                badgeClass = "medium";
                break;

            default:
                badgeClass = "low";
        }

        table.innerHTML += `

        <tr>

            <td>${chat.user}</td>

            <td>${chat.email}</td>

            <td>${chat.question}</td>

            <td>${chat.category}</td>

            <td>
                <span class="badge ${badgeClass}">
                    ${chat.priority}
                </span>
            </td>

            <td>${chat.confidence}%</td>

            <td>${chat.created_at}</td>

        </tr>

        `;

    });

}

// ===============================
// Search + Filter
// ===============================

function filterHistory() {

    const keyword = document
        .getElementById("searchInput")
        .value
        .toLowerCase();

    const category = document
        .getElementById("categoryFilter")
        .value;

    const filtered = allHistory.filter(chat => {

        const matchSearch =

            chat.user.toLowerCase().includes(keyword) ||

            chat.email.toLowerCase().includes(keyword) ||

            chat.question.toLowerCase().includes(keyword);

        const matchCategory =

            category === "" ||

            chat.category === category ||

            chat.priority === category;

        return matchSearch && matchCategory;

    });

    renderTable(filtered);

}
