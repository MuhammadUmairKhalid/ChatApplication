# Create your views here.
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import ChatRoom

@login_required
def chat_room(request, room_name):
    ChatRoom.objects.get_or_create(name=room_name)
    return render(request, "chat_room.html", {
        "room_name": room_name
    })

def redirect_to_room(request):
    room = request.GET.get("room")
    return redirect(f"/chat/{room}/")