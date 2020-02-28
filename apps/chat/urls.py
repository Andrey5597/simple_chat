from django.urls import path
from .views import user_list

urlpatterns = [
    path('users/', user_list, name='All users'),
    path('users/<int:pk>', user_list, name='user-detail'),  # GET request for user with id
]
