from django.contrib import admin
from profiles_api.models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(TokenModel)