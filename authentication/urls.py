from django import urls
from . import views


urlpatterns = [
    urls.path('register/', views.register, name='register'),
    urls.path('login/', views.login, name='login'),
    urls.path('logout/', views.logout, name='logout'),
    urls.path('update_profile/', views.update_profile, name='update_profile'),
    urls.path('change_password/', views.change_password, name='change_password')
]