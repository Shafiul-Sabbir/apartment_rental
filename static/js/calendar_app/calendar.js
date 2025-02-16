// handling the calendar tooltip for each cell
document.addEventListener("DOMContentLoaded", function () {
    var tooltipElements = document.querySelectorAll('[data-toggle="tooltip"]');
    tooltipElements.forEach(function (element) {
        new bootstrap.Tooltip(element);
    });
});
