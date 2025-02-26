function updateTenantNames() {
    let nameCells = document.querySelectorAll(".name-cell");
    nameCells.forEach(cell => {
        let fullName = cell.getAttribute("data-fullname");
        if (window.innerWidth <= 481) {
            cell.textContent = fullName.slice(0, 10); // Show only 10 characters
        } else {
            cell.textContent = fullName; // Show full name
        }
    });
}

// Run on page load and resize
window.addEventListener("load", updateTenantNames);
window.addEventListener("resize", updateTenantNames);