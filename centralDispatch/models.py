from django.db import models
from account.models import Profile
from rubrics.models import Challenge, MegaChallenge, UserSolution, RubricLine, Rubric, SolutionInstance
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver


def validate_only_one_instance(obj):
    model = obj.__class__
    if (model.objects.count() > 0 and
            obj.id != model.objects.get().id):
        raise ValidationError("Can only create 1 %s instance" % model.__name__)


class SolutionRouter(models.Model):
    name = models.CharField(blank=True, max_length=500)
    profile = models.ForeignKey(Profile, blank=True, default='', on_delete=models.CASCADE, null=True)
    challenge = models.ManyToManyField(Challenge, blank=True, default='')
    solutionInstance = models.ForeignKey(SolutionInstance, blank=True, default='', on_delete=models.CASCADE)
    automate = models.BooleanField(default=False)
    routerChoices = models.IntegerField(choices=(
                                        (1, "Subject Matter"),
                                        (2, "Challenge Specific"),
                                        (3, "Manually Assign"),
                                        (4, "Legacy Challenge"),
                                        ), null=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=SolutionInstance, dispatch_uid=str(SolutionInstance))
def create_solution_router(sender, **kwargs):
    if kwargs.get('created', False):
        # challenge = sender.challenge_that_owns_me
        SolutionRouter.objects.create(solutionInstance=kwargs['instance'], name=(str(kwargs['instance'].name + ' router')))

        # i.challenge.set(challenge)
        # i.save()


class ManualAssignmentKeeper(models.Model):
    profile = models.ForeignKey(Profile, blank=True, default='', on_delete=models.PROTECT)
    userSolution = models.ManyToManyField(UserSolution, blank=True, default='')
