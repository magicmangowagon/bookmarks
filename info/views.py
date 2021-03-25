from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView, DetailView, FormView
from .models import BaseInfo, DiscussionBoard, DiscussionTopic
from centralDispatch.models import StudioExpoChoice
from centralDispatch.forms import StudioExpoChoiceForm
from .forms import AddTopicForm
# Create your views here.


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
        context['info'] = info
        form = StudioExpoChoiceForm(baseInfo=info, initial={'user': self.request.user, 'session': info},)
        context['form'] = form
        return context


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