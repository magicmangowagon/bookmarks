from django.contrib import admin
from .models import BaseInfo
# Register your models here.


@admin.register(BaseInfo)
class BaseInfo(admin.ModelAdmin):
    list_display = ['title']
    filter_horizontal = ('learningExpos',)
