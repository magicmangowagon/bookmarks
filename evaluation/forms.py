from django import forms
from django.forms import modelformset_factory, BaseModelFormSet, BaseInlineFormSet, inlineformset_factory
from django.contrib.auth.models import User
from .models import GeneralEvaluation, LoEvaluation, CriteriaEvaluation


CritFormset = inlineformset_factory(
    LoEvaluation,
    CriteriaEvaluation,
    fields=('criteria', 'achievement'),
    extra=1
)


class BaseLoEvaluationWithCritFormset(BaseInlineFormSet):
    def add_fields(self, form, index):
        form.nested = CritFormset(
            instance=form.instance,
            data=form.data
        )


GeneralEvaluationInlineFormset = inlineformset_factory(
    GeneralEvaluation,
    LoEvaluation,
    formset=BaseLoEvaluationWithCritFormset,
    fields=('evidencePresent', 'evidenceMissing', 'feedback', 'suggestions'),
    extra=1
)


