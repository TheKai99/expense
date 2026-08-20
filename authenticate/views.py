from django.shortcuts import render , redirect
from django.contrib.auth import authenticate ,login , logout
from django.contrib.auth.models  import User
from django.contrib import messages

# Create your views here.

def login_page(request):

    if request.method == 'POST':

        data = request.POST

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            messages.error(request , 'Fill all the fieds')
            return redirect('login_page')

        if not User.objects.filter(username = username).exists():
            messages.error(request , 'Invalid username or password')
            return redirect('login_page')

        user = authenticate(username = username , password = password)

        if user is None:
            messages.error(request , 'Invalid credentials')
            return redirect('login_page')

        else:
            login(request , user)
            return redirect('home')

    return render(request , 'login.html')

def register(request):

    if request.method == 'POST':

        data =request.POST

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        password = data.get('password')

        if not first_name or not last_name or not username or not password:
            messages.error(request , "All fields are required")
            return redirect('register')

        user = User.objects.filter(username = username)

        if user.exists():
            messages.info(request , 'username already exist')
            return redirect('register')

        user = User(
            first_name = first_name,
            last_name = last_name,
            username = username,

        )

        user.set_password(password)
        user.save()

        messages.success(request , 'Registerred Successfull')

        return redirect('login_page')


    return render(request , 'register.html')

def logout_page(request):

    logout(request)
    return redirect('login_page')
