from pydoc_data.topics import topics
from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
#rooms=[
 #   { 'id': 1, 'name': 'Lets learn python'},
  #  { 'id': 2, 'name': 'Design with me'},
   # { 'id': 3, 'name': 'Frontend developers'},

#] 

def loginPage(request):
    page='login'

    if request.user.is_authenticated:
        return redirect ('home')

    if request.method =='POST':
        username= request.POST.get('username')
        password=request.POST.get('password')

        try:
            user= User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')    

        user= authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')
    context={'page': page}
    return render(request, "base/login_register.html", context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page= 'register'
    form= UserCreationForm()

    if request.method == 'POST':
        form= UserCreationForm(request.POST)
        if form.is_valid():
            user= form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occured during registration")
    return render (request, 'base/login_register.html', {'form': form})

def home(request):
    q= request.GET.get('q') if request.GET.get('q')!= None else ''
    rooms=Room.objects.filter(
    Q(topic__name__contains=q) |
    Q(name__icontains=q) |
    Q(description__icontains=q)
    )

    
    topics= Topic.objects.all() 
    room_count= rooms.count()

    context={'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/home.html', context) #displays information in the home htlm file


def room(request, pk):
    room-Room.objects.get(id=pk)
    messages= room.message_set.all()
    context= {'room': room, 'messages': messages}
    return render(request, 'base/room.html', context) #displays information in the home room file

@login_required(login_url='login') #login required before creating a room
def createRoom(request):
    form=RoomForm()
    if request.method== 'POST':
        form= RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form': form}
    return render(request, 'base/room_form.html', context)
    
@login_required(login_url='login') #login required before updating a room
def updateRoom(request, pk): #updates a room
    room= Room.objects.get(id=pk)
    form=RoomForm(instance=room)

    if request.user !=room.host:
        return HttpResponse('You are not allowed here')

    if request.method=='POST':
        form=RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form': form}
    return render(request, 'base/room_form.html', context)
@login_required(login_url='login') #login required before deleting a room
def deleteRoom(request, pk):
    room= Room.objects.get(id=pk)

    if request.user !=room.host:
        return HttpResponse('You are not allowed here')
        
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})