from django.urls import path
from . import views


urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),
    path("manage-users/", views.manage_users, name="manage_users"),
]
