from django.db import models
from django.contrib.auth.models import User
import datetime
import random

ROLE_CHOICES = [
    ("distributor", "Independent Distributor/Representative"),
    ("team_leader", "Team Leader"),
    ("recruiter", "Recruiter"),
    ("customer", "Customer"),
]


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    description = models.TextField(default="", blank=True, null=True)
    image = models.ImageField(upload_to="uploads/product/")
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products", default=1
    )

    def __str__(self):
        return self.name

    def get_effective_price(self):
        return self.sale_price if self.is_sale else self.price

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = random.randint(1000, 9999)
        super().save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    referral = models.CharField(max_length=50, blank=True, null=True)
    position = models.CharField(
        max_length=10, choices=[("Left", "Left"), ("Right", "Right")]
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="customer")
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    address = models.CharField(max_length=255, default="", blank=True)
    phone = models.CharField(max_length=20, default="", blank=True)
    date = models.DateField(default=datetime.date.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Order: {self.product.name} - {self.customer.user.username}"

    def get_total_price(self):
        return self.product.get_effective_price() * self.quantity


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item.name} - {self.quantity}"

    def get_total_price(self):
        price = self.item.sale_price if self.item.is_sale else self.item.price
        return price * self.quantity
