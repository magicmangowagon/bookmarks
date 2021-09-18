from django import forms
from django.forms import modelformset_factory, BaseModelFormSet, ModelForm
from .models import DiscussionBoard, DiscussionTopic, FakeLO, QuestionStub


class AddTopicForm(forms.ModelForm):

    class Meta:
        model = DiscussionTopic
        fields = ['title', 'description', 'creator', 'board']
        widgets = {'creator': forms.HiddenInput(), 'board': forms.HiddenInput()}


class AddComment(forms.ModelForm):
    lo = forms.ModelChoiceField(queryset=QuestionStub.objects.none(), empty_label=None)

    class Meta:
        model = FakeLO
        fields = ['lo', ]

    # def __init__(self):
    #     super(AddComment, self).__init__()
