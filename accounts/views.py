# accounts/views.py
import random
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth import login
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # Pause saving for a second

        # --- AUTO-GENERATE USERNAME ---
            # logic: "john@gmail.com" -> "john_4821"
            base_name = user.email.split('@')[0]
            random_id = random.randint(1000, 9999)
            user.username = f"{base_name}_{random_id}"
            # ------------------------------


            user.user_type = 'patient'     # FORCE type to be Patient
            user.save()                    # Now save to DB
            
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')