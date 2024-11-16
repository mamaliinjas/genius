from django.shortcuts import render , redirect
from django.contrib.auth.models import auth , User
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request , 'home.html')

def register(request):
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request , 'EMAIL IS ALREADY USED')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request , 'USERNAME IS TAKEN')
                return redirect(register)
            else:
                user=User.objects.create_user(username=username , email=email , password=password)
                user.save();
                return redirect('login')
        else:
            messages.info(request , 'password not the same')
            return redirect('register')
            
    else:    
         return render(request , 'register.html')