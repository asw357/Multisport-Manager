document.addEventListener("DOMContentLoaded", function() {
    checkLoginStatus();

    document.getElementById("tutorial-link")?.addEventListener("click", function() {
        document.getElementById("tutorial-modal").style.display = "block";
    });

    document.querySelector(".close-btn")?.addEventListener("click", function() {
        document.getElementById("tutorial-modal").style.display = "none";
    });
});

function checkLoginStatus() {
    let user = JSON.parse(localStorage.getItem("loggedInUser"));
    if (user) {
        document.querySelectorAll(".hidden").forEach(el => el.style.display = "inline");
        document.getElementById("logout-link").style.display = "inline";
    }
}

function logout() {
    localStorage.removeItem("loggedInUser");
    window.location.href = "index.html";
}
