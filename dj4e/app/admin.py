from django.contrib import admin

from .models import CustomUser, Request

admin.site.register(Request)
admin.site.register(CustomUser)