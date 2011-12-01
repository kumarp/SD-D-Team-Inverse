# auth/views.py
from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def login_user(request):
    state = "Please log in below..."
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
                #return HttpResponseRedirect('http://www.youtube.com/watch?v=oHg5SJYRHA0')
                return HttpResponseRedirect('/interests/')
            else:
                state = "Your account is not active. Please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

    return render_to_response('login.html',{'state':state, 'username': username},
                              context_instance=RequestContext(request))
	
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login/')
    else:
        form = UserCreationForm()

    return render_to_response('register.html', {'form' : form}, 
                              context_instance=RequestContext(request))
    
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login/')