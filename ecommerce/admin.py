from django.contrib import admin
from .models import Order, Product, Profile, Category
from django.contrib.auth.models import User
from .models import Cart

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "profile"

class UserAdmin(admin.ModelAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "description",
        "is_sale",
        "sale_price",
        "category",  # Added category to display
    )
    list_filter = ("category", "is_sale")  # Added filter for category and sale status
    search_fields = ("name", "category__name")  # Enable searching by name and category

admin.site.register(Order)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "item",
        "quantity",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at", "updated_at")
    search_fields = ("item__name", "user__username")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
