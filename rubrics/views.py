from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from .models import Challenge, UserSolution, Rubric, RubricLine, LearningObjective, Criterion, CriteriaLine, Competency
from .forms import UserFileForm, RubricLineForm, RubricLineFormset, RubricForm, RubricFormSet, CriterionFormSet, CriteriaForm
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.forms import modelformset_factory
from django.contrib import messages
from django.shortcuts import redirect


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
        profile = self.request.user.profile
        # groupName = self.request.user.groups('name')
        if profile.role == 4:
            queryset = UserSolution.objects.all()
            return queryset

        if profile.role == 2:

            queryset = UserSolution.objects.filter()
            return queryset

        else:
            queryset = UserSolution.objects.filter(userOwner=self.request.user)
            return queryset

    context_object_name = 'solutions'
    template_name = 'rubrics/solution_list.html'


class RubricFinalFormView(FormView):
    template_name = 'rubrics/rubricFinalForm.html'
    model = UserSolution
    form_class = RubricFormSet
    success_url = '/evals'

    def get_context_data(self, **kwargs):
        context = super(RubricFinalFormView, self).get_context_data(**kwargs)
        rubric = self.kwargs['pk']
        context['evaluation'] = RubricLine.objects.all().filter(student=rubric)
        completionLevelObj = RubricLine.objects.all().filter(student=rubric)
        fart = 0
        for object in completionLevelObj:
            fart += int(object.completionLevel)
        context['usersolution'] = UserSolution.objects.get(id=rubric)
        userSolution = UserSolution.objects.get(id=rubric)
        challenge = userSolution.challengeName

        if Rubric.objects.all().filter(userSolution=userSolution).exists():
            RubricFormSet = modelformset_factory(Rubric, extra=0,  formset=RubricForm, fields=('userSolution', 'challenge', 'evaluator',
                                                                                               'generalFeedback', 'challengeCompletionLevel', ),
                                                 widgets={'userSolution': forms.HiddenInput, 'challenge': forms.HiddenInput, 'evaluator': forms.HiddenInput})

            formset = RubricFormSet(queryset=Rubric.objects.all().filter(userSolution=userSolution), )

        else:
            RubricFormSet = modelformset_factory(Rubric, extra=1, formset=RubricForm, fields=('userSolution', 'challenge', 'evaluator',
                                                                                              'generalFeedback', 'challengeCompletionLevel'),
                                                 widgets={'userSolution': forms.HiddenInput,
                                                         'challenge': forms.HiddenInput, 'evaluator': forms.HiddenInput})

            formset = RubricFormSet(initial=[{'userSolution': userSolution, 'challenge': challenge,
                                                 'evaluator': self.request.user, 'challengeCompletionLevel': fart}], queryset=Rubric.objects.none(),)

        context['form'] = formset
        return context

    def post(self, request, *args, **kwargs):
        form = RubricFormSet(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/evals')
        else:
            messages.error(request, "Error")
            return self.render_to_response(self.get_context_data(formset=form))

        # creating form that comes after RubricFormView/formsets
        # holds general feedback, and challenge completion level.
        # show slider on formset view for challenge completion level but store in permanently
        # on this page.


class RubricFormView(FormView):
    template_name = 'rubrics/rubric_form.html'
    model = UserSolution
    form_class = RubricLineFormset

    def get_context_data(self, **kwargs):
        context = super(RubricFormView, self).get_context_data(**kwargs)
        usersolution = self.kwargs['pk']
        challenge = UserSolution.objects.get(pk=usersolution).challengeName
        context['lo_list'] = LearningObjective.objects.filter(challenge=challenge)
        lo_list = LearningObjective.objects.filter(challenge=challenge)
        student = UserSolution.objects.get(pk=usersolution)
        context['student'] = student
        context['challenge'] = challenge
        loCount = LearningObjective.objects.filter(challenge=challenge).count()
        context['userRole'] = self.request.user.profile.role
        criteriaList = Criterion.objects.all()

        # edit view, checks for rubricLine objects from this userSolution
        # and sets the formset query to that instance
        context['criteria'] = criteriaList

        if RubricLine.objects.all().filter(student=usersolution).exists():
            RubricLineFormset = modelformset_factory(RubricLine, formset=RubricLineForm, extra=0, fields=(
                'learningObjective', 'evidencePresent', 'evidenceMissing', 'feedback', 'suggestions', 'completionLevel',
                'student', ), widgets={'student': forms.HiddenInput, })

            formset = RubricLineFormset(queryset=RubricLine.objects.all().filter(student=usersolution))

        # create new rubric, checked for rubricline objects from this userSolution
        # and none existed, so queryset is none and extra forms is set to LO count

        else:
            RubricLineFormset = modelformset_factory(RubricLine, formset=RubricLineForm, extra=loCount, fields=(
                'learningObjective', 'evidencePresent', 'evidenceMissing', 'feedback', 'suggestions', 'completionLevel',
                'student', ), widgets={'student': forms.HiddenInput, })

            formset = RubricLineFormset(
                initial=[{'learningObjective': learningObjective.pk, 'student': student} for learningObjective in
                         lo_list], queryset=RubricLine.objects.none())

        context['formset'] = formset
        return context

    def post(self, request, *args, **kwargs):
        formset = RubricLineFormset(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('solution-end-eval', self.kwargs['pk'])

        else:
            messages.error(request, "Error")
            return self.render_to_response(self.get_context_data(formset=formset))

    def form_valid(self, formset):
        formset.save()

    def form_invalid(self, formset):
        return self.render_to_response(self.get_context_data(formset=formset))


class EvalListView(ListView):

    def get_queryset(self, **kwargs):
        if self.request.user.is_staff:
            queryset = UserSolution.objects.all()
            return queryset
        else:
            queryset = UserSolution.objects.filter(userOwner=self.request.user)
            return queryset

    context_object_name = 'evals'
    template_name = "rubrics/eval_list.html"


class EvalDetailView(DetailView):
    model = UserSolution
    template_name = "rubrics/evalDetail.html"

    def get_context_data(self, **kwargs):
        context = super(EvalDetailView, self).get_context_data(**kwargs)
        rubric = self.kwargs['pk']
        student = UserSolution.objects.get(pk=rubric)
        context['evaluation'] = RubricLine.objects.all().filter(student=rubric)
        context['evalFinalForm'] = Rubric.objects.get(userSolution=rubric)
        context['userRole'] = self.request.user.profile.role
        return context


def success(request, pk):
    return render(request, 'rubrics/success.html', )


class CompetencyView(ListView):
    model = Competency
    template_name = "rubrics/compList.html"

    def get_queryset(self, **kwargs):
        queryset = Competency.objects.all()
        return queryset
    context_object_name = 'comps'



