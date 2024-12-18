from django.shortcuts import redirect
from django.contrib import messages

def custom_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You need to log in to access the dashboard.")
            return redirect('login')  # Replace 'login' with the name of your login URL
        return view_func(request, *args, **kwargs)
    return wrapper
