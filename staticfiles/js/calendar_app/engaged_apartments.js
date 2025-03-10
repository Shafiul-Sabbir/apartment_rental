document.addEventListener("DOMContentLoaded", function () {
    function updateTenantNames() {
        let nameCells = document.querySelectorAll(".name-cell");
        nameCells.forEach(cell => {
            let fullName = cell.getAttribute("data-fullname"); // Get full name
            if (!fullName) return; // Avoid errors if data-fullname is missing

            if (window.innerWidth <= 768) {
                if (fullName.length > 10) {
                    cell.textContent = fullName.slice(0, 10) + "..."; // Show first 10 characters + "..."
                } else {
                    cell.textContent = fullName; // Show full name if ≤ 10 characters
                }
            } else {
                cell.textContent = fullName; // Show full name for larger screens
            }
        });
    }

    updateTenantNames(); // Run initially
    window.addEventListener("resize", updateTenantNames); // Update on resize
});