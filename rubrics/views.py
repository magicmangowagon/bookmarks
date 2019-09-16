from django.shortcuts import render, redirect, render_to_response
from datetime import date, datetime
from django import forms
from django.http import HttpResponseRedirect, HttpResponseForbidden
from .models import Challenge, UserSolution, Rubric, RubricLine, LearningObjective, Criterion, CriteriaLine, \
    Competency, CompetencyProgress, ChallengeAddendum, LearningExperience, LearningExpoResponses, Evaluated, \
    CoachReview, SolutionInstance, MegaChallenge
from .forms import UserFileForm, UserFileFormset, RubricLineForm, RubricLineFormset, RubricForm, RubricFormSet, \
    CriterionFormSet, CriteriaForm, CurrentStudentToView, RubricAddendumForm, RubricAddendumFormset, \
    LearningExperienceFormset, LearningExperienceForm, LearningExpoFeedbackForm, LearningExpoFeedbackFormset, \
    CoachReviewForm, CoachReviewFormset
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.forms import modelformset_factory
from django.contrib import messages
from django.contrib.auth.models import User, Group
from .functions import process_rubricLine, assess_competency_done, custom_rubric_producer, mega_challenge_builder


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
                    learningObjectives.append(learningObjective)

            context['learningObjectives'] = learningObjectives
            context['challengeCover'] = Challenge.objects.all().filter(megaChallenge=challengeCover.megaChallenge)
        else:
            learningObjectives = LearningObjective.objects.all().filter(challenge=challengeCover).order_by('compGroup',
                                                                                                           'compNumber',
                                                                                                           'loNumber')
            context['learningObjectives'] = learningObjectives
            context['challengeCover'] = challengeCover



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
                                       widgets={'userOwner': forms.HiddenInput, 'challengeName': forms.HiddenInput, })

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
        solutions = SolutionInstance.objects.all().filter(challenge_that_owns_me=challenge)

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
    queryset = Challenge.objects.all().filter(display=True)
    context_object_name = 'challenges'
    template_name = 'rubrics/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lo_list'] = LearningObjective.objects.all().order_by('compGroup', 'compNumber', 'loNumber')
        return context


class MegaSubPage(DetailView):
    model = MegaChallenge
    template_name = 'rubrics/sub_list.html'

    def get_context_data(self, **kwargs):
        context = super(MegaSubPage, self).get_context_data()
        challenges = Challenge.objects.all().filter(megaChallenge=self.kwargs['pk'])
        context['challenges'] = challenges
        learningExpos = LearningExperience.objects.all().filter(challenge__megaChallenge=self.kwargs['pk'])
        context['learningExpos'] = learningExpos
        return context


class SolutionListView(ListView):

    def get_queryset(self):
        profile = self.request.user.profile

        # groupName = self.request.user.groups('name')
        if profile.role == 4:
            queryset = UserSolution.objects.all()
            return queryset

        if profile.role == 3:

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

        if Rubric.objects.all().filter(userSolution=userSolution).exists():
            RubricFormSet = modelformset_factory(Rubric, extra=0, formset=RubricForm, fields=(
            'userSolution', 'challenge', 'evaluator', 'generalFeedback', 'challengeCompletionLevel',),
             widgets={'userSolution': forms.HiddenInput, 'challenge': forms.HiddenInput, 'evaluator': forms.HiddenInput,
                      'challengeCompletionLevel': forms.HiddenInput})

            formset = RubricFormSet(queryset=Rubric.objects.all().filter(userSolution=userSolution))

        else:
            RubricFormSet = modelformset_factory(Rubric, extra=1, formset=RubricForm, fields=(
            'userSolution', 'challenge', 'evaluator', 'generalFeedback', 'challengeCompletionLevel'),
             widgets={'userSolution': forms.HiddenInput, 'challenge': forms.HiddenInput, 'evaluator': forms.HiddenInput,
                      'challengeCompletionLevel': forms.HiddenInput})

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
        challenge = UserSolution.objects.get(pk=usersolution).solutionInstance
        context['lo_list'] = LearningObjective.objects.filter(solutioninstance=challenge)
        lo_list = LearningObjective.objects.filter(solutioninstance=challenge).order_by('compGroup', 'compNumber', 'loNumber')
        thisUserSolution = UserSolution.objects.get(pk=usersolution)
        context['student'] = thisUserSolution
        try:
            context['challenge'] = challenge.challenge_that_owns_me.all().first
        except:
            context['challenge'] = challenge

        context['solutionInstance'] = challenge
        loCount = LearningObjective.objects.filter(solutioninstance=challenge).count()

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

        # if RubricLine.objects.all().filter(student=usersolution).exists() and Evaluated.objects.filter(whoEvaluated=self.request.user):
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
        evaluated = Evaluated.objects.create(whoEvaluated=self.request.user, date=datetime.now())
        userSolution = UserSolution.objects.get(pk=self.kwargs['pk'])
        userSolution.evaluated.add(evaluated)

        if formset.is_valid() and critFormset.is_valid():
            formset.save()
            critFormset.save()
            userSolution.save()
            return redirect('solution-end-eval', self.kwargs['pk'])

        else:
            messages.error(request, "Error")
            challenge = UserSolution.objects.get(pk=self.kwargs['pk']).challengeName
            student = formset.student
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
        print(thisUserSolution)
        challenge = UserSolution.objects.get(pk=userSolution).challengeName
        lo_list = LearningObjective.objects.filter(challenge=challenge).order_by('compGroup', 'compNumber', 'loNumber')
        extras = len(lo_list)
        rubricLines = RubricLine.objects.all().filter(learningObjective__in=lo_list, student=thisUserSolution)
        context['learningObjectives'] = lo_list
        context['rubricLines'] = rubricLines

        RubricLineFormset = modelformset_factory(RubricLine, formset=RubricLineForm, extra=extras, fields=(
            'ignore', 'learningObjective', 'evidencePresent', 'evidenceMissing', 'feedback', 'suggestions',
            'completionLevel', 'student', 'needsLaterAttention',), widgets={'student': forms.HiddenInput, })

        formset = RubricLineFormset(prefix='rubriclines',
                                    initial=[{'learningObjective': learningObjective.pk, 'student': thisUserSolution}
                                             for learningObjective in lo_list], queryset=RubricLine.objects.none())
        context['formset'] = formset

        return context


class LearningExperienceView(DetailView):
    template_name = 'rubrics/learningExperience.html'
    model = LearningExperience

    def get_context_data(self, **kwargs):
        context = super(LearningExperienceView, self).get_context_data(**kwargs)
        learningExpo = LearningExperience.objects.get(pk=self.kwargs['pk'])
        relatedLearningExperiences = LearningExperience.objects.all().filter(challenge=learningExpo.challenge).order_by('index')
        context['learningObjectives'] = LearningObjective.objects.all().filter(learningExpo=learningExpo)
        list(relatedLearningExperiences.order_by('index'))
        context['expoList'] = relatedLearningExperiences
        context['learningExpo'] = learningExpo
        if learningExpo != relatedLearningExperiences.last():
            context['nextLearningExpo'] = relatedLearningExperiences[learningExpo.index + 1]
            context['last'] = False
        else:
            context['nextLearningExpo'] = learningExpo.challenge
            context['last'] = True

        if learningExpo != relatedLearningExperiences.first():
            context['previous'] = relatedLearningExperiences[learningExpo.index - 1]
            context['first'] = False
        else:
            context['previous'] = learningExpo.challenge
            context['first'] = True

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
            queryset = UserSolution.objects.all()
            return queryset

        if profile.role == 3:

            group = self.request.user.groups.all()
            print(group)
            queryset = UserSolution.objects.filter(userOwner__groups__in=group)
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



