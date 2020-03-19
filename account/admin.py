from django.contrib import admin
from .models import Profile
from centralDispatch.models import SolutionRouter


class SolutionRouterInline(admin.TabularInline):
    model = SolutionRouter
    extra = 0


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo', 'role']
    inlines = [SolutionRouterInline, ]
