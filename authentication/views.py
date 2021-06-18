from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import MyRegisterForm
from django.contrib.auth.decorators import login_required
# from .models import Profile

# Create your views here.

def register(request):

    if request.method == 'POST':
        form = MyRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'successfully created account for {username}')
            return redirect('login')
        else:
            print('some error')
    else:
        form = MyRegisterForm()
    return render(request, 'authentication/register.html', {'form': form})
