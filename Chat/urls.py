from django.urls import path
from .views import chat_room,redirect_to_room

urlpatterns = [
    path('chat/',redirect_to_room,name='chat'),
    path('chat/<str:room_name>/', chat_room, name='chat_room'),
]