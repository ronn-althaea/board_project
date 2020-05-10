from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .models import BoardModel

# Create your views here.

def signupfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            User.objects.get(username=username)
            return render(request, 'signup.html', {'error': 'This user is already registed.'})
        except:
            user = User.objects.create_user(username, '', password)
            user.save()

    return render(request, 'signup.html')

def loginfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            return redirect('login')

    return render(request, 'login.html')

def logoutfunc(request):
    logout(request)
    return redirect('login')

@login_required
def listfunc(request):
    object_list = BoardModel.objects.all()
    return render(request, 'list.html', {'object_list': object_list})

@login_required
def detailfunc(request, pk):
    object = BoardModel.objects.get(pk=pk)
    return render(request, 'details.html', {'object': object})

def goodfunc(request, pk):
    post = BoardModel.objects.get(pk=pk)
    post.good = post.good + 1
    post.save()

    return redirect('list')

def readfunc(request, pk):
    post = BoardModel.objects.get(pk=pk)
    username = request.user.get_username()

    if username in post.readtext:
        return redirect('list')
    else:
        post.read += 1
        post.readtext = post.readtext + ',' + username
        post.save()
        return redirect('list')

class BoardCreate(CreateView):
    template_name = 'create.html'
    model = BoardModel
    fields = ('title', 'content', 'author', 'images')
    success_url = reverse_lazy('list')
