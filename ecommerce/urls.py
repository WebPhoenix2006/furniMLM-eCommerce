from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("cart/", views.cart, name="cart"),
    path("shop/", views.shop, name="shop"),
    path("login/", views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path("signup/", views.signup_view, name="signup"),
]
