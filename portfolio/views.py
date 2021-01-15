from django.shortcuts import render, redirect
from django.forms import modelformset_factory, forms
from .models import Portfolio, UserPortfolio
from rubrics.forms import CoachReviewFormset, RubricLineFormset, CriterionFormSet, RubricLineForm, RubricForm, CriteriaForm
from rubrics.models import Evaluated, RubricLine, Rubric, CriteriaLine, Criterion, LearningObjective
from django.views.generic import ListView, DetailView, FormView
from .forms import UserPortfolioForm
from django.contrib import messages
# Create your views here.


class PortfolioUploadView(FormView):
    form_class = UserPortfolioForm
    template_name = 'portfolioUpload.html'
    model = Portfolio

    def get_form_kwargs(self, **kwargs):
        kwargs = super(PortfolioUploadView, self).get_form_kwargs()
        kwargs['portfolio'] = Portfolio.objects.get(id=self.kwargs['pk'])

        return kwargs

    def get_initial(self, **kwargs):
        initial = super(PortfolioUploadView, self).get_initial()
        portfolio = Portfolio.objects.get(id=self.kwargs['pk'])
        if UserPortfolio.objects.filter(creator=self.request.user, portfolio=portfolio).exists():
            instance = UserPortfolio.objects.get(creator=self.request.user, portfolio=portfolio)
            # initial = UserPortfolioForm(portfolio, instance=instance)
            initial['chosenLearningObjs'] = instance.chosenLearningObjs.all()
            initial['link'] = instance.link
            initial['hardDetail'] = instance.hardDetail

            initial['proudDetail'] = instance.proudDetail
            initial['creator'] = self.request.user
            initial['portfolio'] = portfolio
        else:
            initial['creator'] = self.request.user
            initial['portfolio'] = portfolio
        return initial

    def get_context_data(self, **kwargs):
        context = super(PortfolioUploadView, self).get_context_data(**kwargs)
        portfolio = Portfolio.objects.get(id=self.kwargs['pk'])
        context['portfolioForm'] = UserPortfolioForm(portfolio=portfolio, initial={'creator': self.request.user, 'portfolio': portfolio})
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            portfolio = Portfolio.objects.get(id=self.kwargs['pk'])
            if UserPortfolio.objects.filter(creator=self.request.user, portfolio=portfolio).exists():
                instance = UserPortfolio.objects.get(creator=self.request.user, portfolio=portfolio)
                form = UserPortfolioForm(portfolio, request.POST, instance=instance)
            else:
                form = UserPortfolioForm(portfolio, request.POST)
            if form.is_valid():
                form.save()
                return redirect('eval-list')
            else:
                print(form.errors)
                return redirect('portfolioUpload.html')
        return render(request, self.get_template_names())


class PortfolioListView(ListView):
    model = UserPortfolio
    queryset = UserPortfolio.objects.all()
    template_name = 'portfoliolist.html'


class UserPortfolioDetailView(FormView):
    model = UserPortfolio
    template_name = 'rubrics/coachingreview.html'
    form_class = CoachReviewFormset

    def get_context_data(self, **kwargs):
        context = super(UserPortfolioDetailView, self).get_context_data()
        userSolution = self.kwargs['pk']
        thisUserSolution = UserPortfolio.objects.get(pk=userSolution)

        challenge = UserPortfolio.objects.get(pk=userSolution).portfolio
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


