from django.shortcuts import render, redirect, render_to_response
from datetime import date, datetime
from django import forms
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from centralDispatch.models import SolutionRouter
from .models import Challenge, UserSolution, Rubric, RubricLine, LearningObjective, Criterion, CriteriaLine, \
    Competency, CompetencyProgress, ChallengeAddendum, LearningExperience, LearningExpoResponses, Evaluated, \
    CoachReview, SolutionInstance, MegaChallenge, ChallengeResources, ChallengeResourcesFile, TfJEval, TfJSolution
from .forms import UserFileForm, UserFileFormset, RubricLineForm, RubricLineFormset, RubricForm, RubricFormSet, \
    CriterionFormSet, CriteriaForm, CurrentStudentToView, RubricAddendumForm, RubricAddendumFormset, \
    LearningExperienceFormset, LearningExperienceForm, LearningExpoFeedbackForm, LearningExpoFeedbackFormset, \
    CoachReviewForm, CoachReviewFormset, UserSolutionToView, TfJEvalFormset, TfJEvalForm, \
    TfJForm
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.forms import modelformset_factory
from django.contrib import messages
# from django.contrib.messages import get_messages
from django.contrib.auth.models import User, Group
from django.db.models import Q
from .functions import assess_competency_done
from django.core.mail import send_mail
from .filters import EvalFilter
from centralDispatch.models import ChallengeStatus, SolutionStatus
from centralDispatch.functions import submissionAlert, evaluationCompleted, process_rubricLine
from centralDispatch.forms import ChallengeStatusForm, ChallengeStatusFormset
from info.models import DiscussionBoard


class CourseCatalog(ListView):
    model = MegaChallenge
    # queryset = Challenge.objects.all().filter(display=True).order_by('challengeGroupChoices')
    context_object_name = 'challenges'
    template_name = 'rubrics/coursecatalog.html'
    queryset = MegaChallenge.objects.all().filter(display=True).order_by('challengeGroupChoices')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        competencies = Competency.objects.all().order_by('-id', 'compGroup', 'compNumber').distinct('id')
        context['competencies'] = competencies
        context['megaChallenges'] = MegaChallenge.objects.all()
        return context


class ChallengeCover(DetailView):

    model = Challenge

    def get_context_data(self, **kwargs):
        context = super(ChallengeCover, self).get_context_data(**kwargs)

        challengeCover = Challenge.objects.get(pk=self.kwargs['pk'])

        if challengeCover.megaChallenge:
            print('mega')
            challenges = Challenge.objects.all().filter(megaChallenge=challengeCover.megaChallenge)
            learningObjectives = LearningObjective.objects.filter(
                challenge__in=challengeCover.megaChallenge.challenge_set.all()).order_by('compGroup', 'compNumber', 'loNumber')
            print(learningObjectives)
            context['learningObjectives'] = learningObjectives
            context['challengeCover'] = Challenge.objects.all().filter(megaChallenge=challengeCover.megaChallenge)
            context['challengeParent'] = challengeCover.megaChallenge
            print(challengeCover.megaChallenge.challenge_set.all())
        else:
            print('not mega')
            learningObjectives = LearningObjective.objects.all().filter(challenge=challengeCover).order_by('compGroup',
                                                                                                           'compNumber',
                                                                                                           'loNumber')
            context['learningObjectives'] = learningObjectives
            context['challengeCover'] = challengeCover

        context['criterionList'] = Criterion.objects.all().filter(learningObj__in=learningObjectives)

        competencies = Competency.objects.filter(learningObjs__in=learningObjectives).order_by('-id', 'compGroup', 'compNumber').distinct('id')
        print(learningObjectives.count())
        print(competencies.count())
        context['competencies'] = competencies

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
        print(thisChallenge)
        relatedLearningExperiences = LearningExperience.objects.filter(challenge=thisChallenge).order_by('index')

        context['previous'] = relatedLearningExperiences.last().pk

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
                thisChallenge = SolutionInstance.objects.get(pk=self.kwargs['pk'])
                print(thisChallenge)
                print(self.request.user.first_name)
                submissionAlert(thisChallenge, self.request.user)
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


class TfJSolutionSubmissionView(FormView):
    form_class = TfJForm
    model = SolutionInstance
    template_name = 'rubrics/tfj_upload.html'

    def get_context_data(self, **kwargs):
        context = super(TfJSolutionSubmissionView, self).get_context_data(**kwargs)
        # TfJSolutionSubmissionFormset = modelformset_factory(TfJSolution, extra=1, formset=TfJForm, fields=('solution', 'learningObjectives'), )
        # formset = TfJSolutionSubmissionFormset(initial={'solutionInstance': self.kwargs['pk']})
        solutionInstance = SolutionInstance.objects.get(pk=self.kwargs['pk'])
        formset = TfJForm(initial={'solutionInstance': self.kwargs['pk'], 'user': self.request.user,
                                   'coachLO': solutionInstance.learningObjectives.first()})

        context['solutionInstance'] = solutionInstance
        context['formset'] = formset
        # previousRubricLines = RubricLine.objects.all().filter(student__userOwner=self.request.user, learningObjective__competency__compGroup='E').order_by('learningObjective__compNumber')
        previousTfJEvals = TfJEval.objects.all().filter(userSolution__user=self.request.user).order_by('learningObjective__compNumber', 'learningObjective__loNumber')
        context['previousWork'] = previousTfJEvals

        relatedLearningExperiences = LearningExperience.objects.all().filter(
            challenge=solutionInstance.challenge_that_owns_me.first()).order_by('index')
        context['previous'] = relatedLearningExperiences.last().pk

        return context

    def form_valid(self, form):
        print('valid')
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return '/challenge/' + str(self.kwargs['pk']) + '/success'


class TfJEvaluation(FormView):
    model = TfJSolution
    form_class = TfJEvalFormset
    template_name = 'rubrics/tfjeval.html'

    def get_context_data(self, **kwargs):
        context = super(TfJEvaluation, self).get_context_data(**kwargs)
        solution = TfJSolution.objects.get(pk=self.kwargs['pk'])

        if not solution.coachLO:
            solution.coachLO = solution.solutionInstance.learningObjectives.first()
            solution.save()
        learningObjectives = [solution.coachLO, solution.tcLO]
        if TfJEval.objects.filter(userSolution=solution).exists():
            previousEvals = TfJEval.objects.all().filter(userSolution=solution).order_by('learningObjective__loNumber',
                                                                                 '-evaluator__date').distinct(
                'learningObjective__loNumber')
            print(previousEvals.count())
            TfJEvalFormset = modelformset_factory(TfJEval, formset=TfJEvalForm, extra=2, fields=(
                'learningObjective', 'userSolution', 'question1', 'question2', 'question3', 'question4', 'question5'),
                                                  widgets={'userSolution': forms.HiddenInput()})

            formset = TfJEvalFormset(initial=[{'learningObjective': previousEval.learningObjective,
                                               'userSolution': previousEval.userSolution,
                                               'question1': previousEval.question1,
                                               'question2': previousEval.question2,
                                               'question3': previousEval.question3,
                                               'question4': previousEval.question4,
                                               'question5': previousEval.question5}
                                              for previousEval in previousEvals], queryset=TfJEval.objects.none())

        else:
            TfJEvalFormset = modelformset_factory(TfJEval, formset=TfJEvalForm, extra=2, fields=(
                'learningObjective', 'userSolution', 'question1', 'question2', 'question3', 'question4', 'question5'),
                                                  widgets={'userSolution': forms.HiddenInput()})

            formset = TfJEvalFormset(initial=[{'learningObjective': learningObjective, 'userSolution': solution}
                                              for learningObjective in learningObjectives])
        context['formset'] = formset
        context['usersolution'] = solution
        previousTfJEvals = TfJEval.objects.all().filter(userSolution__user=solution.user).order_by(
            'learningObjective__compNumber')
        context['previousWork'] = previousTfJEvals
        context['previousWork'] = TfJEval.objects.filter(userSolution=solution).order_by(
            'learningObjective__compNumber', 'learningObjective__loNumber')
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            formset = TfJEvalFormset(request.POST)
            evaluator = Evaluated.objects.create(whoEvaluated=self.request.user)

            if formset.is_valid():
                for form in formset:
                    f = form.save(commit=False)
                    f.evaluator = evaluator
                    f.save()
                # evaluator.save()
                # evaluator = Evaluated.objects.create(whoEvaluated=self.request.user)
                print(evaluator)

                formset.save()
                return HttpResponseRedirect('/evals')
            else:
                print(formset.errors)
                # evaluator.delete()
                return self.render_to_response(self.get_context_data(formset=formset))


class SolutionSectionView(DetailView):
    template_name = 'rubrics/solution_sections.html'
    model = Challenge

    def get_context_data(self, **kwargs):
        context = super(SolutionSectionView, self).get_context_data(**kwargs)
        challenge = Challenge.objects.get(id=self.kwargs['pk'])
        context['challenge'] = challenge
        context['lo_list'] = LearningObjective.objects.all().filter(challenge=challenge).order_by('compGroup', 'compNumber', 'loNumber')
        solutions = SolutionInstance.objects.all().filter(challenge_that_owns_me=challenge).order_by('order')

        # field_value = getattr(obj, field_name)
        for solution in solutions:

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
        usersRubricLines = RubricLine.objects.all().filter(student__userOwner=thisSolution.userOwner).filter(
            evaluated__whoEvaluated__profile__role__gte=3)

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
    model = MegaChallenge
    # queryset = Challenge.objects.all().filter(display=True).order_by('challengeGroupChoices')
    context_object_name = 'challenges'
    template_name = 'rubrics/list.html'
    queryset = MegaChallenge.objects.all().filter(display=True).order_by('challengeGroupChoices')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['megaChallenges'] = MegaChallenge.objects.all()
        return context


class MegaSubPage(FormView):
    model = MegaChallenge
    template_name = 'rubrics/sub_list.html'
    form_class = ChallengeStatusFormset

    def get_context_data(self, **kwargs):
        context = super(MegaSubPage, self).get_context_data(**kwargs)
        challenges = Challenge.objects.all().filter(megaChallenge=self.kwargs['pk']).order_by('my_order')
        context['challenges'] = challenges
        learningExpos = []

        # Determine best way to stop non-tc's from generating these models, leave as is for now
        for challenge in challenges:
            learningExpos.append(LearningExperience.objects.all().filter(challenge=challenge).order_by('index').first())
            if ChallengeStatus.objects.filter(user=self.request.user, challenge=challenge).exists():
                print('fart')
                cs = ChallengeStatus.objects.get(user=self.request.user, challenge=challenge)
                cs.save()
            else:
                ChallengeStatus.objects.create(user=self.request.user, challenge=challenge)
                print('ChallengeStatus object created')

        context['learningExpos'] = learningExpos
        ChallengeStatusFormset = modelformset_factory(ChallengeStatus, extra=0,
                                                      fields=('user', 'challenge', 'challengeAccepted'),
                                                      widgets={'user': forms.HiddenInput, 'challenge': forms.HiddenInput})
        challengeStatusForm = ChallengeStatusFormset(queryset=ChallengeStatus.objects.filter(user=self.request.user, challenge__in=challenges) )

        context['challengeStatusForm'] = challengeStatusForm
        return context

    def post(self, request, *args, **kwargs):
        challenges = Challenge.objects.all().filter(megaChallenge=self.kwargs['pk']).order_by('my_order')
        learningExpos = []
        for challenge in challenges:
            learningExpos.append(LearningExperience.objects.all().filter(challenge=challenge).order_by('index').first())

        if request.method == 'POST':
            form = ChallengeStatusFormset(request.POST)

            if form.is_valid():
                form.save()

            else:
                print(form.errors)
        else:
            form = ChallengeStatusFormset()

        context = {'form': form, 'challenges': challenges, 'learningExpos': learningExpos}
        return render(request, self.get_template_names(), context)


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
            # challengeCoachAssigned = UserSolution.objects.all().filter(challengeName__solutionrouter__profile=profile).filter(evaluated__isnull=False).distinct()
            # solutionByTopic = UserSolution.objects.all().filter(userOwner__profile__subjectMatter=profile.subjectMatter).distinct()
            # specificallyAssigned = UserSolution.objects.filter(userOwner__groups__in=group).filter(evaluated__isnull=False).distinct()

            # userSolutions = challengeCoachAssigned | solutionByTopic | specificallyAssigned
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

            if self.request.user.profile.role >= 3:
                if Rubric.objects.filter(userSolution=userSolution).exists():
                    previousFeedback = Rubric.objects.all().filter(userSolution=userSolution).last().generalFeedback
                else:
                    previousFeedback = ''
                formset = RubricFormSet(prefix='rFormset',
                                        initial=[{'userSolution': userSolution, 'challenge': challenge,
                                                  'evaluator': self.request.user,
                                                  'generalFeedback': previousFeedback,
                                                  'challengeCompletionLevel': incrementor}],
                                        queryset=Rubric.objects.none())
            else:
                formset = RubricFormSet(prefix='rFormset', initial=[{'userSolution': userSolution, 'challenge': challenge,
                 'evaluator': self.request.user, 'challengeCompletionLevel': incrementor}], queryset=Rubric.objects.none())

        if self.request.user.profile.role >= 3:
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

        userSolution = UserSolution.objects.get(id=self.kwargs['pk'])

        if self.request.user.profile.role >= 3:
            coachForm = CoachReviewFormset(request.POST, prefix='coachRevFormset')

        if form.is_valid():
            super().form_valid(form)
            form.save()

            theseRubricLines = RubricLine.objects.filter(evaluated__whoEvaluated=self.request.user).filter(
                student=userSolution).order_by('learningObjective__id', '-evaluated__date',).distinct('learningObjective')
            # completionLevelObj = RubricLine.objects.all().filter(self__in=f)
            if self.request.user.profile.role >= 3:
                if coachForm.is_valid():
                    coachForm.save()
                    print('coachReview saved')
                    if self.request.user.profile.role >= 3:

                        process_rubricLine(theseRubricLines)
                        assess_competency_done(theseRubricLines)
            # moved this out of the above conditional, thinking this is the
            # reason evaluation notifications aren't going out to coaches
            evaluationCompleted(userSolution, self.request.user)
            return HttpResponseRedirect('/evals')
        else:
            messages.error(request, "Error")
            return self.render_to_response(self.get_context_data(formset=form))

        # creating form that comes after RubricFormView/formsets
        # holds general feedback, and challenge completion level.
        # show slider on formset view for challenge completion level but store in permanently
        # on this page.


class TFJHotFixView(ListView):
    # queryset = UserSolution.objects.all().filter(solutionInstance__name__icontains='Tfj')
    template_name = 'rubrics/tfj_list.html'
    context_object_name = 'solutions'

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = UserSolution.objects.all().filter(solutionInstance__name__icontains='Tfj')
        else:
            queryset = None
        return queryset


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
            lo_list = LearningObjective.objects.filter(challengeaddendum=challenge)
        else:
            challenge = UserSolution.objects.get(pk=usersolution).solutionInstance
            lo_list = LearningObjective.objects.filter(solutioninstance=challenge)

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

        # print(critFormset.errors)
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


# ________
# Updated Evaluation Page
# Need to test with SolutionStatus set to return to
# Check that updated rubricLines from self are shown, but only the latest
class SolutionEvaluationView(FormView):
    template_name = 'rubrics/rubric_form.html'
    model = UserSolution
    form_class = RubricLineFormset

    def get_context_data(self, **kwargs):
        context = super(SolutionEvaluationView, self).get_context_data()

        userSolution = UserSolution.objects.get(pk=self.kwargs['pk'])

        if userSolution.customized:
            challenge = ChallengeAddendum.objects.get(userSolution=userSolution)
            lo_list = LearningObjective.objects.filter(challengeaddendum=challenge)
        else:
            challenge = userSolution.solutionInstance
            lo_list = LearningObjective.objects.filter(solutioninstance=challenge)

        context['lo_list'] = lo_list
        context['student'] = userSolution
        context['usersolution'] = userSolution

        try:
            context['challenge'] = challenge.challenge_that_owns_me.all().first
        except:
            context['challenge'] = challenge

        context['solutionInstance'] = userSolution.solutionInstance
        loCount = len(lo_list)

        context['userRole'] = self.request.user.profile.role

        neededCriteria = Criterion.objects.filter(learningObj__in=lo_list)
        criteriaLength = len(neededCriteria)

        context['criteria'] = neededCriteria
        context['count'] = criteriaLength

        # Set up each formset, always create new ones initialized based on conditions
        # delineated below
        RubricLineFormset = modelformset_factory(RubricLine, formset=RubricLineForm, extra=loCount, fields=(
            'ignore', 'learningObjective', 'evidencePresent', 'evidenceMissing', 'feedback', 'suggestions',
            'completionLevel',
            'student', 'needsLaterAttention'), widgets={'student': forms.HiddenInput,
                                                        'completionLevel': forms.HiddenInput(),
                                                        'ignore': forms.HiddenInput(),
                                                        'needsLaterAttention': forms.HiddenInput()})

        CriterionFormSet = modelformset_factory(CriteriaLine, formset=CriteriaForm, extra=criteriaLength, fields=(
            'achievement', 'criteria', 'userSolution'), widgets={'criteria': forms.HiddenInput,
                                                                 'userSolution': forms.HiddenInput,
                                                                 'evaluator': forms.HiddenInput})

        RubricFormSet = modelformset_factory(Rubric, extra=1, formset=RubricForm, fields=(
            'userSolution', 'challenge', 'evaluator', 'generalFeedback', 'challengeCompletionLevel',),
                                             widgets={'userSolution': forms.HiddenInput, 'challenge': forms.HiddenInput,
                                                      'evaluator': forms.HiddenInput,
                                                      'challengeCompletionLevel': forms.HiddenInput})

        # Need a more thorough check of status of solution, initial return to should populate with coaches feedback.
        # After that do we lock the eval? Allow the Evaluator to continue editing until a coach looks at it again?
        if RubricLine.objects.filter(student=userSolution).exists():
            print('found old eval')
            if SolutionStatus.objects.filter(userSolution=userSolution):
                print('status object found')
                solutionStatus = SolutionStatus.objects.get(userSolution=userSolution)
                if solutionStatus.returnTo == self.request.user or self.request.user.profile.role == 4:
                    print('returned to evaluator')
                    rubricLines = RubricLine.objects.filter(
                        learningObjective__in=userSolution.solutionInstance.learningObjectives.all()).order_by('learningObjective__id', '-evaluated__date', ).distinct('learningObjective').filter(
                        student=userSolution)
                    # rubricLines = RubricLines.order_by('learningObjective__compGroup', 'learningObjective__compNumber', 'learningObjective__compNumber',)
                    criteriaLines = CriteriaLine.objects.all().filter(userSolution=userSolution).order_by('criteria', '-evaluator__date').distinct('criteria')
                    try:
                        rubric = Rubric.objects.all().filter(userSolution=userSolution).last()
                        rubricFormset = RubricFormSet(prefix='rFormset',
                                                      queryset=Rubric.objects.none(),
                                                      initial=[{'userSolution': rubric.userSolution,
                                                               'challenge': rubric.challenge,
                                                               'evaluator': self.request.user,
                                                               'generalFeedback': rubric.generalFeedback}])
                    except:
                        rubricFormset = RubricFormSet(prefix='rFormset',
                                                      queryset=Rubric.objects.none(),
                                                      initial=[{'userSolution': userSolution,
                                                               'challenge': userSolution.challengeName,
                                                               'evaluator': self.request.user}])

                    formset = RubricLineFormset(prefix='rubriclines',
                                                initial=[{'learningObjective': rubricLine.learningObjective,
                                                          'student': rubricLine.student,
                                                          'evidencePresent': rubricLine.evidencePresent,
                                                          'evidenceMissing': rubricLine.evidenceMissing,
                                                          'feedback': rubricLine.feedback,
                                                          'suggestions': rubricLine.suggestions,
                                                          'completionLevel': rubricLine.completionLevel,
                                                          'needsLaterAttention': rubricLine.needsLaterAttention,
                                                          'ignore': rubricLine.ignore
                                                          } for rubricLine in rubricLines],
                                                queryset=RubricLine.objects.none())

                    critFormset = CriterionFormSet(prefix='criteria',
                                                   initial=[{'userSolution': criteriaLine.userSolution,
                                                             'criteria': criteriaLine.criteria,
                                                             'achievement': criteriaLine.achievement} for
                                                            criteriaLine in criteriaLines],
                                                   queryset=CriteriaLine.objects.none())


                else:
                    print('Not for you')
                    formset = 'Not Authorized'
                    critFormset = 'Not Authorized'
                    rubricFormset = 'Not Authorized'

            elif RubricLine.objects.filter.filter(evaluated__whoEvaluated=self.request.user, userSolution=userSolution).exists():
                print('Eval unchanged')
                rubricLines = RubricLine.objects.all().filter(userSolution=userSolution,
                                                              evaluated__whoEvaluated=self.request.user).order_by('learningObjective').distinct('learningObjective').latest()
                criteriaLines = CriteriaLine.objects.all().filter(userSolution=userSolution,
                                                                  evaluated__whoEvaluated=self.request.user).latest().distinct()
                rubric = Rubric.objects.get(userSolution=userSolution, evaluator=self.request.user).latest()
                formset = RubricLineFormset(prefix='rubriclines',
                                            initial=[{'learningObjective': rubricLine.learningObjective,
                                                      'student': rubricLine.student,
                                                      'evidencePresent': rubricLine.evidencePresent,
                                                      'evidenceMissing': rubricLine.evidenceMissing,
                                                      'feedback': rubricLine.feedback,
                                                      'suggestions': rubricLine.suggestions,
                                                      'completionLevel': rubricLine.completionLevel,
                                                      'needsLaterAttention': rubricLine.needsLaterAttention,
                                                      'ignore': rubricLine.ignore
                                                      } for rubricLine in rubricLines],
                                            queryset=RubricLine.objects.none())

                critFormset = CriterionFormSet(prefix='criteria',
                                               initial=[{'userSolution': criteriaLine.userSolution,
                                                         'criteria': criteriaLine.criteria,
                                                         'achievement': criteriaLine.achievement} for
                                                        criteriaLine in criteriaLines],
                                               queryset=CriteriaLine.objects.none())

                rubricFormset = RubricFormSet(prefix='rFormset',
                                              queryset=Rubric.objects.none(),
                                              initial={'userSolution': rubric.userSolution,
                                                       'challenge': rubric.challenge,
                                                       'evaluator': self.request.user,
                                                       'generalFeedback': rubric.generalFeedback,
                                                       'challengeCompletionLevel': rubric.challengeCompletionLevel})


        # if challenge has been flagged for customization
        # reroute it to this function to apply the corrected learning
        # objectives and return it to the view
        elif userSolution.customized is True:
            print('Customized Eval')
            # evaluated = Evaluated(whoEvaluated=self.request.user)
            challenge = ChallengeAddendum.objects.get(userSolution=userSolution)
            lo_list = LearningObjective.objects.filter(challengeaddendum=challenge).order_by('compGroup', 'compNumber',
                                                                                             'loNumber', )
            neededCriteria = Criterion.objects.filter(learningObj__in=lo_list)
            context['criteria'] = neededCriteria
            print('lo_list ' + str(len(lo_list)))
            print('needCriteria ' + str(len(neededCriteria)))

            formset = RubricLineFormset(prefix='rubriclines',
                                        initial=[{'learningObjective': learningObjective.pk, 'student': learningObjective
                                                  } for learningObjective in lo_list],
                                        queryset=RubricLine.objects.none())


            critFormset = CriterionFormSet(prefix='criteria',
                                           initial=[{'userSolution': userSolution, 'criteria': criterion, } for
                                                    criterion in neededCriteria], queryset=CriteriaLine.objects.none())

            rubricFormset = RubricFormSet(prefix='rFormset',
                                          queryset=Rubric.objects.none())
            # custom_rubric_producer(ChallengeAddendum.objects.get(challenge=thisUserSolution))

        # create new rubric, checked for rubricline objects from this challenge
        # and none existed, so queryset is none and extra forms is set to LO count
        else:
            print('New Eval')
            formset = RubricLineFormset(prefix='rubriclines',
                                        initial=[
                                            {'learningObjective': learningObjective.pk, 'student': userSolution} for
                                            learningObjective in
                                            lo_list], queryset=RubricLine.objects.none())

            critFormset = CriterionFormSet(prefix='criteria',
                                           initial=[{'userSolution': userSolution, 'criteria': criterion} for
                                                    criterion in neededCriteria],
                                           queryset=CriteriaLine.objects.none())
            print(userSolution)
            print(userSolution.challengeName)
            print(self.request.user)
            rubricFormset = RubricFormSet(prefix='rFormset',
                                          queryset=Rubric.objects.none(),
                                          initial=[{'userSolution': userSolution,
                                                   'challenge': userSolution.challengeName,
                                                   'evaluator': self.request.user}])

        context['formset'] = formset
        context['critFormset'] = critFormset
        context['rubricFormset'] = rubricFormset
        return context

    def post(self, request, *args, **kwargs):
        formset = RubricLineFormset(request.POST, prefix='rubriclines')
        critFormset = CriterionFormSet(request.POST, prefix='criteria')
        rubricFormset = RubricFormSet(request.POST, prefix='rFormset')

        userSolution = UserSolution.objects.get(pk=self.kwargs['pk'])

        # print(critFormset.errors)
        if formset.is_valid() and critFormset.is_valid() and rubricFormset.is_valid():
            evaluated = Evaluated.objects.create(whoEvaluated=self.request.user)
            userSolution.evaluated.add(evaluated)

            for form in formset:
                f = form.save(commit=False)
                f.evaluated = evaluated
                f.save()
            for critForm in critFormset:
                c = critForm.save(commit=False)
                c.evaluator = evaluated
                c.save()
            rubricFormset.save()
            userSolution.save()
            formset.save()
            critFormset.save()

            return HttpResponseRedirect('/evals')

        else:
            messages.error(request, "Error")
            challenge = UserSolution.objects.get(pk=self.kwargs['pk']).challengeName
            student = userSolution.userOwner
            content = {'formset': formset, 'critFormset': critFormset, 'challenge': challenge,
                       'student': student, 'rubricFormset': rubricFormset}
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
            lo_list = LearningObjective.objects.filter(challengeaddendum=challenge)
        else:
            challenge = UserSolution.objects.get(pk=userSolution).solutionInstance
            lo_list = LearningObjective.objects.filter(solutioninstance=challenge)
        criteria = Criterion.objects.filter(learningObj__in=lo_list).order_by('learningObj_id')
        # set rubricLines based on whether this is a new evaluation or not
        if RubricLine.objects.all().filter(evaluated__whoEvaluated=self.request.user, student=thisUserSolution).exists():
            rubricLines = RubricLine.objects.all().filter(evaluated__whoEvaluated=self.request.user, student=
            thisUserSolution).exclude(evaluated__isnull=True).order_by('learningObjective__id', '-evaluated__date').distinct('learningObjective')
            finalRubric = Rubric.objects.all().filter(userSolution=thisUserSolution).filter(evaluator=self.request.user).distinct()
        else:
            rubricLines = RubricLine.objects.filter(student=thisUserSolution).exclude(evaluated__isnull=True).order_by(
                'learningObjective__id', '-evaluated__date').distinct('learningObjective')
            finalRubric = Rubric.objects.all().filter(userSolution=thisUserSolution)

        # set criteriaLines based on whether this is a new evaluation or not
        if CriteriaLine.objects.filter(evaluator__whoEvaluated=self.request.user, userSolution=thisUserSolution).exists():
            print('Found criteriaLines')
            criteriaLines = CriteriaLine.objects.filter(userSolution=thisUserSolution, evaluator__whoEvaluated=self.request.user).order_by(
                'criteria__learningObj__id')
        else:
            print('no criteria lines detected')
            criteriaLines = CriteriaLine.objects.all().filter(userSolution=thisUserSolution).order_by('-criteria_id',
                'criteria__learningObj__id').distinct('criteria_id')

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
                                                                                evaluator__whoEvaluated=self.request.user))
        else:
            print(criteriaLines.count())
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
                if DiscussionBoard.objects.filter(challenge=challenge).exists():
                    print(DiscussionBoard.objects.get(challenge=challenge))
                    context['discussion'] = DiscussionBoard.objects.get(challenge=challenge)
                else:
                    context['discussion'] = ''
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

        if profile.role == 3 or profile.role == 2:
            group = self.request.user.groups.all()
            print(group)
            queryset = UserSolution.objects.filter(userOwner__groups__in=group).filter(
                evaluated__isnull=False).order_by('-id')
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
        elif self.request.user.profile.role == 3 or self.request.user.profile.role == 3:
                group = self.request.user.groups.all()
                you = self.request.user.profile
                print(group)

                # challengeCoachAssigned = UserSolution.objects.all().filter(challengeName__solutionrouter__profile=you).filter(evaluated__isnull=False).distinct()
                # solutionByTopic = UserSolution.objects.all().filter(userOwner__profile__subjectMatter=you.subjectMatter).filter(evaluated__isnull=False).distinct()
                # specificallyAssigned = UserSolution.objects.filter(userOwner__groups__in=group).filter(evaluated__isnull=False).distinct()

                userSolutions = UserSolution.objects.filter(userOwner__groups__in=group)
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

        if UserSolution.objects.filter(coachReview__release=True):
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
            print('Checking for rubricLines')
            rubricLines = RubricLine.objects.all().filter(student=rubric, evaluated__whoEvaluated__profile__role__gte=3).filter(student__coachReview__release=True)
            print(rubricLines.count())
            context['evaluation'] = rubricLines
        context['userRole'] = self.request.user.profile.role

        try:
            context['evalFinalForm'] = Rubric.objects.all().filter(userSolution=rubric, userSolution__coachReview__release=True).last()
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

