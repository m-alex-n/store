from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from django.shortcuts import render, redirect

from store.forms import CustomUserForm


def register(request):
    form = CustomUserForm()
    if request.method =='POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registerd successfully! Login to continue")
            return redirect ('loginpage')
    context = {'form':form}
    return render (request, 'store/auth/register.html', context )

def loginpage(request):
    if request.user.is_authenticated:
            messages.success(request, "You are already logged in")
            return redirect('home')
    else:
        if request.method == "POST":
            # get value from the post form 
            name = request.POST.get('username')
            passwd = request.POST.get('password')
            user = authenticate(request, username = name , password = passwd)

            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password")
                return redirect('loginpage')
        return render(request, "store/auth/login.html")


def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request , "Logged out successfully")
    return redirect('home')