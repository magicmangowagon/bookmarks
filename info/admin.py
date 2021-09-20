from django.contrib import admin
from .models import BaseInfo, InfoCategory, DiscussionBoard, DiscussionTopic, QuestionStub, FakeLO, FakeCompetency
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


@admin.register(FakeLO)
class FakeLOAdmin(admin.ModelAdmin):
    list_display = ['name']
    filter_horizontal = ['questionGroup', ]


@admin.register(QuestionStub)
class QuestionStubAdmin(admin.ModelAdmin):
    list_display = ['question', 'questionCategory']


@admin.register(FakeCompetency)
class FakeCompAdmin(admin.ModelAdmin):
    list_display = ['name']
    filter_horizontal = ['fakeLos', ]
