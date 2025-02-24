from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib import messages
from .models import CalendarEvent
from tenants.models import Apartment, Tenant
from datetime import datetime, date, timedelta
import calendar
from django.http import JsonResponse

def calendar_view(request, year, month):
    """
    View to display the monthly calendar with events.
    If no specific year or month is provided, it defaults to the current month.
    """
    today = datetime.today()  # Get today's date
    today_date = today.day  # Extract current day
    today_month = today.month  # Extract current month
    today_year = today.year  # Extract current year
    year = year or today.year  # Use provided year or fallback to current year
    
    # Ensure month is within valid range (1-12)
    if month > 12 or month < 1:
        month = today.month
    
    # Get first day of the month and total number of days
    first_day_of_month = datetime(year, month, 1)
    _, total_days = calendar.monthrange(year, month)
    
    # Calculate previous and next month details
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    
    # Get last day of previous month
    _, prev_month_days = calendar.monthrange(prev_year, prev_month)
    
    month_calendar = []  # Stores the entire month's calendar structure
    week = []  # Stores a single week's data
    first_weekday = first_day_of_month.weekday()  # Find the starting weekday (0 = Monday, 6 = Sunday)
    
    # Fill in previous month's dates to align the first row
    for i in range(first_weekday):
        day = prev_month_days - first_weekday + i + 1
        week.append({"day": day, "month": prev_month, "year": prev_year, "extra": True })
    
    # Fill in the current month's dates
    for day in range(1, total_days + 1):
        week.append({"day": day, "month": month, "year": year, "extra": False})
        if len(week) == 7:  # If a full week is completed, push to month_calendar
            month_calendar.append(week)
            week = []
    
    # Fill in next month's dates to align the last row
    next_day = 1
    while len(week) < 7:
        week.append({"day": next_day, "month": next_month, "year": next_year, "extra": True})
        next_day += 1
    if week:
        month_calendar.append(week)
    
    # Fetch all events occurring within the selected months
    events = CalendarEvent.objects.filter(
        start_date__year__in=[prev_year, year, next_year],
        start_date__month__in=[prev_month, month, next_month]
    )
    
    # Assign events to their respective dates
    for week in month_calendar:
        for day_info in week:
            date_obj = date(day_info["year"], day_info["month"], day_info["day"])
            day_info["tenants"] = events.filter(start_date__lte=date_obj, end_date__gte=date_obj)
    
    return render(request, 'calendar_app/calendar.html', {
        'current_date': first_day_of_month,
        'calendar_data': month_calendar,
        'today': today,
        'today_date': today_date,
        'today_month': today_month,
        'today_year': today_year,
        'year': year,
        'month': month,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
    })

def calendar_redirect(request):
    """
    Redirects the user to the current month's calendar if they are an admin.
    Otherwise, displays an error message and redirects to login.
    """
    user = request.user
    if user.is_authenticated and user.is_superuser:
        today = datetime.today()
        return redirect('calendar_view', year=today.year, month=today.month)
    else:
        messages.error(request, 'You have to log in as an Admin to access this page.')
        return redirect('login')

def day_view(request, year, month, day):
    """
    Displays events occurring on a specific day, accessible only by admins.
    """
    user = request.user
    if user.is_authenticated and user.is_superuser:
        try:
            formatted_date = datetime(year, month, day).strftime("%d %B, %Y")  # Format date nicely
            day_start = datetime(year, month, day)  # Start of the selected day
            day_end = datetime(year, month, day, 23, 59, 59)  # End of the selected day
            
            # Fetch events that are active on this day
            events = CalendarEvent.objects.filter(
                start_date__lte=day_end,
                end_date__gte=day_start
            )
            
            return render(request, 'calendar_app/day_view.html', {
                'events': events,
                'formatted_date': formatted_date,
                'year': year,
                'month': month,
                'day': day
            })
        except ValueError:
            return render(request, 'calendar_app/error.html', {'error_message': "Invalid date selected."})
    else:
        messages.error(request, 'You have to log in as an Admin to access this page.')
        return redirect('login')

def get_events(request, year, month, day):
    """
    Returns event data for a specific date as a JSON response.
    """
    try:
        selected_date = date(year, month, day)  # Convert to date object
        events = CalendarEvent.objects.filter(
            start_date__lte=selected_date,
            end_date__gte=selected_date
        )
        
        # Prepare event data in JSON format
        event_data = []
        for event in events:
            event_data.append({
                "tenant_name": event.tenant.name,
                "apartment_number": event.apartment.number,
                "start_date": event.start_date.strftime("%d %B, %Y"),
                "end_date": event.end_date.strftime("%d %B, %Y"),
                "tenant_status": event.tenant.status,
                "tenant_remarks": event.tenant.remarks,
            })
        
        return JsonResponse({"events": event_data})
    except ValueError:
        return JsonResponse({"error": "Invalid date"}, status=400)

def engaged_apartments(request):
    today = now().date()
    print(today)
    # Get the filter dates from the request
    start_date = request.GET.get('start_date', now().date())
    end_date = request.GET.get('end_date', now().date() + timedelta(days=30))  # Default to next 30 days

    # Convert to datetime objects
    start_date = datetime.strptime(str(start_date), "%Y-%m-%d").date()
    end_date = datetime.strptime(str(end_date), "%Y-%m-%d").date()

    print(start_date, end_date)
    
    # Fetch engaged apartments (those with at least one tenant)
    engaged_apartments = Apartment.objects.filter(
        tenant__isnull=False,
        tenant__move_in_date__lte=end_date,
        tenant__move_out_date__gte=start_date).distinct().order_by('number')

    # Collect tenant data per apartment
    apartment_data = []
    for apartment in engaged_apartments:
        # print(apartment)
        tenants = Tenant.objects.filter(apartment=apartment).order_by("move_in_date")
        tenant_entries = []
        
        for tenant in tenants:
            # print(f"for apartment {apartment}, tenant: {tenant}" )
            if tenant.move_out_date and tenant.move_out_date.date() >= start_date:
                move_in = tenant.move_in_date.date()
                # print(f"{tenant.name} move in date: {tenant.move_in_date.date()} and move_in: {move_in}")
                move_out = tenant.move_out_date.date() if tenant.move_out_date else None
                # print(f"{tenant.name} move out date: {tenant.move_out_date.date()} and move_out: {move_out}")

                # Prepare date range for visualization
                date_range = []
                if move_out:
                    current_date = move_in
                    while current_date <= move_out and current_date <= end_date:
                        if current_date >= start_date:
                            date_range.append(current_date.strftime("%Y-%m-%d"))
                        current_date += timedelta(days=1)

                tenant_entries.append({
                    "name": tenant.name,
                    "year": move_in.year,
                    "move_in": move_in.strftime("%Y-%m-%d"),
                    "move_out": move_out.strftime("%Y-%m-%d") if move_out else "Present",
                    "dates": date_range
                })
                # print(f"name : {tenant.name}, year : {move_in.year}, ")
        
        apartment_data.append({
            "apartment": apartment,
            "tenants": tenant_entries
        })

    context = {
        "apartment_data": apartment_data,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "date_range": [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)],
        "today": today,

    }
    return render(request, "calendar_app/engaged_apartments.html", context)