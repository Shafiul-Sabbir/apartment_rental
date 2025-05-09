from django.urls import path
from . import views

urlpatterns = [
path('', views.calendar_redirect, name='calendar_redirect'),  # Redirect to current month
path('<int:year>/<int:month>/', views.calendar_view, name='calendar_view'),
path('<int:year>/<int:month>/<int:day>/', views.day_view, name='day_view'),
path('get-events/<int:year>/<int:month>/<int:day>/', views.get_events, name='get_events'),  # New API
path('engaged-apartments/', views.engaged_apartments, name='engaged_apartments'),  # New view

]