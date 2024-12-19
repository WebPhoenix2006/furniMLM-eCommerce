from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("cart/", views.cart, name="cart"),
    path('cart/add/', views.add_to_cart, name='add_to_cart'), 
    path('cart/update/', views.update_cart, name='update_cart'), 
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    path("shop/", views.shop, name="shop"),
    path("blog/", views.blog, name="blog"),
    path("contact/", views.contact, name="contact"),
    path("services/", views.services, name="services"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup_view, name="signup"),
]
