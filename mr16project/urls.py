from django.contrib import admin
from django.urls import path
from trips.views import home, history, delete_trip, edit_trip
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('history/', history, name='history'),
    path('delete/<int:trip_id>/', delete_trip, name='delete_trip'),
    path('edit/<int:trip_id>/', edit_trip, name='edit_trip'),
    path(
    'login/',
    auth_views.LoginView.as_view(
        template_name='login.html'
    ),
    name='login'
    ),
    path('logout/',
     auth_views.LogoutView.as_view(),
     name='logout'),
    ]