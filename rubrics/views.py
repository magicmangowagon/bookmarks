from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden
from .models import Challenge, UserSolution, Rubric, RubricLine, User, LearningObjective, Competency
from .forms import ChallengeForm, UserFileForm, RubricForm, RubricLineForm, RubricLineFormset
from django.views.generic import ListView, DetailView, FormView, CreateView
from django import forms
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.views import View
from django.forms import formset_factory


# Class based challenge view with functioning form.
# Currently using this. Need to revisit, probably not best practice.
class challenge_detail(DetailView, FormMixin):
    template_name = 'rubrics/challenge_detail.html'
    model = Challenge
    form_class = UserFileForm

    def get_success_url(self):
        return reverse('success', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(challenge_detail, self).get_context_data(**kwargs)
        context['rubric_list'] = Challenge.objects.all()
        context['learningObjectives_list'] = LearningObjective.objects.all().filter(challenge=self.kwargs['pk'])
        context['form'] = UserFileForm(initial={'challengeName': self.object, 'userOwner': self.request.user})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(challenge_detail, self).form_valid(form)


class SolutionDetailView(DetailView):
    template_name = 'rubrics/solution_detail.html'
    model = UserSolution

    def get_context_data(self, **kwargs):
        context = super(SolutionDetailView, self).get_context_data(**kwargs)
        context['solution_list'] = UserSolution.objects.all()
        return context


class ChallengeListView(ListView):
    model = Challenge
    queryset = Challenge.objects.all()
    context_object_name = 'challenges'
    template_name = 'rubrics/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lo_list'] = LearningObjective.objects.all()
        return context


class SolutionListView(ListView):

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = UserSolution.objects.all()
            return queryset
        else:
            queryset = UserSolution.objects.filter(userOwner=self.request.user)
            return queryset

    context_object_name = 'solutions'
    # paginate_by = 3
    template_name = 'rubrics/solution_list.html'


class RubricFormView(CreateView):
    template_name = 'rubrics/rubric_form.html'
    model = UserSolution
    form_class = RubricLineForm
    
    def get_context_data(self, **kwargs):
        context = super(RubricFormView, self).get_context_data(**kwargs)
        context['rubric_challenge'] = Challenge
        # seems like there is more code here than I need
        # capture current pk, then get the pk associated with it
        # then pass it to the filter
        usersolution = self.kwargs['pk']
        challenge = UserSolution.objects.get(pk=usersolution).challengeName
        context['lo_list'] = LearningObjective.objects.filter(challenge=challenge)
        student = UserSolution.objects.get(pk=usersolution).userOwner
        context['formset'] = RubricLineForm(initial={'student': student, 'learningObjective': LearningObjective})

        return context

    def post(self, request, *args, **kwargs):
        form = RubricLineForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)

    def form_valid(self, formset):
        formset.save()
        return HttpResponseRedirect('/')

    def form_invalid(self, formset):
        return self.render_to_response(self.get_context_data(formest=formset))


def success(request, pk):
    return render(request, 'rubrics/success.html', )


# function based view not being used, supplanted by Class based view above
def solution_submission(request, pk):
    submitted = False
    if request.method == "POST":
        form = UserFileForm(request.POST, request.FILES)
        if form.is_valid():
            usersolution = form.save(commit=False)
            try:
                usersolution.userOwner = request.user
                usersolution.challengeName = Challenge.pk
            except Exception:
                pass
            form.save()
            return HttpResponseRedirect('?submitted=True')
    else:
        form = UserFileForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'rubrics/solution_form.html', {'form': form, 'submitted': submitted})

