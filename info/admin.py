from django.contrib import admin
from .models import BaseInfo, InfoCategory, DiscussionBoard, DiscussionTopic
from rubrics.models import LearningExperience
from adminsortable2.admin import SortableInlineAdminMixin
# Register your models here.


@admin.register(InfoCategory)
class CategoryAdmin(admin.ModelAdmin):
    model = InfoCategory


@admin.register(BaseInfo)
class BaseInfo(admin.ModelAdmin):
    list_display = ['title', ]
    filter_horizontal = ('learningExpos', 'category')


@admin.register(DiscussionTopic)
class DiscussionTopic(admin.ModelAdmin):
    list_display = ['title', 'creator', 'creationDate', 'board']


@admin.register(DiscussionBoard)
class DiscussionBoardAdmin(admin.ModelAdmin):
    list_display = ['challenge']



