# auth/views.py
from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# View function to log in
def login_user(request):
    state = "Please log in below..."
    username = password = ''
    # if there is a POST request, the user has entered information, store the info in variables
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate the user
        user = authenticate(username=username, password=password)
        # if authenticate succeeded, the user gets logged in
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
                # send logged in user to the "Interests" page
                return HttpResponseRedirect('/interests/')
            # in case user is not active
            else:
                state = "Your account is not active. Please contact the site admin."
        # could not authenticate
        else:
            state = "Your username and/or password were incorrect."
    
    # Render the view to the login.html template
    return render_to_response('login.html',{'state':state, 'username': username},
                              context_instance=RequestContext(request))

# View function to register                              
def register(request):
    if request.method == 'POST':
        # User is trying to send the form
        form = UserCreationForm(request.POST)
        # Validate the form fields and register
        if form.is_valid():
            form.save()
            # Redirect to Login page on successful registration
            return HttpResponseRedirect('/login/')
    else:
        # Create a blank user creation form
        form = UserCreationForm()

    # Render the view to the register.html template
    return render_to_response('register.html', {'form' : form}, 
                              context_instance=RequestContext(request))

# Function for logout                             
def logout_user(request):
    logout(request)
    # Redirect to Login page
    return HttpResponseRedirect('/login/')
    
# Function to create an anonymous account for unregistered users
def anonymous(request):
    # Assign a guest username and number
    user_num = User.objects.filter(username__startswith='guest_').count()
    username = "guest_" + str(user_num)
    
    # Create guest account
    user = User.objects.create_user(username, "bogus@email.com", "dummypassword")
    
    # Log in user
    user = authenticate(username=username, password="dummypassword")
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a random match chat
            return HttpResponseRedirect('/match_random/')
    else:
        return HttpResponse('Sorry, something broke. :(')
        
