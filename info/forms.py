from django import forms
from django.forms import modelformset_factory, BaseModelFormSet, ModelForm
from .models import DiscussionBoard, DiscussionTopic


class AddTopicForm(forms.ModelForm):

    class Meta:
        model = DiscussionTopic
        fields = ['title', 'description', 'creator', 'board']
        widgets = {'creator': forms.HiddenInput(), 'board': forms.HiddenInput()}
