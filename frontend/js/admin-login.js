const API_URL = "http://127.0.0.1:5000/api";

document
    .getElementById("adminLoginForm")
    .addEventListener("submit", loginAdmin);

async function loginAdmin(e){

    e.preventDefault();

    const email = document.getElementById("email").value;

    const password = document.getElementById("password").value;

    try{

        const response = await fetch(`${API_URL}/auth/admin-login`,{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                email,
                password
            })

        });

        const data = await response.json();

        if(!response.ok){

            alert(data.message);

            return;

        }

        if(data.user.role !== "admin"){

            alert("Access Denied! Only administrators can login here.");

            return;

        }

        localStorage.setItem("token",data.token);

        localStorage.setItem("user",JSON.stringify(data.user));

        window.location.href="admin.html";

    }

    catch(error){

        console.error(error);

        alert("Server Error");

    }

}