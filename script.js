document.addEventListener("DOMContentLoaded", function() {
    checkLoginStatus();

    document.getElementById("tutorial-link").addEventListener("click", function() {
        document.getElementById("tutorial-modal").style.display = "block";
    });

    document.querySelector(".close-btn").addEventListener("click", function() {
        document.getElementById("tutorial-modal").style.display = "none";
    });
});

function checkLoginStatus() {
    let user = localStorage.getItem("user");
    if (user) {
        document.querySelectorAll(".hidden").forEach(el => el.style.display = "inline");
    }
}

function logout() {
    localStorage.removeItem("user");
    window.location.href = "index.html";
}
