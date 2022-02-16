from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView, DetailView, FormView
from django.forms import modelformset_factory
from django import forms
from django.core.paginator import Paginator
from .models import BaseInfo, DiscussionBoard, DiscussionTopic, FakeLO, QuestionStub, FakeCompetency, CommentContainer,\
    DesignJournal, DjPage, DjResponse, DjPrompt, DesignJournalContent, LearningModule, LearningModulePage, \
    LearningModulePrompt, LearningModuleResponse, Message
from centralDispatch.models import StudioExpoChoice
from centralDispatch.forms import StudioExpoChoiceForm
from rubrics.models import Competency, LearningObjective
from .forms import AddTopicForm, AddComment, CommentContainerForm, AddDjPageForm, AddDjPromptForm, AddDjResponseForm, \
    LearningModuleResponseForm, LMResponseFormset, MessageForm
import json
# Create your views here.


class LearningModuleListView(ListView):
    context_object_name = 'learningModulePages'
    template_name = 'info/learning_module_list.html'
    model = LearningModule
    paginate_by = 1

    def get_queryset(self, **kwargs):
        currentLM = LearningModule.objects.get(pk=self.kwargs['pk'])
        return currentLM.pages.all().order_by('pageNumber')


class LearningModuleView(DetailView):
    model = LearningModulePage
    template_name = 'info/learning_module.html'

    def get_context_data(self, **kwargs):
        context = super(LearningModuleView, self).get_context_data()
        currentPage = LearningModulePage.objects.get(pk=self.kwargs['pk'])
        learningModule = currentPage.learningmodule_set.first()

        pages = learningModule.pages.all().order_by('pageNumber')
        conversations = Message.objects.filter(pageLocation__in=pages)
        context['conversations'] = conversations
        questions = currentPage.prompt.all()
        LMResponseFormset = modelformset_factory(LearningModuleResponse, extra=len(questions), formset=LearningModuleResponseForm,
                                                 fields=['creator', 'question', 'response'], widgets={'creator': forms.HiddenInput})
        responseForm = LMResponseFormset(prefix='responseForm', initial=[{'question': question, 'creator': self.request.user} for question in questions],
                                         queryset=LearningModuleResponse.objects.none())
        context['responseForm'] = responseForm
        messageCoach = MessageForm(initial={'creator': self.request.user, 'recipient': self.request.user})
        context['messageCoach'] = messageCoach
        context['pages'] = pages
        context['learningModule'] = learningModule
        return context

    def post(self, request, *args, **kwargs):
        if request.POST:
            print('inside POST')
            if request.POST.get("msgForm"):
                newMsg = MessageForm(request.POST)
                print('inside msg form')
                if newMsg.is_valid():
                    newMsg.save()
                    # LearningModule.objects.get(pk=self.kwargs['pk'])
                    return redirect('learning-module', pk=self.kwargs.get('pk'))
            if request.POST.get("promptResponse"):
                promptResponse = LearningModuleResponseForm(request.POST)

                if promptResponse.is_valid():
                    promptResponse.save()

                    return redirect('learning-module', pk=self.kwargs.get('pk'))
        else:
            return redirect('learning-module', pk=self.kwargs['pk'])


class BaseInfoList(ListView):
    model = BaseInfo
    queryset = BaseInfo.objects.all().order_by('occurrenceDate')
    context_object_name = 'baseInfoList'
    template_name = 'info/infolist.html'


class BaseInfoDetail(DetailView):
    model = BaseInfo
    template_name = 'info/infodetail.html'

    def get_context_data(self, **kwargs):
        context = super(BaseInfoDetail, self).get_context_data(**kwargs)
        info = BaseInfo.objects.get(id=self.kwargs['pk'])
        comps = Competency.objects.all().filter(archive=False)
        category = []
        tree = []
        existingComments = CommentContainer.objects.filter(baseInfo=self.kwargs['pk'])
        context['existingComments'] = existingComments
        questionStubForm = AddComment
        for comp in comps:
            c = {
                'name': comp.name,
                'children': []
            }
            for lo in comp.learningObjs.all():
                l = {
                    'name': lo.name,
                    'children': []
                }
                stubs = QuestionStub.objects.filter(learningObjective=lo)
                for q in stubs:
                    qS = {
                        'category': q.questionCategory,
                        'questionText': q.question,
                        'id': q.id
                    }
                    l['children'].append(qS)
                c['children'].append(l)
            tree.append(c)
        # print(tree)
            # tree.update(comp)
            # for lo in comp.get_los():
        containerForm = CommentContainerForm(initial={'baseInfo': self.kwargs['pk']})
        context['containerForm'] = containerForm
        context['qsForm'] = questionStubForm
        context['comps'] = comps
        context['info'] = info
        context['tree'] = json.dumps(tree)

        return context

    def post(self, request, *args, **kwargs):
        baseInfo = BaseInfo.objects.get(pk=self.kwargs['pk'])
        if request.POST:
            if request.POST.get("qStub"):
                newQStub = AddComment(request.POST)

                if newQStub.is_valid():
                    newQStub.save()
                    container = CommentContainer.objects.create(comment=newQStub.instance, baseInfo=
                    BaseInfo.objects.get(pk=self.kwargs['pk']))
                    return redirect('infodetail', pk=self.kwargs.get('pk'))
            if request.POST.get("container"):
                newQStub = CommentContainerForm(request.POST)

                if newQStub.is_valid():
                    newQStub.save()
                    #container = CommentContainer.objects.create(comment=newQStub.instance, baseInfo=
                    # BaseInfo.objects.get(pk=self.kwargs['pk']))
                    return redirect('infodetail', pk=self.kwargs.get('pk'))


class DiscussionBoardView(ListView):
    model = DiscussionBoard
    template_name = 'info/discussion.html'

    def get_queryset(self):
        queryset = DiscussionTopic.objects.all().filter(board=self.kwargs['pk']).order_by('creationDate')
        print(queryset.count())
        return queryset

    def get_context_data(self, **kwargs):
        context = super(DiscussionBoardView, self).get_context_data(**kwargs)
        board = DiscussionBoard.objects.get(id=self.kwargs['pk'])
        context['topics'] = DiscussionTopic.objects.all().filter(board=board)
        context['discussionBoard'] = board
        addTopic = AddTopicForm(initial={'creator': self.request.user, 'board': board}, )
        context['addTopic'] = addTopic
        return context

    def post(self, request, *args, **kwargs):
        if request.POST:
            addTopic = AddTopicForm(request.POST)
            if addTopic.is_valid():
                addTopic.save()
                return redirect('discussion-board', pk=self.kwargs.get('pk'))

            else:
                print(addTopic.errors)
                return redirect('discussion-board', pk=self.kwargs.get('pk'))


class DiscussionTopicView(DetailView):
    model = DiscussionTopic
    template_name = 'info/discussiontopic.html'


class DesignJournalView(DetailView):
    model = DesignJournal
    template_name = 'info/design_journal.html'

    def get_context_data(self, **kwargs):
        context = super(DesignJournalView, self).get_context_data(**kwargs)
        designJournal = DesignJournal.objects.get(pk=self.kwargs['pk'])
        djPages = DjPage.objects.filter(designJournal=self.kwargs['pk']).order_by('-date')
        djPageForm = AddDjPageForm(initial={'designJournal': self.kwargs['pk'], 'creator': self.request.user})
        # djResponseForm = AddDjResponseForm(initial={'designJournal': self.kwargs['pk'], 'creator': self.request.user})
        djPrompts = DjPrompt.objects.last()
        context['prompts'] = djPrompts
        context['addDjPage'] = djPageForm
        context['designJournal'] = designJournal
        context['pages'] = djPages
        return context

    def post(self, request, *args, **kwargs):
        djPage = AddDjPageForm(request.POST)

        if djPage.is_valid():
            djPage.save()
            return redirect('design-journal', pk=self.kwargs['pk'])

