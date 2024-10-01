from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from forms import SignUpForm
from django import forms

def product(request,pk):
    product = Product.objects.get(id=pk)
    return  render(request, 'product.html', {'product':product})

def home(request): 
    products = Product.objects.all()
    return  render(request, 'home.html', {'products':products})


def shop(request):
    products = Product.objects.all()
    return  render(request, 'shop.html', {'products':products})


def preorder(request):
    return  render(request, 'pre-order.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You have logged in successfully'))
            return redirect('home')
        else:
            messages.success(request, ('The details you have entered are incorrect'))
            return redirect('login')
    else:  
     return  render(request, 'login.html', {})
     
def logout_user(request):
    logout(request)
    messages.success(request, ("You have logged out sucessfully"))
    return redirect('home')

def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# first_name = form.cleaned_data['first_name']
			# second_name = form.cleaned_data['second_name']
			# email = form.cleaned_data['email']
			# Log in user
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, ("You have successfully registered! Welcome!"))
			return redirect('home')
          	
	return render(request, "register.html", {'form':form})

def update_user(request):
     return render(request, "update_user.html") 


def slideshow(request):
    products = Product.objects.all()
    return  render(request, 'home.html', {'products':products})
