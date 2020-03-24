from django.db import models
from account.models import Profile
from rubrics.models import Challenge, MegaChallenge, UserSolution, RubricLine, Rubric
from django.core.exceptions import ValidationError


def validate_only_one_instance(obj):
    model = obj.__class__
    if (model.objects.count() > 0 and
            obj.id != model.objects.get().id):
        raise ValidationError("Can only create 1 %s instance" % model.__name__)


class SolutionRouter(models.Model):
    profile = models.ForeignKey(Profile, blank=True, default='', on_delete=models.CASCADE)
    challenge = models.ManyToManyField(Challenge, blank=True, default='')
    automate = models.BooleanField(default=False)

