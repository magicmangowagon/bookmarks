from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView
from .models import BaseInfo
# Create your views here.


class BaseInfoList(ListView):
    model = BaseInfo
    queryset = BaseInfo.objects.all()
    context_object_name = 'baseInfoList'
    template_name = 'info/infolist.html'
