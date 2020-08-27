from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView
from .models import BaseInfo
from centralDispatch.models import StudioExpoChoice
from centralDispatch.forms import StudioExpoChoiceForm
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
