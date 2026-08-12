document.addEventListener("DOMContentLoaded", function () {

    console.log("TourEase Loaded Successfully");

    const profileBtn = document.getElementById("profileBtn");
    const profileCard = document.getElementById("profileCard");

    if (profileBtn && profileCard) {

        profileBtn.onclick = function(e) {
            e.preventDefault();

            if (profileCard.style.display === "block") {
                profileCard.style.display = "none";
            } else {
                profileCard.style.display = "block";
            }
        };

    }

});