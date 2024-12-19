from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator

from .forms import CustomUserCreationForm, ProfileForm

import json
from .models import Cart, Product, Category


# Home view
def home(request):
    return render(request, "ecommerce/index.html")


def signup_view(request):
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect("login")
    else:
        user_form = CustomUserCreationForm()
        profile_form = ProfileForm()
    return render(
        request,
        "ecommerce/sign-up.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


# Login view
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
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = AuthenticationForm()
    return render(request, "ecommerce/login.html", {"form": form})


# Logout view
def logout_view(request):
    logout(request)
    return redirect("login")


# Dashboard redirect for unauthenticated users
def custom_dashboard_redirect(request):
    messages.error(request, "You need to log in to access the dashboard.")
    return redirect("login")


# Cart view
def cart(request):
    if not request.user.is_authenticated:
        # If the user is not authenticated, render the empty cart
        return render(
            request, "ecommerce/cart.html", {"cartitems": [], "total_price": 0}
        )

    # Fetch the cart items for the authenticated user
    cartitems = Cart.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cartitems)
    return render(
        request,
        "ecommerce/cart.html",
        {"cartitems": cartitems, "total_price": total_price},
    )


@csrf_exempt
def add_to_cart(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"status": "error", "message": "User not authenticated"}, status=403
        )

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            item_id = data.get("item_id")

            if item_id:
                product = Product.objects.get(id=item_id)
                cart_item, created = Cart.objects.get_or_create(
                    user=request.user, item=product
                )
                if not created:
                    cart_item.quantity += 1
                cart_item.save()
                return JsonResponse({"status": "success"})
            return JsonResponse(
                {"status": "error", "message": "Item ID missing"}, status=400
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON"}, status=400
            )

        except Product.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Product not found"}, status=404
            )

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


@csrf_exempt
def update_cart(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"status": "error", "message": "User not authenticated"}, status=403
        )

    if request.method == "POST":
        data = json.loads(request.body)
        item_id = data.get("item_id")
        quantity = data.get("quantity")

        if item_id and quantity:
            try:
                cart_item = Cart.objects.get(user=request.user, item__id=item_id)
                cart_item.quantity = quantity
                cart_item.save()
                return JsonResponse({"status": "success"})
            except Cart.DoesNotExist:
                return JsonResponse(
                    {"status": "error", "message": "Item not found"}, status=404
                )

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


@csrf_exempt
def remove_from_cart(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"status": "error", "message": "User not authenticated"}, status=403
        )

    if request.method == "POST":
        data = json.loads(request.body)
        item_id = data.get("item_id")

        if item_id:
            try:
                cart_item = Cart.objects.get(user=request.user, item__id=item_id)
                cart_item.delete()
                return JsonResponse({"status": "success"})
            except Cart.DoesNotExist:
                return JsonResponse(
                    {"status": "error", "message": "Item not found"}, status=404
                )

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


# Shop view with pagination
def shop(request):
    categories = Category.objects.all()
    selected_category = request.GET.get("category")
    products = (
        Product.objects.filter(category__name=selected_category)
        if selected_category
        else Product.objects.all()
    )

    # Set up pagination
    paginator = Paginator(products, 10)  # Show 10 products per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "ecommerce/shop.html",
        {
            "page_obj": page_obj,
            "categories": categories,
            "selected_category": selected_category,
        },
    )


# About view
def about(request):
    return render(request, "ecommerce/about.html")


# Blog view
def blog(request):
    return render(request, "ecommerce/blog.html")


# Contact view
def contact(request):
    return render(request, "ecommerce/contact.html")


# Services view
def services(request):
    return render(request, "ecommerce/services.html")
