from django.db import models
from rubrics.models import Challenge, MegaChallenge, UserSolution, RubricLine, Rubric
from django.core.exceptions import ValidationError


def validate_only_one_instance(obj):
    model = obj.__class__
    if (model.objects.count() > 0 and
            obj.id != model.objects.get().id):
        raise ValidationError("Can only create 1 %s instance" % model.__name__)

