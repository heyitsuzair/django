from django.shortcuts import render

# Create your views here.

rooms = [
    {"id": 1, "name": "Lets Learn Python"},
    {"id": 2, "name": "Lets Learn Js"},
    {"id": 3, "name": "Lets Learn PHP"},
    {"id": 4, "name": "Lets Learn C"},
    {"id": 5, "name": "Lets Learn Java"}
]


def home(request):
    home_data = {'rooms': rooms}
    return render(request, 'base/home.html', home_data)


def room(request, pk):
    found_room = None

    for i in rooms:
        if i['id'] == int(pk):
            found_room = i

    room_data = {'room': found_room}
    return render(request, 'base/room.html', room_data)
