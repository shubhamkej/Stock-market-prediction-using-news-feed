from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User

def signup(request):
    if request.method == 'POST':
        #REGISTER USER HERE
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['password2']
        
        #First check if passwords match or not
        if password1 == password2:

            #Check for username 
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is already taken")
                return redirect('signup')
            else:
                #Check for email 
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is is being used')
                    return redirect('signup')
                else:
                    #Everything looks good
                    user = User.objects.create_user(username=username, password=password1,
                    email=email,first_name=first_name, last_name=last_name)
                    user.save()
                    messages.success(request, 'You have registered successfully and can log in')
                    return redirect('login')

        else:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')

    else:
        return render(request, 'accounts/signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('dashboard')

        else:
            messages.error(request, 'Please provide valid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are logged out successfully!')
        return redirect('login')