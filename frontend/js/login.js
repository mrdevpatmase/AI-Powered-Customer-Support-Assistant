const form = document.getElementById("loginForm");

form.addEventListener("submit", loginUser);

async function loginUser(e){

    e.preventDefault();

    const email=document.getElementById("email").value.trim();

    const password=document.getElementById("password").value.trim();

    try{

        const response=await fetch(`${API_BASE_URL}/api/auth/login`,{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                email,
                password
            })

        });

        const data=await response.json();

        if(!response.ok){

            alert(data.message);

            return;

        }

        // Save JWT

        localStorage.setItem("token",data.token);

        // Save User

        localStorage.setItem("user",JSON.stringify(data.user));

        // Redirect

        if (data.user.role === "admin") {

    window.location.href = "admin.html";

} else {

    localStorage.setItem("openChat", "true");
window.location.href = "index.html";

}

    }

    catch(err){

        console.error(err);

        alert("Unable to connect to server.");

    }

}