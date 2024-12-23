from django.urls import path
from . import views


urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("page_not_found/", views.notfound, name="page_not_found"),
    path("analytics/", views.analytics, name="analytics"),
    path("network/", views.network, name="network"),
    path("orders/", views.orders, name="orders"),
    path("profile/", views.profile, name="profile"),
    path("referrals/", views.referrals, name="referrals"),
    path("support/", views.support, name="support"),
    path("logout/", views.logout_view, name="logout"),
]
