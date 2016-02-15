from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from quora.profile.forms import SignUpForm
from django.contrib.auth.models import User

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, 'auth/signup.html', {'form': form})
        else:
            firstname = form.cleaned_data.get('firstname')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(
                first_name=firstname,
                username=username,
                password=password)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        return render(request, 'auth/signup.html', {'form': SignUpForm()})

