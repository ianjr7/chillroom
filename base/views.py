from email import message
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Room, Topic, Message
from .forms import RoomForms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


def about_us(request):
    return render(request, 'base/about_us.html')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(desription__icontains=q)
    )
    room_count = rooms.count()
    message = Message.objects.all()

    topics = Topic.objects.all()
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 
                'message': message}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    messages_room = room.message_set.all().order_by('create')

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)


    context = {'room': room, 'messages_room': messages_room}
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForms()

    if request.method == 'POST':
        form = RoomForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForms(instance=room)

    if request.user != room.host:
        return HttpResponse('you are not allowed here')

    if request.method == 'POST':
        form = RoomForms(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):    
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('you are not allowed here')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'obj': room}
    return render(request, 'base/delete.html', context)


def loginPage(request):

    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'user does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
             messages.error(request, 'user or password does not exist')


    context = {'page': page}
    return render(request, 'base/login_registration.html', context)

def logOut(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user =  form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    return render(request, 'base/login_registration.html', {'form': form})


@login_required(login_url='login')
def deleteMessage(request, pk):    
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('you are not allowed here')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    context = {'obj': message}
    return render(request, 'base/delete.html', context)

