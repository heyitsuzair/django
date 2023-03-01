from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm

# Create your views here.

# rooms = [
#     {"id": 1, "name": "Lets Learn Python"},
#     {"id": 2, "name": "Lets Learn Js"},
#     {"id": 3, "name": "Lets Learn PHP"},
#     {"id": 4, "name": "Lets Learn C"},
#     {"id": 5, "name": "Lets Learn Java"}
# ]


def home(request):
    rooms = Room.objects.all()
    home_data = {'rooms': rooms}
    return render(request, 'base/home.html', home_data)


def room(request, pk):
    found_room = Room.objects.get(id=pk)
    room_data = {'room': found_room}
    return render(request, 'base/room.html', room_data)


def create_room(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {"form": form}

    return render(request, 'base/room_form.html', context)


def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {"form": form}

    return render(request, 'base/room_form.html', context)


def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})
