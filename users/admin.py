from django.contrib import admin

from .models import User, UserProfile, Post


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class UserAdmin(admin.ModelAdmin):
    pass
