from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from .models import Room, Topic, Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

# rooms = [
#     {"id": 1, "name": "Lets Learn Python"},
#     {"id": 2, "name": "Lets Learn Js"},
#     {"id": 3, "name": "Lets Learn PHP"},
#     {"id": 4, "name": "Lets Learn C"},
#     {"id": 5, "name": "Lets Learn Java"}
# ]


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User Doesnot Exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

    context = {"page": page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return HttpResponseRedirect('/')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An Error Occured')

    context = {"form": form}
    return render(request, 'base/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))

    topics = Topic.objects.all()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    room_count = rooms.count()

    home_data = {'rooms': rooms, 'topics': topics,
                 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', home_data)


def room(request, pk):
    found_room = Room.objects.get(id=pk)
    room_messages = found_room.message_set.all()
    participants = found_room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user, room=found_room, body=request.POST.get('body'))
        found_room.participants.add(request.user)
        return redirect('room', pk=found_room.id)

    room_data = {'room': found_room,
                 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', room_data)


@login_required(login_url='login')
def create_room(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {"form": form}

    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You Are Not Allowed Here')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {"form": form}

    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def delete_mesage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You Are Not Allowed Here')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})
