from django.db import models
from rubrics.models import Challenge, MegaChallenge
from django.core.exceptions import ValidationError


def validate_only_one_instance(obj):
    model = obj.__class__
    if (model.objects.count() > 0 and
            obj.id != model.objects.get().id):
        raise ValidationError("Can only create 1 %s instance" % model.__name__)


# Create your models here.
class ChallengeListSort(models.Model):
    replaceChallengesMega = models.BooleanField(default=False)

    def clean(self):
        validate_only_one_instance(self)
