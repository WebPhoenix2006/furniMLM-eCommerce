from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm


# Home view
def home(request):
    return render(request, "ecommerce/index.html")


# Sign-up view (using Django's default UserCreationForm)


def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "ecommerce/sign-up.html", {"form": form})


# Login view (using Django's default AuthenticationForm)
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect(
                    "dashboard"
                )  # Redirect to the dashboard page after login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = AuthenticationForm()
    return render(request, "ecommerce/login.html", {"form": form})


def logout_view(request):
    logout(request)  # Logs out the user
    return redirect("login")  # Redirect to the login page after logout
def custom_dashboard_redirect(request):
    messages.error(request, "You need to log in to access the dashboard.")
    return redirect('login')  # Replace 'login' with your login page URL name

# Other views
def about(request):
    return render(request, "ecommerce/about.html")


def cart(request):
    return render(request, "ecommerce/cart.html")


def shop(request):
    return render(request, "ecommerce/shop.html", {"range": range(8)})
