from django.shortcuts import render, redirect, render_to_response
from datetime import date, datetime
from django import forms
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from .models import Challenge, UserSolution, Rubric, RubricLine, LearningObjective, Criterion, CriteriaLine, \
    Competency, CompetencyProgress, ChallengeAddendum, LearningExperience, LearningExpoResponses, Evaluated, \
    CoachReview, SolutionInstance, MegaChallenge, ChallengeResources, ChallengeResourcesFile
from .forms import UserFileForm, UserFileFormset, RubricLineForm, RubricLineFormset, RubricForm, RubricFormSet, \
    CriterionFormSet, CriteriaForm, CurrentStudentToView, RubricAddendumForm, RubricAddendumFormset, \
    LearningExperienceFormset, LearningExperienceForm, LearningExpoFeedbackForm, LearningExpoFeedbackFormset, \
    CoachReviewForm, CoachReviewFormset, UserSolutionToView
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.forms import modelformset_factory
from django.contrib import messages
from django.contrib.auth.models import User, Group
from .functions import process_rubricLine, assess_competency_done, custom_rubric_producer, mega_challenge_builder
from django.core.mail import send_mail
from .filters import EvalFilter


class ChallengeCover(DetailView):

    model = Challenge

    def get_context_data(self, **kwargs):
        context = super(ChallengeCover, self).get_context_data(**kwargs)

        challengeCover = Challenge.objects.get(pk=self.kwargs['pk'])

        if challengeCover.megaChallenge:
            challenges = Challenge.objects.all().filter(megaChallenge=challengeCover.megaChallenge)
            learningObjectives = []
            for challenge in challenges:
                lo_list = LearningObjective.objects.all().filter(challenge=challenge).order_by('compGroup', 'compNumber', 'loNumber')
                for learningObjective in lo_list:
                    if learningObjective not in learningObjectives:
                        learningObjectives.append(learningObjective)

            context['learningObjectives'] = learningObjectives
            context['challengeCover'] = Challenge.objects.all().filter(megaChallenge=challengeCover.megaChallenge)
        else:
            learningObjectives = LearningObjective.objects.all().filter(challenge=challengeCover).order_by('compGroup',
                                                                                                           'compNumber',
                                                                                                           'loNumber')
            context['learningObjectives'] = learningObjectives
            context['challengeCover'] = challengeCover

        context['criterionList'] = Criterion.objects.all().filter(learningObj__in=learningObjectives)
        theseComps = []
        competencies = Competency.objects.all()
        for learningObjective in learningObjectives:
            for competency in competencies:
                if competency.compGroup == learningObjective.compGroup and competency.compNumber == learningObjective.compNumber:
                    if competency not in theseComps:
                        theseComps.append(competency)
        context['competencies'] = theseComps

        try:
            relatedLearningExperiences = LearningExperience.objects.all().filter(challenge=challengeCover).order_by('index')
            context['next'] = relatedLearningExperiences.first().pk

        except:
            relatedLearningExperiences = 0
            context['next'] = relatedLearningExperiences

        return context

    def render_to_response(self, context, **response_kwargs):

        if self.request.user.is_staff or Challenge.objects.get(pk=self.kwargs['pk']).display:
            return render_to_response('rubrics/challenge_cover.html', context)
        else:
            return HttpResponseForbidden()


# Murphy Page was the first TC user
# July 12, 2019, they uploaded their solution for
# Caregiver Engagement. Now we have users, so we should
# probably fix this thing!
class ChallengeDetail(FormView):
    template_name = 'rubrics/challenge_detail.html'
    model = SolutionInstance
    form_class = UserFileFormset

    def get_context_data(self, **kwargs):
        context = super(ChallengeDetail, self).get_context_data(**kwargs)
        context['learningObjectives_list'] = LearningObjective.objects.all().filter(solutioninstance=self.kwargs['pk'])
        # print(SolutionInstance.objects.get(pk=self.kwargs['pk']).challenge_that_owns_me.first())
        thisChallenge = SolutionInstance.objects.get(pk=self.kwargs['pk']).challenge_that_owns_me.first()
        existingSolutions = UserSolution.objects.all().filter(challengeName=thisChallenge, userOwner=self.request.user)
        theseLearningExpos = LearningExperience.objects.all().filter(challenge=thisChallenge)
        thisSolutionInstance = SolutionInstance.objects.get(pk=self.kwargs['pk'])

        relatedLearningExperiences = LearningExperience.objects.all().filter(challenge=thisChallenge).order_by('index')
        print(relatedLearningExperiences.count())
        context['previous'] = relatedLearningExperiences.last().pk
        print(self.kwargs['pk'])

        if existingSolutions.filter(solutionInstance=thisSolutionInstance).exists():
            thisSolution = existingSolutions.get(solutionInstance=self.kwargs['pk'])

            UserFileFormSet = modelformset_factory(UserSolution, extra=0, formset=UserFileForm, fields=('userOwner', 'challengeName', 'solutionInstance', 'solution',
            'goodTitle', 'workFit', 'proudDetail', 'hardDetail', 'objectiveWell', 'objectivePoor', 'personalLearningObjective', 'helpfulLearningExp',
            'notHelpfulLearningExp', 'changeLearningExp', 'notIncludedLearningExp'),
            widgets={'userOwner': forms.HiddenInput, 'challengeName': forms.HiddenInput, 'solutionInstance': forms.HiddenInput })

            formset = UserFileFormSet(prefix='user', queryset=UserSolution.objects.all().filter(id=thisSolution.id), )

            LearningExpoFeedbackFormset = modelformset_factory(LearningExpoResponses, extra=0, formset=LearningExpoFeedbackForm,
                   fields=('learningExperienceResponse', 'learningExperience', 'user'), widgets={'user': forms.HiddenInput})

            feedbackFormset = LearningExpoFeedbackFormset(prefix='expo', queryset=LearningExpoResponses.objects.all().filter(
                user=self.request.user, learningExperience__challenge=thisChallenge))

        else:

            UserFileFormset = modelformset_factory(UserSolution, extra=1, formset=UserFileForm, fields=('userOwner', 'challengeName', 'solution', 'solutionInstance',
            'goodTitle', 'workFit', 'proudDetail', 'hardDetail', 'objectiveWell', 'objectivePoor', 'personalLearningObjective', 'helpfulLearningExp',
            'notHelpfulLearningExp', 'changeLearningExp', 'notIncludedLearningExp'),
                                       widgets={'userOwner': forms.HiddenInput, 'challengeName': forms.HiddenInput, 'solutionInstance': forms.HiddenInput})

            formset = UserFileFormset(prefix='user', initial=[{'challengeName': thisChallenge, 'userOwner': self.request.user, 'solutionInstance': thisSolutionInstance}],
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
        if request.method == 'POST':
            form = UserFileFormset(request.POST, prefix='user')
            expoForm = LearningExpoFeedbackFormset(request.POST, prefix='expo')

            if form.is_valid() and expoForm.is_valid():
                form.save()
                expoForm.save()
                try:
                    send_mail('New TC submission', str(self.request.user) + ' has submitted a challenge solution',
                              'noreply@wwgradschool.org', ['castle@woodrowacademy.org', ], fail_silently=False)
                except:
                    pass
                return redirect('success', self.kwargs['pk'])
            else:
                print(form.errors)
        else:
            form = UserFileFormset(prefix='user')
            expoForm = LearningExpoFeedbackFormset(prefix='expo')
        challenge = SolutionInstance.objects.get(pk=self.kwargs['pk']).challenge_that_owns_me.first()
        learningObjectives_list = LearningObjective.objects.all().filter(challenge=challenge)

        context = {'form': form, 'feedbackForm': expoForm, 'challenge': challenge, 'learningObjectives_list': learningObjectives_list}
        return render(request, self.get_template_names(), context)


class SolutionSectionView(DetailView):
    template_name = 'rubrics/solution_sections.html'
    model = Challenge
    # context_object_name = 'solutions'

    '''
    def get_queryset(self):
        queryset = SolutionInstance.objects.all().filter(challenge_that_owns_me=self.kwargs['pk'])
        return queryset
    '''

    def get_context_data(self, **kwargs):
        context = super(SolutionSectionView, self).get_context_data(**kwargs)
        challenge = Challenge.objects.get(id=self.kwargs['pk'])
        context['challenge'] = challenge
        context['lo_list'] = LearningObjective.objects.all().filter(challenge=challenge).order_by('compGroup', 'compNumber', 'loNumber')
        solutions = SolutionInstance.objects.all().filter(challenge_that_owns_me=challenge).order_by('order')

        # field_value = getattr(obj, field_name)
        for solution in solutions:
            print(getattr(solution, 'DESIGN'))
            context['degree'] = [(solution.DESIGN, 'Design', solution.name),
                                 (solution.SIMULATE, 'Simulate', solution.name),
                                 (solution.IMPLEMENT, 'Implement', solution.name)]
            context['scale'] = [(solution.ONEONONE, 'One on One', solution.name),
                                (solution.SMALLGROUP, 'Small Group', solution.name),
                                (solution.FULLCLASS, 'Full Class', solution.name)]
            context['type'] = [(solution.REFLECTION, 'Reflection', solution.name),
                               (solution.CLASSROOMEVIDENCE, 'Classroom Evidence', solution.name),
                               (solution.OBSERVATION, 'Observation', solution.name)]

        print(solutions.count())
        context['solutions'] = solutions
        return context


class SolutionDetailView(DetailView):
    template_name = 'rubrics/solution_detail.html'
    model = UserSolution

    def get_context_data(self, **kwargs):
        context = super(SolutionDetailView, self).get_context_data(**kwargs)
        context['solution_list'] = UserSolution.objects.all()
        thisSolution = UserSolution.objects.get(pk=self.kwargs['pk'])
        thisChallenge = thisSolution.challengeName

        theseles = LearningExperience.objects.all().filter(challenge=thisChallenge)
        print(theseles)
        theseLearningExpos = LearningExpoResponses.objects.all().filter(user=thisSolution.userOwner, learningExperience__in=theseles)
        context['theseLearningExpos'] = theseLearningExpos

        otherLOinstances = []
        theseLearningObjectives = LearningObjective.objects.all().filter(challenge=thisChallenge)
        usersRubricLines = RubricLine.objects.all().filter(student__userOwner=thisSolution.userOwner)

        for learningObjective in theseLearningObjectives:
            for rubricLine in usersRubricLines:
                if rubricLine.learningObjective == learningObjective and rubricLine.student != thisSolution:
                    otherLOinstances.append(rubricLine)

        context['otherInstances'] = otherLOinstances
        return context

        # Should pre-eval information go here?


class PreEvaluationUpdate(ListView):
    model = UserSolution
    template_name = "rubrics/pre_evaluation.html"
    # put the information page needed to properly evaluate a solution with a TC


class ChallengeListView(ListView):
    model = Challenge
    # queryset = Challenge.objects.all().filter(display=True).order_by('challengeGroupChoices')
    context_object_name = 'challenges'
    template_name = 'rubrics/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mega_lo'] = LearningObjective.objects.all().filter(challenge__megaChallenge__isnull=False).distinct().order_by('compGroup', 'compNumber', 'loNumber')
        context['megaChallenges'] = MegaChallenge.objects.all()
        return context

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Challenge.objects.all().order_by('challengeGroupChoices')
            return queryset
        else:
            queryset = Challenge.objects.all().filter(display=True).order_by('challengeGroupChoices')
            return queryset


class MegaSubPage(DetailView):
    model = MegaChallenge
    template_name = 'rubrics/sub_list.html'

    def get_context_data(self, **kwargs):
        context = super(MegaSubPage, self).get_context_data()
        challenges = Challenge.objects.all().filter(megaChallenge=self.kwargs['pk']).order_by('my_order')
        context['challenges'] = challenges
        learningExpos = []
        for challenge in challenges:
            learningExpos.append(LearningExperience.objects.all().filter(challenge=challenge).order_by('index').first())
        print(len(learningExpos))
        context['learningExpos'] = learningExpos
        return context


class SolutionListView(ListView):

    def get_queryset(self):
        profile = self.request.user.profile

        # groupName = self.request.user.groups('name')
        if profile.role == 4:
            queryset = UserSolution.objects.all()
            return queryset

        if profile.role == 3 or profile.role == 2:

            group = self.request.user.groups.all()
            print(group)
            queryset = UserSolution.objects.filter(userOwner__groups__in=group)
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

        if Rubric.objects.all().filter(userSolution=userSolution).filter(evaluator=self.request.user).exists():
            RubricFormSet = modelformset_factory(Rubric, extra=0, formset=RubricForm, fields=(
            'userSolution', 'challenge', 'evaluator', 'generalFeedback', 'challengeCompletionLevel',),
             widgets={'userSolution': forms.HiddenInput, 'challenge': forms.HiddenInput, 'evaluator': forms.HiddenInput,
                      'challengeCompletionLevel': forms.HiddenInput})

            formset = RubricFormSet(prefix='rFormset', queryset=Rubric.objects.all().filter(userSolution=userSolution).filter(evaluator=self.request.user).distinct())

        else:
            RubricFormSet = modelformset_factory(Rubric, extra=1, formset=RubricForm, fields=(
            'userSolution', 'challenge', 'evaluator', 'generalFeedback', 'challengeCompletionLevel'),
             widgets={'userSolution': forms.HiddenInput, 'challenge': forms.HiddenInput, 'evaluator': forms.HiddenInput,
                      'challengeCompletionLevel': forms.HiddenInput})

            formset = RubricFormSet(prefix='rFormset', initial=[{'userSolution': userSolution, 'challenge': challenge,
             'evaluator': self.request.user, 'challengeCompletionLevel': incrementor}], queryset=Rubric.objects.none())

        if self.request.user.profile.role is 3:
            if CoachReview.objects.filter(userSolution=userSolution).exists():
                CoachReviewFormset = modelformset_factory(CoachReview, formset=CoachReviewForm, extra=0, fields=(
                    'release', 'userSolution', 'comment'), widgets={'userSolution': forms.HiddenInput, 'comment': forms.HiddenInput})
                coachRevFormset = CoachReviewFormset(prefix='coachRevFormset', queryset=CoachReview.objects.filter(userSolution=userSolution))

            else:
                CoachReviewFormset = modelformset_factory(CoachReview, formset=CoachReviewForm, extra=1, fields=(
                    'release', 'userSolution', 'comment'), widgets={'userSolution': forms.HiddenInput, 'comment': forms.HiddenInput})
                coachRevFormset = CoachReviewFormset(prefix='coachRevFormset',
                                                     initial=[{'userSolution': userSolution}], queryset=CoachReview.objects.none())
            # context['formset'] = cFormset
            context['coachRevFormset'] = coachRevFormset

        context['form'] = formset
        return context

    def post(self, request, *args, **kwargs):
        form = RubricFormSet(request.POST, prefix='rFormset')
        completionLevelObj = RubricLine.objects.all().filter(student=self.kwargs['pk'])

        if self.request.user.profile.role is 3:
            coachForm = CoachReviewFormset(request.POST, prefix='coachRevFormset')

        if form.is_valid():
            form.save()
            if self.request.user.profile.role is 3:
                if coachForm.is_valid():
                    coachForm.save()
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
        thisUserSolution = UserSolution.objects.get(pk=usersolution)

        if thisUserSolution.customized:
            challenge = ChallengeAddendum.objects.get(userSolution=thisUserSolution)
            lo_list = LearningObjective.objects.filter(challengeaddendum=challenge).order_by('compGroup', 'compNumber',
                                                                                            'loNumber')
        else:
            challenge = UserSolution.objects.get(pk=usersolution).solutionInstance
            lo_list = LearningObjective.objects.filter(solutioninstance=challenge).order_by('compGroup', 'compNumber',
                                                                                            'loNumber')

        context['lo_list'] = lo_list
        context['student'] = thisUserSolution
        context['usersolution'] = thisUserSolution

        try:
            context['challenge'] = challenge.challenge_that_owns_me.all().first
        except:
            context['challenge'] = challenge

        context['solutionInstance'] = thisUserSolution.solutionInstance
        loCount = len(lo_list)

        context['userRole'] = self.request.user.profile.role

        # The idea: Run through the list of learning objectives attached to this challenge and add criterion
        # to contextual list if they match one of the learning objectives.
        neededCriteria = Criterion.objects.filter(learningObj__in=lo_list)
        criteriaLength = len(neededCriteria)

        # edit view, checks for rubricLine objects from this challenge
        # and sets the formset query to that instance
        context['criteria'] = neededCriteria
        context['count'] = criteriaLength

        if RubricLine.objects.filter(student=thisUserSolution).filter(evaluated__whoEvaluated=self.request.user).exists():
            print('You previously evaluated this' + str(lo_list))
            RubricLineFormset = modelformset_factory(RubricLine, formset=RubricLineForm, extra=0, fields=(
                'ignore', 'learningObjective', 'evidencePresent', 'evidenceMissing', 'feedback', 'suggestions', 'completionLevel',
                'student', 'needsLaterAttention'), widgets={'student': forms.HiddenInput,
                                                                         'completionLevel': forms.HiddenInput(), 'ignore': forms.HiddenInput(),
                                                                         'needsLaterAttention': forms.HiddenInput()})

            formset = RubricLineFormset(prefix='rubriclines', queryset=RubricLine.objects.filter(student=thisUserSolution).filter(
                evaluated__whoEvaluated=self.request.user).order_by(
                'learningObjective__compGroup', 'learningObjective__compNumber', 'learningObjective__loNumber'))

            CriterionFormSet = modelformset_factory(CriteriaLine, formset=CriteriaForm, extra=0, fields=(
                'achievement', 'criteria', 'userSolution'), widgets={'criteria': forms.HiddenInput,
                                                                                  'userSolution': forms.HiddenInput,
                                                                                  'evaluator': forms.HiddenInput})

            critFormset = CriterionFormSet(prefix='criteria', queryset=CriteriaLine.objects.all().filter(userSolution=thisUserSolution, evaluator__whoEvaluated=self.request.user))

        # if challenge has been flagged for customization
        # reroute it to this function to apply the corrected learning
        # objectives and return it to the view
        elif thisUserSolution.customized is True:
            print('customized')
            # evaluated = Evaluated(whoEvaluated=self.request.user)
            challenge = ChallengeAddendum.objects.get(userSolution=thisUserSolution)
            lo_list = LearningObjective.objects.filter(challengeaddendum=challenge).order_by('compGroup', 'compNumber',
                                                                                             'loNumber', )
            neededCriteria = Criterion.objects.filter(learningObj__in=lo_list)
            context['criteria'] = neededCriteria
            print('lo_list ' + str(len(lo_list)))
            print('needCriteria ' + str(len(neededCriteria)))

            RubricLineFormset = modelformset_factory(RubricLine, formset=RubricLineForm, extra=len(lo_list), fields=(
                'ignore', 'learningObjective', 'evidencePresent', 'evidenceMissing', 'feedback', 'suggestions',
                'completionLevel', 'student', 'needsLaterAttention', ), widgets={'student': forms.HiddenInput,
                                                                         'completionLevel': forms.HiddenInput(), 'ignore': forms.HiddenInput(),
                                                                         'needsLaterAttention': forms.HiddenInput()})

            formset = RubricLineFormset(prefix='rubriclines',
                                        initial=[{'learningObjective': learningObjective.pk, 'student': thisUserSolution
                                                  } for learningObjective in lo_list], queryset=RubricLine.objects.none())

            CriterionFormSet = modelformset_factory(CriteriaLine, formset=CriteriaForm, extra=len(neededCriteria), fields=(
                'achievement', 'criteria', 'userSolution'), widgets={'criteria': forms.HiddenInput,
                                                                   'userSolution': forms.HiddenInput})

            critFormset = CriterionFormSet(prefix='criteria',
                                           initial=[{'userSolution': thisUserSolution, 'criteria': criterion, } for
                                                    criterion in neededCriteria], queryset=CriteriaLine.objects.none())
            # custom_rubric_producer(ChallengeAddendum.objects.get(challenge=thisUserSolution))

        # create new rubric, checked for rubricline objects from this challenge
        # and none existed, so queryset is none and extra forms is set to LO count
        else:
            # evaluated = Evaluated(whoEvaluated=self.request.user)
            RubricLineFormset = modelformset_factory(RubricLine, formset=RubricLineForm, extra=loCount, fields=(
                'ignore', 'learningObjective', 'evidencePresent', 'evidenceMissing', 'feedback', 'suggestions', 'completionLevel',
                'student', 'needsLaterAttention'), widgets={'student': forms.HiddenInput,
                                                                         'completionLevel': forms.HiddenInput(), 'ignore': forms.HiddenInput(),
                                                                         'needsLaterAttention': forms.HiddenInput()})

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

        userSolution = UserSolution.objects.get(pk=self.kwargs['pk'])

        print(critFormset.errors)
        if formset.is_valid() and critFormset.is_valid():
            evaluated = Evaluated.objects.create(whoEvaluated=self.request.user)
            userSolution.evaluated.add(evaluated)

            for form in formset:
                f =form.save(commit=False)
                f.evaluated = evaluated
                f.save()
            for critForm in critFormset:
                c = critForm.save(commit=False)
                c.evaluator = evaluated
                c.save()
            userSolution.save()
            formset.save()
            critFormset.save()

            return redirect('solution-end-eval', self.kwargs['pk'])

        else:
            messages.error(request, "Error")
            challenge = UserSolution.objects.get(pk=self.kwargs['pk']).challengeName
            student = userSolution.userOwner
            content = {'formset': formset, 'critFormset': critFormset, 'challenge': challenge, 'student': student}
            return render(request, 'rubrics/rubric_form.html', content)
            # return self.render_to_response(self.get_context_data(formset=formset))


# Check user role on dashboard, use the pk on those links to load up this view with that user solution
class CoachingReviewView(FormView):
    template_name = 'rubrics/coachingreview.html'
    model = UserSolution
    form_class = CoachReviewFormset

    def get_context_data(self, **kwargs):
        context = super(CoachingReviewView, self).get_context_data()
        userSolution = self.kwargs['pk']
        thisUserSolution = UserSolution.objects.get(pk=userSolution)

        # Check if this is a modified solution
        if thisUserSolution.customized:
            challenge = ChallengeAddendum.objects.get(userSolution=thisUserSolution)
            lo_list = LearningObjective.objects.filter(challengeaddendum=challenge).order_by('compGroup', 'compNumber',
                                                                                            'loNumber').distinct().distinct()
        else:
            challenge = UserSolution.objects.get(pk=userSolution).solutionInstance
            lo_list = LearningObjective.objects.filter(solutioninstance=challenge).order_by('compGroup', 'compNumber',
                                                                                            'loNumber')
        criteria = Criterion.objects.filter(learningObj__in=lo_list).order_by('learningObj__compGroup',
                                                                              'learningObj__compNumber',
                                                                              'learningObj__loNumber')
        # set rubricLines based on whether this is a new evaluation or not
        if RubricLine.objects.all().filter(evaluated__whoEvaluated=self.request.user, student=thisUserSolution).exists():
            rubricLines = RubricLine.objects.all().filter(evaluated__whoEvaluated=self.request.user, student=thisUserSolution).exclude(evaluated__isnull=True).distinct()
            finalRubric = Rubric.objects.all().filter(userSolution=thisUserSolution).filter(evaluator=self.request.user).distinct()
        else:
            rubricLines = RubricLine.objects.filter(student=thisUserSolution).exclude(evaluated__isnull=True).order_by('learningObjective__compGroup',
                                                                                       'learningObjective__compNumber',
                                                                                       'learningObjective__loNumber')
            finalRubric = Rubric.objects.all().filter(userSolution=thisUserSolution)

        # set criteriaLines based on whether this is a new evaluation or not
        if CriteriaLine.objects.filter(evaluator__whoEvaluated=self.request.user, userSolution=thisUserSolution).exists():
            criteriaLines = CriteriaLine.objects.filter(userSolution=thisUserSolution, evaluator__whoEvaluated=self.request.user).distinct().order_by(
                'criteria__learningObj')
        else:
            criteriaLines = CriteriaLine.objects.all().filter(userSolution=thisUserSolution, ).exclude(evaluator__isnull=True).distinct().order_by(
                'criteria__learningObj')

        context['finalRubric'] = finalRubric
        context['learningObjectives'] = lo_list
        context['rubricLines'] = rubricLines
        context['criteria'] = criteria
        context['usersolution'] = thisUserSolution

        if RubricLine.objects.filter(evaluated__whoEvaluated=self.request.user, student=thisUserSolution).exists():
            print('Existence detected')

            RubricLineFormset = modelformset_factory(RubricLine, formset=RubricLineForm, extra=0, fields=(
                'ignore', 'learningObjective', 'evidencePresent', 'evidenceMissing', 'feedback', 'suggestions',
                'completionLevel', 'student', 'needsLaterAttention', 'evaluated'), widgets={'student': forms.HiddenInput})

            rFormset = RubricLineFormset(prefix='rFormset', queryset=RubricLine.objects.filter(
                                                          evaluated__whoEvaluated=self.request.user, student=thisUserSolution).order_by(
                                             'learningObjective__compGroup', 'learningObjective__compNumber',
                                             'learningObjective__loNumber'))

        else:
            print('no rubricLines detected')
            # evaluated = Evaluated(whoEvaluated=self.request.user)
            RubricLineFormset = modelformset_factory(RubricLine, formset=RubricLineForm, extra=len(rubricLines),
                                                     fields=('ignore', 'learningObjective', 'evidencePresent',
                                                         'evidenceMissing', 'feedback', 'suggestions',
                                                         'completionLevel', 'student', 'needsLaterAttention'),
                                                     widgets={'student': forms.HiddenInput})

            rFormset = RubricLineFormset(prefix='rFormset', initial=[{'learningObjective': rubricLine.learningObjective,
                                                                      'evidencePresent': rubricLine.evidencePresent,
                                                                      'evidenceMissing': rubricLine.evidenceMissing,
                                                                      'feedback': rubricLine.feedback,
                                                                      'suggestions': rubricLine.suggestions,
                                                                      'completionLevel': rubricLine.completionLevel,
                                                                      'student': rubricLine.student,
                                                                      'needsLaterAttention': rubricLine.needsLaterAttention,
                                                                      'ignore': rubricLine.ignore
                                                                      } for rubricLine in
                                                                     rubricLines],
                                         queryset=RubricLine.objects.none())

        if CriteriaLine.objects.filter(evaluator__whoEvaluated=self.request.user, userSolution=thisUserSolution).exists():
            print('Criterialines detected')
            CriterionFormSet = modelformset_factory(CriteriaLine, formset=CriteriaForm, extra=0,
                                                    fields=('achievement', 'criteria', 'userSolution', 'evaluator'),
                                                    widgets={'criteria': forms.HiddenInput,
                                                             'userSolution': forms.HiddenInput})

            critFormset = CriterionFormSet(prefix='criteria',
                                           queryset=CriteriaLine.objects.filter(userSolution=thisUserSolution,
                                                                                evaluator__whoEvaluated=self.request.user).distinct())
        else:
            # evaluated = Evaluated.objects.create(whoEvaluated=self.request.user)
            CriterionFormSet = modelformset_factory(CriteriaLine, formset=CriteriaForm, extra=len(criteriaLines), fields=(
                'achievement', 'criteria', 'userSolution'), widgets={'criteria': forms.HiddenInput,
                                                                      'userSolution': forms.HiddenInput})

            critFormset = CriterionFormSet(prefix='criteria',
                                           initial=[{'userSolution': thisUserSolution, 'criteria': criteriaLine.criteria,
                                                     'achievement': criteriaLine.achievement} for
                                                    criteriaLine in criteriaLines], queryset=CriteriaLine.objects.none())

        context['rFormset'] = rFormset
        context['critFormset'] = critFormset
        context['reviewSession'] = False
        return context

    def post(self, request, *args, **kwargs):
        # form = CoachReviewFormset(request.POST, prefix='cFormset')
        rForm = RubricLineFormset(request.POST, prefix='rFormset')
        critForm = CriterionFormSet(request.POST, prefix='criteria')
        print(critForm.errors)
        if rForm.is_valid() and critForm.is_valid():
            evaluated = Evaluated.objects.create(whoEvaluated=self.request.user)
            # userSolution.evaluated.add(evaluated)
            for form in rForm:
                f = form.save(commit=False)
                f.evaluated = evaluated
                f.save()
            for critForm in critForm:
                c = critForm.save(commit=False)
                c.evaluator = evaluated
                c.save()
            # userSolution.save()

            rForm.save()
            critForm.save()
            return redirect('solution-end-eval', self.kwargs['pk'])
            # return HttpResponseRedirect('/evals')
        else:
            messages.error(request, "Error")
            print(rForm.errors)
            return self.render_to_response(self.get_context_data(formset=rForm))


class CoachingReviewSession(FormView):
    template_name = 'rubrics/coachingreview.html'
    model = UserSolution
    form_class = CoachReviewFormset

    def get_context_data(self, **kwargs):
        context = super(CoachingReviewSession, self).get_context_data()
        userSolution = self.kwargs['pk']
        thisUserSolution = UserSolution.objects.get(pk=userSolution)

        if thisUserSolution.customized:
            challenge = ChallengeAddendum.objects.get(userSolution=thisUserSolution)
            lo_list = LearningObjective.objects.filter(challengeaddendum=challenge).order_by('compGroup', 'compNumber',
                                                                                            'loNumber')
        else:
            challenge = UserSolution.objects.get(pk=userSolution).solutionInstance
            lo_list = LearningObjective.objects.filter(solutioninstance=challenge).order_by('compGroup', 'compNumber',
                                                                                            'loNumber')
        criteria = Criterion.objects.filter(learningObj__in=lo_list).order_by('learningObj__compGroup',
                                                                              'learningObj__compNumber',
                                                                              'learningObj__loNumber')

        RubricLineFormset = modelformset_factory(RubricLine, formset=RubricLineForm, extra=0, fields=(
            'ignore', 'learningObjective', 'evidencePresent', 'evidenceMissing', 'feedback', 'suggestions',
            'completionLevel', 'student', 'needsLaterAttention', 'evaluated'), widgets={'student': forms.HiddenInput,
                                                                                        'completionLevel': forms.HiddenInput()})

        rFormset = RubricLineFormset(prefix='rFormset', queryset=RubricLine.objects.filter(
            evaluated__whoEvaluated=self.request.user, student=thisUserSolution).order_by(
            'learningObjective__compGroup', 'learningObjective__compNumber',
            'learningObjective__loNumber'))

        CriterionFormSet = modelformset_factory(CriteriaLine, formset=CriteriaForm, extra=0,
                                                fields=('achievement', 'criteria', 'userSolution', 'evaluator'),
                                                widgets={'criteria': forms.HiddenInput,
                                                         'userSolution': forms.HiddenInput})

        critFormset = CriterionFormSet(prefix='criteria',
                                       queryset=CriteriaLine.objects.filter(userSolution=thisUserSolution,
                                                                            evaluator__whoEvaluated=self.request.user).distinct())

        context['rFormset'] = rFormset
        context['critFormset'] = critFormset
        context['criteria'] = criteria
        context['usersolution'] = thisUserSolution
        context['reviewSession'] = True
        return context

    def post(self, request, *args, **kwargs):
        # form = CoachReviewFormset(request.POST, prefix='cFormset')
        rForm = RubricLineFormset(request.POST, prefix='rFormset')
        critForm = CriterionFormSet(request.POST, prefix='criteria')
        print(critForm.errors)
        if rForm.is_valid() and critForm.is_valid():
            rForm.save()
            critForm.save()
            return redirect('solution-end-eval', self.kwargs['pk'])
            # return HttpResponseRedirect('/evals')
        else:
            messages.error(request, "Error")
            print(rForm.errors)
            return self.render_to_response(self.get_context_data(formset=rForm))


class LearningExperienceView(DetailView):
    template_name = 'rubrics/learningExperience.html'
    model = LearningExperience

    def get_context_data(self, **kwargs):
        context = super(LearningExperienceView, self).get_context_data(**kwargs)
        learningExpo = LearningExperience.objects.get(pk=self.kwargs['pk'])
        relatedLearningExperiences = LearningExperience.objects.all().filter(challenge=learningExpo.challenge).order_by('index')
        if learningExpo.challenge.megaChallenge:
            relatedChallenges = MegaChallenge.objects.get(challenge=learningExpo.challenge).challenge_set.all().order_by('my_order')
            for challenge in relatedChallenges:
                print(challenge.learningexperience_set.all())
            # relatedChallenges = megaChallenge.challenge_set
            context['relatedChallenges'] = relatedChallenges

        context['learningObjectives'] = LearningObjective.objects.all().filter(learningExpo=learningExpo)
        list(relatedLearningExperiences.order_by('index'))
        context['expoList'] = relatedLearningExperiences
        context['learningExpo'] = learningExpo
        if ChallengeResources.objects.filter(challenge=learningExpo.challenge).exists():
            context['resources'] = ChallengeResources.objects.get(challenge=learningExpo.challenge)
        if ChallengeResources.objects.filter(learningExperience=self.kwargs['pk']).exists():
            context['expoResources'] = ChallengeResources.objects.filter(learningExperience=self.kwargs['pk'])
        print(str(learningExpo.index) + ' of ' + str(relatedLearningExperiences.count()))

        if learningExpo != relatedLearningExperiences.last():
            print(relatedLearningExperiences[learningExpo.index].index)

            context['nextLearningExpo'] = LearningExperience.objects.get(challenge=learningExpo.challenge, index=learningExpo.index + 1).pk
            context['last'] = False
        else:
            context['nextLearningExpo'] = learningExpo.challenge
            context['last'] = True

        if learningExpo != relatedLearningExperiences.first():
            context['previous'] = LearningExperience.objects.get(challenge=learningExpo.challenge, index=learningExpo.index - 1).pk
            context['first'] = False
        else:
            context['previous'] = learningExpo.challenge
            context['first'] = True

        return context


class ChallengeResourcesView(DetailView):
    model = ChallengeResources
    template_name = 'rubrics/challengeResources.html'

    def get_context_data(self, **kwargs):
        context = super(ChallengeResourcesView, self).get_context_data()
        challengeResources = ChallengeResources.objects.get(pk=self.kwargs['pk'])
        files = ChallengeResourcesFile.objects.all().filter(challengeResources=challengeResources)
        context['files'] = files
        context['challengeResources'] = challengeResources

        return context


class LearningExperienceCreator(FormView):
    template_name = 'rubrics/learningExperienceCreator.html'
    model = LearningExperience
    form_class = LearningExperienceFormset

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
            queryset = UserSolution.objects.all().filter(evaluated__isnull=False).distinct()
            return queryset

        if profile.role == 3 or profile.role == 2:
            group = self.request.user.groups.all()
            print(group)
            queryset = UserSolution.objects.filter(userOwner__groups__in=group).filter(evaluated__isnull=False).distinct()
            return queryset

        else:
            queryset = UserSolution.objects.filter(userOwner=self.request.user)
            return queryset

    def get_context_data(self, **kwargs):
        context = super(EvalListView, self).get_context_data(**kwargs)

        if self.request.user.profile.role == 4:
            form = UserSolutionToView(self.request.GET)
            if form.is_valid():
                userSolutions = UserSolution.objects.filter(userOwner=form.cleaned_data['chooseUser']).filter(
                        evaluated__isnull=False).distinct()
            else:
                userSolutions = UserSolution.objects.all().filter(evaluated__isnull=False).distinct()
            context['form'] = form
        elif self.request.user.profile.role == 2 or self.request.user.profile.role == 3:
                group = self.request.user.groups.all()
                print(group)
                userSolutions = UserSolution.objects.filter(userOwner__groups__in=group).filter(
                    evaluated__isnull=False).distinct()
        else:
            userSolutions = UserSolution.objects.all().filter(userOwner=self.request.user)

        context['userSolutions'] = userSolutions

        return context

    context_object_name = 'evals'
    template_name = "rubrics/eval_list.html"


class EvalDetailView(DetailView):
    model = UserSolution
    template_name = "rubrics/evalDetail.html"

    def get_context_data(self, **kwargs):
        context = super(EvalDetailView, self).get_context_data(**kwargs)
        rubric = self.kwargs['pk']

        if UserSolution.objects.filter(evaluated__whoEvaluated__profile__role=3).exists():
            context['notReady'] = False
        else:
            context['notReady'] = True

        # try:
        #    if CoachReview.objects.get(userSolution=rubric).release:
        #        context['notReady'] = False
        # except:
        #    context['notReady'] = True

        if self.request.user.profile.role is not 1:
            context['evaluation'] = RubricLine.objects.all().filter(student=rubric)
        else:
            context['evaluation'] = RubricLine.objects.all().filter(student=rubric, evaluated__whoEvaluated__profile__role=3)
        context['userRole'] = self.request.user.profile.role

        try:
            context['evalFinalForm'] = Rubric.objects.get(userSolution=rubric, evaluator__profile__role=3)
            # print(Rubric.objects.get(userSolution=rubric, evaluator__profile__role=3).generalFeedback)
        except:
            context['evalFinalForm'] = 'There was an error'
            print('There was nothing found')

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
        learningObjs = LearningObjective.objects.all().filter(archive=False).order_by('compGroup', 'compNumber', 'loNumber')
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


def searchSubmissions(request):
    solutions = UserSolution.objects.all()
    coachReviews = CoachReview.objects.all()
    solution_filter = EvalFilter(request.GET, queryset=solutions)
    return render(request, 'rubrics/solutions.html', {'filter': solution_filter, 'coachReview': coachReviews})

