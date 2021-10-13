from django.contrib import admin

from .models import Users, Product


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ("tele_id", "first_name", "last_name", "age", "phone")
    list_filter = ("first_name", "last_name", "age")
    search_fields = ("last_name__startswith", "first_name__startswith")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "qty", "desc", "price", "img", "availability")
