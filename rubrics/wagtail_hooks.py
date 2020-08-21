from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from.models import Challenge, LearningExperience, SolutionInstance


class LearningExpAdmin(ModelAdmin):
    model = LearningExperience
    list_display = ['name', 'challenge', 'learningObjectives']
    list_filter = ['challenge', ]
    filter_horizontal = ('learningObjectives',)
    menu_icon = 'pick'
    menu_label = 'Learning Experiences'
    menu_order = 1
    add_to_settings_menu = False
    exclude_from_explorer = False


modeladmin_register(LearningExpAdmin)
