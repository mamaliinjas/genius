from django.shortcuts import render , redirect
from django.contrib.auth.models import  User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout

# Create your views here.

def home(request):
    return render(request , 'home.html')

def register(request):
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        
        if password != password2:
            messages.info(request, 'Passwords do not match')
            return render(request, 'register.html', {'username': username, 'email': email})
        
        if User.objects.filter(email=email).exists():
            messages.info(request, 'EMAIL IS ALREADY USED')
            return render(request, 'register.html', {'username': username, 'email': email})
        
        if User.objects.filter(username=username).exists():
            messages.info(request, 'USERNAME IS TAKEN')
            return render(request, 'register.html', {'username': username, 'email': email})

            
    else:    
         return render(request , 'register.html')
     
def login(request):
    if request.method == 'POST':
        login_input = request.POST['login_input']
        password = request.POST['password']
        
 
        try:
            user = User.objects.get(email=login_input)
            username = user.username
        except User.DoesNotExist:
            username = login_input

     
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid email/username or password')
            return redirect('login') 
    return render(request, 'login.html') 
                