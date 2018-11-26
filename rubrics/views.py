from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden
from .models import Challenge, UserSolution
from .forms import ChallengeForm
from django.views.generic import ListView, DetailView, FormView
from django import forms
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.views import View


class UserFileForm(forms.ModelForm):
    class Meta:
        model = UserSolution
        fields = ('file', )


class ChallengeDisplay(DetailView):
    model = Challenge

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserFileForm()
        return context


class challenge_detail(DetailView):
    model = Challenge

    def get_context_data(self, **kwargs):
        context = super(challenge_detail, self).get_context_data(**kwargs)
        context['rubric_list'] = Challenge.objects.all()
        context['form'] = SolutionForm()
        return context


class SolutionUploadForm(SingleObjectMixin, FormView):
    template_name = 'rubrics/challenge_detail.html'
    form_class = UserFileForm
    model = Challenge

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('challenge-detail', kwargs={'pk': self.object.pk})


class ChallengeDetail(View):

    def get(self, request, *args, **kwargs):
        view = ChallengeDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self,request, *args, **kwargs):
        view = SolutionUploadForm.as_view()
        return view(request, *args, **kwargs)


class SolutionForm(forms.Form):
    file = forms.FileField()
    form_class = UserFileForm


class ChallengeListView(ListView):
    queryset = Challenge.objects.all()
    context_object_name = 'challenges'
    # paginate_by = 3
    template_name = 'rubrics/list.html'


def solution_submission(request, pk):
    submitted = False
    if request.method == "POST":
        form = UserFileForm(request.POST, request.FILES)
        if form.is_valid():
            usersolution = form.save(commit=False)
            try:
                usersolution.userOwner = request.user
                usersolution.challengeName = pk
            except Exception:
                pass
            form.save()
            return HttpResponseRedirect('?submitted=True')
    else:
        form = UserFileForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'rubrics/solution_form.html', {'form': form, 'submitted': submitted})
