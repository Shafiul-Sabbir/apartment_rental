from django.shortcuts import render, redirect
from django.utils.timezone import now
from .models import CalendarEvent
from datetime import datetime, timedelta
import calendar
from datetime import date

def calendar_view(request, year, month):
    today = datetime.today()
    year = year or today.year
    month = month or today.month
    month_calendar = calendar.monthcalendar(year, month)
    
    events = CalendarEvent.objects.filter(
        start_date__month=month, start_date__year=year
    )

    calendar_data = []
    for week in month_calendar:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append(None)
            else:
                # Construct a full date object for filtering
                date_obj = date(year, month, day)
                tenants = events.filter(start_date__lte=date_obj, end_date__gte=date_obj)
                
                week_data.append({"day": day, "tenants": tenants})  # Store tenants correctly
        calendar_data.append(week_data)

    # Calculate previous and next month
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    return render(request, 'calendar_app/calendar.html', {
        'calendar_data': calendar_data,
        'year': year,
        'month': month,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
    })

def calendar_redirect(request):
    today = datetime.today()
    return redirect('calendar_view', year=today.year, month=today.month)

def day_view(request, year, month, day):
    day_start = datetime(year, month, day)
    day_end = datetime(year, month, day, 23, 59, 59)
    events = CalendarEvent.objects.filter(
        start_date__lte=day_end,
        end_date__gte=day_start
    )
    
    
    return render(request, 'calendar_app/day_view.html', {
        'events': events,
        'year': year,
        'month': month,
        'day': day
    })