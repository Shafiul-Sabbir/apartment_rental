// handling the calendar tooltip for each cell
document.addEventListener("DOMContentLoaded", function () {
    var tooltipElements = document.querySelectorAll('[data-toggle="tooltip"]');
    tooltipElements.forEach(function (element) {
        new bootstrap.Tooltip(element);
    });
});


function fetchEvents(year, month, day) {
    console.log("Fetching events for:", year, month, day);
    // Update modal title with selected date
    document.getElementById("modalDate").innerText = `${day}-${month}-${year}`;

    // Clear previous event list
    let eventListDiv = document.getElementById("eventList");
    eventListDiv.innerHTML = '<p class="text-center">Loading events...</p>';

    // Load CSS dynamically for modal
    let cssLink = document.getElementById("dayViewStyles");
    if (!cssLink) {
        cssLink = document.createElement("link");
        cssLink.id = "dayViewStyles";
        cssLink.rel = "stylesheet";
        cssLink.href = "/static/css/calendar_app/day_view.css"; // Adjust the path if necessary
        document.head.appendChild(cssLink);
    }

    // Fetch event data using AJAX
    fetch(`/calendar/get-events/${year}/${month}/${day}/`)
    .then(response => response.json())
    .then(data => {
        eventListDiv.innerHTML = ""; // Clear loading message
        
        if (data.events.length === 0) {
            eventListDiv.innerHTML = `
                <div class="alert alert-warning text-center" role="alert">
                    No events for this day.
                </div>
            `;
        } else {
            let eventCards = `<div class="row d-flex justify-content-center ">`;

            data.events.forEach(event => {
                let tenant_name = event.tenant_name ; // Default to "N/A" if remarks are missing
                let tenant_nameHTML = "";

                if (tenant_name.length > 10) {
                    tenant_nameHTML = `
                        <p class="card-text">Tenant: 
                            <span class="card-title" data-full-text="${tenant_name}">
                                ${tenant_name.substring(0, 10)}...
                            </span>
                        </p>
                    `;
                } else {
                    tenant_nameHTML = `<p class="card-text">Tenant: 
                    <span class="card-title" data-full-text="${tenant_name}">
                                ${tenant_name.substring(0, 10)}...
                            </span>
                        </p>`;
                }

                let remarksText = event.tenant_remarks || "N/A"; // Default to "N/A" if remarks are missing
                let remarksHTML = "";

                if (remarksText.length > 10) {
                    remarksHTML = `
                        <p class="card-text">Remarks: 
                            <span class="remarks-tooltipp" data-full-text="${remarksText}">
                                ${remarksText.substring(0, 10)}...
                            </span>
                        </p>
                    `;
                } else {
                    remarksHTML = `<p class="card-text">Remarks: ${remarksText}</p>`;
                }

                eventCards += `
                    <div class="col-md-4 mb-4 ">
                        <div class="card event-card shadow-sm">
                            <div class="card-body text-center">
                                ${tenant_nameHTML}
                                <p class="card-text">Apartment: ${event.apartment_number}</p>
                                <p class="card-text">Arrival Date: ${event.start_date}</p>
                                <p class="card-text">Departure Date: ${event.end_date}</p>
                                <p class="card-text">Status: ${event.tenant_status}</p>
                                ${remarksHTML}
                            </div>
                        </div>
                    </div>
                `;
            });

            eventCards += `</div>`;
            eventListDiv.innerHTML = eventCards;
        }

        // Enable tooltips
        $(function () {
            $('[data-full-text]').tooltip({
                placement: 'top',
                trigger: 'hover',
                title: function () {
                    return $(this).attr('data-full-text');
                }
            });
        });
    })
    .catch(error => {
        console.error("Error fetching events:", error);
        eventListDiv.innerHTML = '<p class="text-danger text-center">Failed to load events.</p>';
    });

    // Show the modal
    $('#eventModal').modal('show');

    $(document).ready(function () {
        $(".close").click(function () {
            $("#eventModal").modal("hide");
        });
    });
}

