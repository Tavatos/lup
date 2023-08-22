from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import User_Profile
from itertools import chain
import random

# Create your views here.
def index(request):
    user_object = User.objects.get(username=request.user.username)
    # user_profile = User_Profile.objects.get(user=user_object)
    return render(request, 'index.html')


def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = User_Profile.objects.get(user=user_object)
    
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        
    }
    return render(request, 'profile.html', context)

# def e_profile(request):
#     eprofile = PublicEntity.objects.get()


#     return render(request, 'profile_2.html')

# @login_required(login_url='signin')
def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already in use")
                return redirect(signup)
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = User_Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
                

        else:
            messages.info(request, 'Password does not match')
            return redirect('signup')

    else: 
        return render(request, 'signup.html')

def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/profiles')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def settings(request):
    user_profile = User_Profile.objects.get(user=request.user)

    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['about']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['about']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        return redirect('settings')

    return render(request, 'setting.html', {'user_profile': user_profile}) 

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')