from django.contrib import admin
from .models import ChallengeListSort

# Register your models here.
@admin.register(ChallengeListSort)
class ChallengeListOrderAdmin(admin.ModelAdmin):
    model = ChallengeListSort
