const form=document.getElementById("signupForm");

form.addEventListener("submit",signup);

async function signup(e){

e.preventDefault();

const name=document.getElementById("name").value.trim();

const email=document.getElementById("email").value.trim();

const password=document.getElementById("password").value.trim();

try{

const response=await fetch(`${API_BASE_URL}/api/auth/signup`,{

method:"POST",

headers:{

"Content-Type":"application/json"

},

body:JSON.stringify({

name,
email,
password

})

});

const data=await response.json();

if(!response.ok){

alert(data.message);

return;

}

alert("Account created successfully");

window.location.href="login.html";

}

catch(err){

console.log(err);

alert("Unable to connect to server.");

}

}