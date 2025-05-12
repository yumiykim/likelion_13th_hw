from django.contrib import admin
from django.contrib.auth.models import User
from accounts.models import Profile

# Profile을 User 아래에 인라인으로 붙임
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

# User admin에 ProfileInline 추가
class CustomUserAdmin(admin.ModelAdmin):
    inlines = (ProfileInline,)

# 기존 User admin을 커스텀 admin으로 덮어씀
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

