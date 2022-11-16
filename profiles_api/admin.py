from django.contrib import admin
from profiles_api.models import *

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'nickname', 'is_active', 'is_staff')

admin.site.register(UserProfile, CustomUserAdmin)
admin.site.register(TokenModel)