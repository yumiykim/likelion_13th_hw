from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Profile
from datetime import datetime  # 생일 문자열 처리용


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('main:mainpage')
        
        else:
            return render(request, 'accounts/login.html')

    elif request.method == 'GET':
        return render(request, 'accounts/login.html')
    

def logout(request):
    auth.logout(request)
    return redirect('main:mainpage')

def signup(request):
    if request.method == 'POST':

        if request.POST['password'] == request.POST['confirm']:
            user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password']
            )
            
            # 생일: 문자열 → date 객체로 변환
            birthday_str = request.POST.get('birthday')
            birthday = None
            if birthday_str:
                birthday = datetime.strptime(birthday_str, "%Y-%m-%d").date()
            
            phone=request.POST.get('phone')

            profile = Profile(user=user, birthday=birthday, phone=phone)
            profile.save()

            auth.login(request, user)
            return redirect('/')
        
    return render(request, 'accounts/signup.html')