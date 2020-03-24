from django import forms
from django.forms import modelformset_factory, BaseModelFormSet
from rubrics.models import Challenge, UserSolution, Rubric, RubricLine, CriteriaLine, \
    ChallengeAddendum, LearningExperience, LearningExpoResponses, CoachReview
from .models import SolutionRouter, ManualAssignmentKeeper
from django.contrib.auth.models import User

# create form for router, then a form for manual assignment. Going to have to dig into AJAX to make this work
# smoothly for Hannah.