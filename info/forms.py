from django import forms
from django.forms import modelformset_factory, BaseModelFormSet, ModelForm
from .models import DiscussionBoard, DiscussionTopic, FakeLO, QuestionStub, CommentContainer, DesignJournal, DjPage, \
    DjPrompt, DjResponse


class AddDjResponseForm(forms.ModelForm):
    class Meta:
        model = DjResponse
        fields = ['designJournal', 'content', 'index', 'creator', 'prompt']


class AddDjPageForm(forms.ModelForm):
    class Meta:
        model = DjPage
        fields = ['designJournal', 'content', 'index', 'creator']
        widgets = {'designJournal': forms.HiddenInput(), 'index': forms.HiddenInput(), 'creator': forms.HiddenInput()}


class AddDjPromptForm(forms.ModelForm):
    class Meta:
        Model = DjPrompt
        fields = ['prompt', 'creator']


class AddTopicForm(forms.ModelForm):

    class Meta:
        model = DiscussionTopic
        fields = ['title', 'description', 'creator', 'board']
        widgets = {'creator': forms.HiddenInput(), 'board': forms.HiddenInput()}


class AddComment(forms.ModelForm):
    # lo = forms.ModelChoiceField(queryset=QuestionStub.objects.none(), empty_label=None)

    class Meta:
        model = QuestionStub
        fields = ['learningObjective', 'question', 'questionCategory']

    # def __init__(self):
    #     super(AddComment, self).__init__()


class CommentContainerForm(forms.ModelForm):

    class Meta:
        model = CommentContainer
        fields = ['comment', 'baseInfo', 'coordinates']
        widgets = {'baseInfo': forms.HiddenInput(), 'coordinates': forms.HiddenInput(), }
