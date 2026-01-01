from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import login
from .forms import NurseRegistrationForm
from .models import Nurse

def nurse_register(request):
    if request.method == 'POST':
        form = NurseRegistrationForm(request.POST)
        if form.is_valid():
            # Create User
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )

            # Assign Nurse group
            nurse_group = Group.objects.get(name='Nurse')
            user.groups.add(nurse_group)

            # Create Nurse profile
            nurse = form.save(commit=False)
            nurse.user = user
            nurse.save()

            login(request, user)
            return redirect('nurse_dashboard')
    else:
        form = NurseRegistrationForm()

    return render(request, 'nurses/register.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def nurse_dashboard(request):
    return render(request, 'nurses/dashboard.html')

