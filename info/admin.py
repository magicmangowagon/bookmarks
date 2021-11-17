from django.contrib import admin
from .models import BaseInfo, InfoCategory, DiscussionBoard, DiscussionTopic, QuestionStub, FakeLO, FakeCompetency, \
    Prompts, CommentContainer, DesignJournal, DjPage, DjResponse, DjPrompt
from rubrics.models import LearningExperience
from adminsortable2.admin import SortableInlineAdminMixin
# Register your models here.


@admin.register(InfoCategory)
class CategoryAdmin(admin.ModelAdmin):
    model = InfoCategory


@admin.register(Prompts)
class PromptsAdmin(admin.ModelAdmin):
    model = Prompts
    list_display = ['question', 'response']


@admin.register(CommentContainer)
class CommentContainerAdmin(admin.ModelAdmin):
    list_display = ['comment', 'baseInfo', 'coordinates']


@admin.register(BaseInfo)
class BaseInfo(admin.ModelAdmin):
    list_display = ['title', ]
    filter_horizontal = ('learningExpos', 'category', 'prompts')


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
    list_display = ['question', 'questionCategory', 'learningObjective']


@admin.register(FakeCompetency)
class FakeCompAdmin(admin.ModelAdmin):
    list_display = ['name']
    filter_horizontal = ['fakeLos', ]


@admin.register(DesignJournal)
class DesignJournalAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(DjPage)
class DjPageAdmin(admin.ModelAdmin):
    list_display = ['designJournal', 'date', 'index', 'content']


@admin.register(DjPrompt)
class DjPromptAdmin(admin.ModelAdmin):
    list_display = ['prompt']
