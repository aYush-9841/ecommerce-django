from django.views import View
from django.shortcuts import render, redirect
from store_app.models import Product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.core.exceptions import ValidationError

class AuthView(View):
    def get(self, request):
        return render(request, 'register/auth.html')

def BASE(request):
    return render(request, 'main/base.html')

def HOME(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'main/index.html', context)

def product(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'main/product.html', context)

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        try:

            User.objects.get(email=email)
            return render(request, 'register/auth.html', {'error_message': 'Email address is already in use'})
        except User.DoesNotExist:

            if pass1 != pass2:
                return render(request, 'register/auth.html', {'error_message': 'Passwords do not match'})


            if not username:
                username = email.split('@')[0]


            customer = User.objects.create_user(username, email, pass1)
            customer.first_name = first_name
            customer.last_name = last_name
            customer.save()



            return redirect('register')

    return render(request, 'register/auth.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'register/auth.html', {'error_message': 'Invalid login credentials'})



def user_logout(request):
    logout(request)

    return render(request, 'register/auth.html')


