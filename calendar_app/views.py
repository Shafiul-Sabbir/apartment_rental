from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib import messages
from .models import CalendarEvent
from datetime import datetime, date
import calendar

def calendar_view(request, year, month):
    today = datetime.today()
    today_date = today.day
    today_month = today.month
    today_year = today.year
    year = year or today.year
    if month > 12 or month < 1:
        month = today.month

    # Get the first day of the month and total days
    first_day_of_month = datetime(year, month, 1)
    _, total_days = calendar.monthrange(year, month)
    
    # Get previous and next month details
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    # Get previous month's last day
    _, prev_month_days = calendar.monthrange(prev_year, prev_month)

    # Generate calendar matrix (6 rows, 7 columns)
    month_calendar = []
    week = []
    first_weekday = first_day_of_month.weekday()  # 0 = Monday, 6 = Sunday
    
    # Fill previous month's dates to complete the first row
    for i in range(first_weekday):
        day = prev_month_days - first_weekday + i + 1
        week.append({"day": day, "month": prev_month, "year": prev_year, "extra": True })

    # Fill current month days
    for day in range(1, total_days + 1):
        week.append({"day": day, "month": month, "year": year, "extra": False})
        if len(week) == 7:
            month_calendar.append(week)
            week = []

    # Fill next month's dates to complete the last row
    next_day = 1
    while len(week) < 7:
        week.append({"day": next_day, "month": next_month, "year": next_year, "extra": True})
        next_day += 1
    if week:
        month_calendar.append(week)

    # Fetch events for all relevant dates
    events = CalendarEvent.objects.filter(
        start_date__year__in=[prev_year, year, next_year],
        start_date__month__in=[prev_month, month, next_month]
    )

    # Assign events to the respective dates
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
    user = request.user
    if user.is_authenticated and user.is_superuser :
        today = datetime.today()
        return redirect('calendar_view', year=today.year, month=today.month)
    else:
        messages.error(request, 'You have to log in as an Admin to access this page.')
        return redirect('login')

def day_view(request, year, month, day):
    user = request.user
    if user.is_authenticated and user.is_superuser :
        try:
            # Convert numerical date into a full formatted string
            formatted_date = datetime(year, month, day).strftime("%d %B, %Y")
            
            day_start = datetime(year, month, day)
            day_end = datetime(year, month, day, 23, 59, 59)
            
            events = CalendarEvent.objects.filter(
                start_date__lte=day_end,
                end_date__gte=day_start
            )
            
            return render(request, 'calendar_app/day_view.html', {
                'events': events,
                'formatted_date': formatted_date,  # Pass formatted date
                'year': year,
                'month': month,
                'day': day
            })
        except ValueError:
            return render(request, 'calendar_app/error.html', {'error_message': "Invalid date selected."})
    else:
        messages.error(request, 'You have to log in as an Admin to access this page.')
        return redirect('login')
    
from django.http import JsonResponse

def get_events(request, year, month, day):
    try:
        selected_date = date(year, month, day)
        events = CalendarEvent.objects.filter(
            start_date__lte=selected_date,
            end_date__gte=selected_date
        )

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

