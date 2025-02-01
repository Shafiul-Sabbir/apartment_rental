from django import urls
from . import views


urlpatterns = [
    urls.path('register/', views.register, name='register'),
    urls.path('login/', views.login, name='login'),
    urls.path('logout/', views.logout, name='logout'),
]