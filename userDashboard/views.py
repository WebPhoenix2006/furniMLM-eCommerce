from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .decorators import custom_login_required

@custom_login_required
def dashboard(request):
    return render(request, 'userDashboard/index.html')
def analytics(request):
    return render(request, 'userDashboard/analytics.html')
def network(request):
    return render(request, 'userDashboard/network.html')
def orders(request):
    return render(request, 'userDashboard/orders.html')
def profile(request):
    return render(request, 'userDashboard/profile.html')
def referrals(request):
    return render(request, 'userDashboard/referrals.html')
def support(request):
    return render(request, 'userDashboard/support.html')
def notfound(request):
    return render(request, 'userDashboard/404.html')

# @login_required(login_url="login")  # URL to redirect unauthenticated users
# def dashboard(request):
#     return render(request, "dashboard/index.html")


def logout_view(request):
    logout(request)  # Logs out the user
    return redirect("login")  # Redirect to the login page after logout
def custom_dashboard_redirect(request):
    messages.error(request, "You need to log in to access the dashboard.")
    return redirect('login')  # Replace 'login' with your login page URL name

