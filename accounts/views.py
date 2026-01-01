# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            # Role-based redirect
            if user.groups.filter(name='Nurse').exists():
                return redirect('nurse_dashboard')
            elif user.groups.filter(name='Doctor').exists():
                return redirect('doctor_dashboard')
            elif user.groups.filter(name='Patient').exists():
                return redirect('patient_dashboard')
            else:
                return redirect('admin_dashboard')

    return render(request, 'accounts/login.html')
