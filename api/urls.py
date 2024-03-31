from django.urls import path
from . import views
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (

    TokenRefreshView,
)
appname = 'api'
urlpatterns = [
    path('routes/', views.routes, name='routes'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', views.users, name='users'),
    path('user/<int:id>/', views.user, name='user'),
    path('username/<str:username>/', views.username, name='username'),
    path('email_exists/<str:email>/', views.email_exists, name='email_exists'),
    path('signup/', views.signup, name='signup'),
    path('email_verify/', views.email_verify, name='email_verify'),
    path('resend/<int:id>/', views.resend, name='resend'),
    path('upload_pic/<int:id>/', views.upload_pic, name='upload_pic'),
    path('edit_user/<int:id>/', views.edit_user, name='edit_user'),
    path('edit_details1/<int:id>/', views.edit_details1, name='edit_details1'),
    path('edit_details2/', views.edit_details2, name='edit_details2'),
    path('edit_password/<int:id>/', views.edit_password, name='edit_password'),
    path('delete_user/<int:id>/', views.delete_user, name='delete_user'),
    path('email_verify_password1/<int:id>/', views.email_verify_password1, name='email_verify_password1'),
    path('email_verify_password2/', views.email_verify_password2, name='email_verify_password2'),
    path('search_user/<str:username>/', views.search_user, name='search_user'),
    path('cars/', views.cars, name='cars'),
    path('addCar/<int:id>/', views.addCar, name='addCar'),
    path('user_cars/<int:id>/', views.user_cars, name='user_cars'),
    path('add_license/<int:id>/', views.add_license, name='add_license'),
    path('filter_cars/', views.filter_cars, name='filter_cars'),
    path('my_trips/<int:id>/', views.my_trips, name='my_trips'),
    path('add_trip/', views.add_trip, name='add_trip'),
    path('trips/', views.trips, name='trips'),
    path('add_trip_photos/<int:id>/', views.add_trip_photos, name='add_trip_photos'),
    path('get_trip/<int:id>/', views.get_trip, name='get_trip'),
    path('delete_image/', views.delete_image, name='delete_image'),
    path('all_images/', views.all_images, name='all_images'),
    path('edit_trip/<int:id>/', views.edit_trip, name='edit_trip'),
    path('client_trips/<int:id>/', views.client_trips, name='client_trips')
]