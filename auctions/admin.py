from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.
# class CustomAdmin(UserAdmin):
#     model = User
#     list_display = ['username', 'email', 'first_name', 'last_name','is_staff']

# admin.site.register(User, CustomAdmin)
