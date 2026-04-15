from django.urls import path
from .views import signup_page, login_page, logout_page, home

urlpatterns = [
    path('signup/', signup_page, name='signup_page'),
    path('login/', login_page, name='login_page'),
    path('logout/', logout_page, name='logout_page'),
    path('', home, name='home'),
]