from django.contrib.auth.models import User
from rest_framework import serializers
from .models import LearningModulePage, LearningModulePageSection, LearningModuleResponse, LearningModule, LearningModulePrompt, NewLearningObjective


class CaseStudyPromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningModuleResponse
        fields = ['question', 'response', 'creator', 'dateCreated']
