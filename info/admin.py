from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from .models import BaseInfo, InfoCategory, DiscussionBoard, DiscussionTopic, QuestionStub, FakeLO, FakeCompetency, \
    Prompts, CommentContainer, DesignJournal, DjPage, DjResponse, DjPrompt, LearningModulePage, LearningModulePrompt, \
    LearningModule, LearningModuleResponse, Message, LearningModulePageSection, PageOrderThrough, NewLearningObjective, LearningModulePromptInstructions
from rubrics.models import LearningExperience
from adminsortable2.admin import SortableInlineAdminMixin
# Register your models here.


class PageSectionInline(SortableInlineAdminMixin, admin.TabularInline):
    model = LearningModulePage.content.through
    exclude = ['learningObjectives', 'content']
    extra = 0


@admin.register(NewLearningObjective)
class NewLearningObjectiveAdmin(admin.ModelAdmin):
    model = NewLearningObjective
    filter_horizontal = ['criteria']


@admin.register(InfoCategory)
class CategoryAdmin(admin.ModelAdmin):
    model = InfoCategory


@admin.register(Prompts)
class PromptsAdmin(admin.ModelAdmin):
    model = Prompts
    list_display = ['question', 'response']


@admin.register(CommentContainer)
class CommentContainerAdmin(admin.ModelAdmin):
    list_display = ['comment', 'baseInfo', 'coordinates', 'highlight']


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


@admin.register(LearningModule)
class LearningModuleAdmin(admin.ModelAdmin):
    list_display = ['name']
    filter_horizontal = ['pages']


@admin.register(LearningModulePage)
class LearningModulePageAdmin(admin.ModelAdmin):
    list_display = ['name', 'pageNumber']
    filter_horizontal = ['content']


@admin.register(LearningModulePageSection)
class LearningModulePageSectionAdmin(admin.ModelAdmin):
    list_display = ['sectionContent']
    filter_horizontal = ['learningObjectives', 'prompts', 'promptInstructions']


@admin.register(LearningModulePromptInstructions)
class LearningModulePromptInstructionsAdmin(admin.ModelAdmin):
    list_display = ['instructions']


@admin.register(LearningModulePrompt)
class LearningModulePromptAdmin(admin.ModelAdmin):
    list_display = ['promptText']


@admin.register(LearningModuleResponse)
class LearningModuleResponseAdmin(admin.ModelAdmin):
    list_display = ['response']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['messageText', 'recipient']
