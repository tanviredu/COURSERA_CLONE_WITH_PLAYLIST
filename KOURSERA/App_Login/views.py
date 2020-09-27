from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from .models import User,Profile
from django.urls import reverse
from django.contrib import messages
from .forms import SignUpForm,ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate



def sign_up(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            ## profile is created by signals
            form.save()
            messages.success(request,"Account is Created")
            ## redirect to login
            return HttpResponseRedirect(reverse('App_Login:login'))
    
    return render(request,'App_Login/signup.html',{'form':form})


def login_user(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)
        
        if form.is_valid():
            ## username is the email
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username)
            print(password)
            user = authenticate(username=username,password=password)
            
            if user is not None:
                login(request,user)
                ## this is temporary Http Response
                ## return HttpResponse("You Are Logged IN")
                return HttpResponseRedirect(reverse('App_Shop:home'))
    
    return render(request,'App_Login/login.html',{'form':form})


@login_required
def logout_user(request):
    logout(request)
    messages.warning(request,"You are Logged Out")
    ## This is temporary
    return HttpResponseRedirect(reverse('App_Login:login'))


@login_required
def user_profile(request):
    profile = Profile.objects.get(user = request.user)
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,'Changed Saved')
            ## this is temporary
            return HttpResponseRedirect(reverse('App_Shop:home'))
    
    return render(request,"App_Login/change_profile.html",{'form':form})
    




