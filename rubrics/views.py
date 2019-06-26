from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from .models import Challenge, UserSolution, Rubric, RubricLine, LearningObjective, Criterion, CriteriaLine, \
    Competency, CompetencyProgress, ChallengeAddendum, LearningExperience, LearningExpoResponses
from .forms import UserFileForm, UserFileFormset, RubricLineForm, RubricLineFormset, RubricForm, RubricFormSet, \
    CriterionFormSet, CriteriaForm, CurrentStudentToView, RubricAddendumForm, RubricAddendumFormset, \
    LearningExperienceFormset, LearningExperienceForm, LearningExpoFeedbackForm, LearningExpoFeedbackFormset
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.forms import modelformset_factory
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .functions import process_rubricLine, assess_competency_done, custom_rubric_producer


class ChallengeCover(DetailView):
    template_name = 'rubrics/challenge_cover.html'
    model = Challenge

    def get_context_data(self, **kwargs):
        context = super(ChallengeCover, self).get_context_data(**kwargs)

        challengeCover = Challenge.objects.get(pk=self.kwargs['pk'])
        context['challengeCover'] = challengeCover

        learningObjectives = LearningObjective.objects.all().filter(challenge=self.kwargs['pk']).order_by('compGroup', 'compNumber', 'loNumber')
        context['learningObjectives'] = learningObjectives

        theseComps = []
        competencies = Competency.objects.all()
        for learningObjective in learningObjectives:
            for competency in competencies:
                if competency.compGroup == learningObjective.compGroup and competency.compNumber == learningObjective.compNumber:
                    if competency not in theseComps:
                        theseComps.append(competency)
        context['competencies'] = theseComps

        degree = challengeCover.degree
        context['degree'] = degree

        scale = challengeCover.scale
        context['scale'] = scale

        type = challengeCover.type
        context['type'] = type

        return context


class ChallengeDetail(FormView):
    template_name = 'rubrics/challenge_detail.html'
    model = Challenge
    form_class = UserFileFormset

    def get_context_data(self, **kwargs):
        context = super(ChallengeDetail, self).get_context_data(**kwargs)
        context['rubric_list'] = Challenge.objects.all()
        context['learningObjectives_list'] = LearningObjective.objects.all().filter(challenge=self.kwargs['pk'])
        existingSolutions = UserSolution.objects.all().filter(challengeName=self.kwargs['pk'])
        theseLearningExpos = LearningExperience.objects.all().filter(challenge=self.kwargs['pk'])
        thisChallenge = Challenge.objects.get(pk=self.kwargs['pk'])

        if existingSolutions.filter(userOwner=self.request.user).exists():
            thisSolution = existingSolutions.get(userOwner=self.request.user).id

            UserFileFormSet = modelformset_factory(UserSolution, extra=0, formset=UserFileForm, fields=('userOwner', 'challengeName', 'solution',
            'goodTitle', 'workFit', 'proudDetail', 'hardDetail', 'objectiveWell', 'objectivePoor', 'personalLearningObjective', 'helpfulLearningExp',
            'notHelpfulLearningExp', 'changeLearningExp', 'notIncludedLearningExp'),
            widgets={'userOwner': forms.HiddenInput, 'challengeName': forms.HiddenInput, })

            formset = UserFileFormSet(prefix='user', queryset=UserSolution.objects.all().filter(id=thisSolution), )

            LearningExpoFeedbackFormset = modelformset_factory(LearningExpoResponses, extra=0, formset=LearningExpoFeedbackForm,
                   fields=('learningExperienceResponse', 'learningExperience', 'user'), widgets={'user': forms.HiddenInput})

            feedbackFormset = LearningExpoFeedbackFormset(prefix='expo', queryset=LearningExpoResponses.objects.all().filter(
                user=self.request.user, learningExperience__challenge=thisChallenge))

        else:
            UserFileFormset = modelformset_factory(UserSolution, extra=1, formset=UserFileForm, fields=('userOwner', 'challengeName', 'solution',
            'goodTitle', 'workFit', 'proudDetail', 'hardDetail', 'objectiveWell', 'objectivePoor', 'personalLearningObjective', 'helpfulLearningExp',
            'notHelpfulLearningExp', 'changeLearningExp', 'notIncludedLearningExp'),
                                       widgets={'userOwner': forms.HiddenInput, 'challengeName': forms.HiddenInput})

            formset = UserFileFormset(prefix='user', initial=[{'challengeName': thisChallenge, 'userOwner': self.request.user}],
                                      queryset=UserSolution.objects.none())

            LearningExpoFeedbackFormset = modelformset_factory(LearningExpoResponses, extra=theseLearningExpos.count(),
                formset=LearningExpoFeedbackForm, fields=('learningExperienceResponse', 'learningExperience', 'user'),
                    widgets={'user': forms.HiddenInput})

            feedbackFormset = LearningExpoFeedbackFormset(prefix='expo', initial=[{'learningExperience': learningExperience, 'user': self.request.user}
                for learningExperience in theseLearningExpos], queryset=LearningExpoResponses.objects.none())

        context['form'] = formset
        context['feedbackForm'] = feedbackFormset
        context['challenge'] = thisChallenge
        return context

    def post(self, request, *args, **kwargs):
        # self.object = self.get_object()
        form = UserFileFormset(request.POST, prefix='user')
        expoForm = LearningExpoFeedbackFormset(request.POST, prefix='expo')
        if form.is_valid() and expoForm.is_valid():
            form.save()
            expoForm.save()
            return redirect('success', self.kwargs['pk'])
        else:
            messages.error(request, "Error")
            print(messages.error(request, "Error"))
            print("Form invalid")
            return self.render_to_response(self.get_context_data(formset=form))

    def form_valid(self, formset):
        formset.save()

    def form_invalid(self, form):
        print("Error")


class SolutionDetailView(DetailView):
    template_name = 'rubrics/solution_detail.html'
    model = UserSolution

    def get_context_data(self, **kwargs):
        context = super(SolutionDetailView, self).get_context_data(**kwargs)
        context['solution_list'] = UserSolution.objects.all()
        return context

        # Should pre-eval information go here?


class PreEvaluationUpdate(ListView):
    model = UserSolution
    template_name = "rubrics/pre_evaluation.html"
    # put the information page needed to properly evaluate a solution with a TC


class ChallengeListView(ListView):
    model = Challenge
    queryset = Challenge.objects.all()
    context_object_name = 'challenges'
    template_name = 'rubrics/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lo_list'] = LearningObjective.objects.all().order_by('compGroup', 'compNumber', 'loNumber')
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
        incrementor = 0
        for object in completionLevelObj:
            incrementor += int(object.completionLevel)
        context['usersolution'] = UserSolution.objects.get(id=rubric)
        userSolution = UserSolution.objects.get(id=rubric)
        challenge = userSolution.challengeName

        if Rubric.objects.all().filter(userSolution=userSolution).exists():
            RubricFormSet = modelformset_factory(Rubric, extra=0, formset=RubricForm, fields=(
            'userSolution', 'challenge', 'evaluator', 'generalFeedback', 'challengeCompletionLevel',),
             widgets={'userSolution': forms.HiddenInput, 'challenge': forms.HiddenInput, 'evaluator': forms.HiddenInput})

            formset = RubricFormSet(queryset=Rubric.objects.all().filter(userSolution=userSolution))

        else:
            RubricFormSet = modelformset_factory(Rubric, extra=1, formset=RubricForm, fields=(
            'challenge', 'challenge', 'evaluator', 'generalFeedback', 'challengeCompletionLevel'),
             widgets={'userSolution': forms.HiddenInput, 'challenge': forms.HiddenInput, 'evaluator': forms.HiddenInput})

            formset = RubricFormSet(initial=[{'userSolution': userSolution, 'challenge': challenge,
             'evaluator': self.request.user, 'challengeCompletionLevel': incrementor}], queryset=Rubric.objects.none())

        context['form'] = formset
        return context

    def post(self, request, *args, **kwargs):
        form = RubricFormSet(request.POST)
        completionLevelObj = RubricLine.objects.all().filter(student=self.kwargs['pk'])

        if form.is_valid():
            form.save()
            process_rubricLine(completionLevelObj)
            assess_competency_done(completionLevelObj)
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
        lo_list = LearningObjective.objects.filter(challenge=challenge).order_by('compGroup', 'compNumber', 'loNumber')
        thisUserSolution = UserSolution.objects.get(pk=usersolution)
        context['student'] = thisUserSolution
        context['challenge'] = challenge
        loCount = LearningObjective.objects.filter(challenge=challenge).count()

        context['userRole'] = self.request.user.profile.role
        criteriaList = Criterion.objects.all()

        # The idea: Run through the list of learning objectives attached to this challenge and add criterion
        # to contextual list if they match one of the learning objectives.
        neededCriteria = []
        for criterion in criteriaList:
            for learningObjective in lo_list:
                if (criterion.learningObj.id == learningObjective.id and criterion.learningObj.id not in criteriaList):
                    neededCriteria.append(criterion)

        criteriaLength = len(neededCriteria)

        # edit view, checks for rubricLine objects from this challenge
        # and sets the formset query to that instance
        context['criteria'] = neededCriteria
        context['count'] = criteriaLength

        if RubricLine.objects.all().filter(student=usersolution).exists():
            RubricLineFormset = modelformset_factory(RubricLine, formset=RubricLineForm, extra=0, fields=(
                'ignore', 'learningObjective', 'evidencePresent', 'evidenceMissing', 'feedback', 'suggestions', 'completionLevel',
                'student', 'needsLaterAttention', ), widgets={'student': forms.HiddenInput, })

            formset = RubricLineFormset(prefix='rubriclines', queryset=RubricLine.objects.all().filter(student=usersolution).order_by(
                'learningObjective__compGroup', 'learningObjective__compNumber', 'learningObjective__loNumber'))

            CriterionFormSet = modelformset_factory(CriteriaLine, formset=CriteriaForm, extra=0, fields=(
                'achievement', 'criteria', 'userSolution',), widgets={'criteria': forms.HiddenInput, 'userSolution': forms.HiddenInput})

            critFormset = CriterionFormSet(prefix='criteria', queryset=CriteriaLine.objects.all().filter(userSolution=thisUserSolution))

        # if challenge has been flagged for customization
        # reroute it to this function to apply the corrected learning
        # objectives and return it to the view
        elif thisUserSolution.customized is True:
            challenge = ChallengeAddendum.objects.get(userSolution=thisUserSolution)
            lo_list = LearningObjective.objects.filter(challengeaddendum=challenge).order_by('compGroup', 'compNumber', 'loNumber',)
            loCount = lo_list.count()
            RubricLineFormset = modelformset_factory(RubricLine, formset=RubricLineForm, extra=loCount, fields=(
                'ignore', 'learningObjective', 'evidencePresent', 'evidenceMissing', 'feedback', 'suggestions',
                'completionLevel', 'student', 'needsLaterAttention',), widgets={'student': forms.HiddenInput, })

            formset = RubricLineFormset(prefix='rubriclines',
                                        initial=[{'learningObjective': learningObjective.pk, 'student': thisUserSolution} for learningObjective in lo_list], queryset=RubricLine.objects.none())

            CriterionFormSet = modelformset_factory(CriteriaLine, formset=CriteriaForm, extra=criteriaLength, fields=(
                'achievement', 'criteria', 'userSolution',), widgets={'criteria': forms.HiddenInput,
                                                                   'userSolution': forms.HiddenInput})

            critFormset = CriterionFormSet(prefix='criteria',
                                           initial=[{'userSolution': thisUserSolution, 'criteria': criterion} for
                                                    criterion in neededCriteria], queryset=CriteriaLine.objects.none())
            # custom_rubric_producer(ChallengeAddendum.objects.get(challenge=thisUserSolution))

        # create new rubric, checked for rubricline objects from this challenge
        # and none existed, so queryset is none and extra forms is set to LO count

        else:
            RubricLineFormset = modelformset_factory(RubricLine, formset=RubricLineForm, extra=loCount, fields=(
                'ignore', 'learningObjective', 'evidencePresent', 'evidenceMissing', 'feedback', 'suggestions', 'completionLevel',
                'student', 'needsLaterAttention', ), widgets={'student': forms.HiddenInput, })

            formset = RubricLineFormset(prefix='rubriclines',
                initial=[{'learningObjective': learningObjective.pk, 'student': thisUserSolution} for learningObjective in
                         lo_list], queryset=RubricLine.objects.none())

            CriterionFormSet = modelformset_factory(CriteriaLine, formset=CriteriaForm, extra=criteriaLength, fields=(
                'achievement', 'criteria', 'userSolution', ), widgets={'criteria': forms.HiddenInput, 'userSolution': forms.HiddenInput})

            critFormset = CriterionFormSet(prefix='criteria',
                                           initial=[{'userSolution': thisUserSolution, 'criteria': criterion} for criterion in neededCriteria],
                                           queryset=CriteriaLine.objects.none())

        context['formset'] = formset
        context['critFormset'] = critFormset
        return context

    def post(self, request, *args, **kwargs):
        formset = RubricLineFormset(request.POST, prefix='rubriclines')
        critFormset = CriterionFormSet(request.POST, prefix='criteria')
        if formset.is_valid() and critFormset.is_valid():
            formset.save()
            critFormset.save()
            return redirect('solution-end-eval', self.kwargs['pk'])

        else:
            messages.error(request, "Error")
            return self.render_to_response(self.get_context_data(formset=formset))

    def form_valid(self, formset):
        formset.save()

    def form_invalid(self, form):
        print("Error")


class LearningExperienceView(DetailView):
    template_name = 'rubrics/learningExperience.html'
    model = LearningExperience

    def get_context_data(self, **kwargs):
        context = super(LearningExperienceView, self).get_context_data(**kwargs)
        learningExpo = LearningExperience.objects.get(pk=self.kwargs['pk'])
        context['learningExpo'] = learningExpo
        return context


class LearningExperienceCreator(FormView):
    template_name = 'rubrics/learningExperienceCreator.html'
    model = LearningExperience
    form_class = LearningExperienceFormset
    # success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(LearningExperienceCreator, self).get_context_data(**kwargs)
        LearningExperienceFormset = modelformset_factory(LearningExperience, formset=LearningExperienceForm, extra=1,
            fields=('name', 'challenge', 'learningObjectives', 'description', 'tags'))
        learningExpoformset = LearningExperienceFormset(queryset=LearningExperience.objects.none())
        context['form'] = learningExpoformset
        return context

    def post(self, request, *args, **kwargs):
        formset = LearningExperienceFormset(request.POST)

        if formset.is_valid():
            formset.save()
            return redirect('learningExperience', self.kwargs['pk'])
        else:
            return self.render_to_response(self.get_context_data(formset=formset))


class RubricAddendum(FormView):
    template_name = 'rubrics/rubric_addendum.html'
    model = UserSolution
    form_class = RubricAddendumFormset

    def get_context_data(self, **kwargs):
        context = super(RubricAddendum, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        solution = UserSolution.objects.get(pk=pk)
        challenge = UserSolution.objects.get(pk=pk).challengeName
        lo_list = LearningObjective.objects.filter(challenge=challenge)

        if ChallengeAddendum.objects.all().filter(userSolution=solution).exists():
            RubricAddendumFormset = modelformset_factory(ChallengeAddendum, formset=RubricAddendumForm, extra=0,
                                                         fields=('name', 'note', 'parentChallenge', 'learningObjs', 'group',
                                                                 'userSolution'))
            challengeAddendumForm = RubricAddendumFormset(queryset=
                                                          ChallengeAddendum.objects.all().filter(userSolution=solution))

        else:
            RubricAddendumFormset = modelformset_factory(ChallengeAddendum, formset=RubricAddendumForm, extra=1, fields=('name', 'note', 'parentChallenge', 'learningObjs', 'group',
                                                                                                                         'userSolution'))
            challengeAddendumForm = RubricAddendumFormset(initial=[{'learningObjs': learningObjective.pk, 'parentChallenge': challenge, 'userSolution': solution}
                                                                   for learningObjective in lo_list], queryset=ChallengeAddendum.objects.none())

        context['challengeAddendumForm'] = challengeAddendumForm
        return context

    def post(self, request, *args, **kwargs):
        formset = RubricAddendumFormset(request.POST)
        solution = UserSolution.objects.get(pk=self.kwargs['pk'])
        solution.customized = True
        if formset.is_valid():
            formset.save()
            solution.save()
            return redirect('solution-eval', self.kwargs['pk'])
        else:
            return self.render_to_response(self.get_context_data(formset=formset))


class EvalListView(ListView):

    def get_queryset(self, **kwargs):
        profile = self.request.user.profile
        if profile.role == 4:
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


class CompetencyView(ListView, FormMixin):
    model = Competency
    template_name = "rubrics/compList.html"
    form_class = CurrentStudentToView

    def get_queryset(self, **kwargs):
        queryset = Competency.objects.all().order_by('compGroup', 'compNumber')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CompetencyView, self).get_context_data(**kwargs)
        learningObjs = LearningObjective.objects.all().order_by('compGroup', 'compNumber', 'loNumber')
        context['learningObjs'] = learningObjs

        if self.request.user.profile.role == 4:
            firstStudent = User.objects.order_by('last_name').filter()[:1].get()
            form = CurrentStudentToView(self.request.GET)
            context['chosenUserForm'] = form
            rubricLines = RubricLine.objects.all().filter(student__userOwner=firstStudent)
            context['assess_competency_done'] = CompetencyProgress.objects.all().filter(
                student=firstStudent)

            # Ping server to load RubricLines for chosen user
            # Will put this into an AJAX call eventually
            if form.is_valid():
                if RubricLine.objects.all().filter(student__userOwner=form.cleaned_data['chooseUser']).exists():
                    rubricLines = RubricLine.objects.all().filter(student__userOwner=form.cleaned_data['chooseUser'])
                    context['currentUser'] = form.cleaned_data['chooseUser']

                    # Function checks if conditions are met and returns true or false rubricLine.ready
                    # will add some more logic to check if competency is complete
                    context['assess_competency_done'] = CompetencyProgress.objects.all().filter(student=form.cleaned_data['chooseUser'])
                else:
                    print('no data')

            else:
                rubricLines = RubricLine.objects.all().filter(student__userOwner=firstStudent)
                context['currentUser'] = firstStudent

        else:
            rubricLines = RubricLine.objects.all().filter(student__userOwner=self.request.user)
            context['currentUser'] = self.request.user
            context['assess_competency_done'] = CompetencyProgress.objects.all().filter(student=self.request.user)

        context['rubricLines'] = rubricLines

        return context

    context_object_name = 'comps'



