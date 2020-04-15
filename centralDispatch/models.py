from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from account.models import Profile
from rubrics.models import Challenge, MegaChallenge, UserSolution, RubricLine, Rubric, SolutionInstance
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db.models import Q
from datetime import datetime


def validate_only_one_instance(obj):
    model = obj.__class__
    if (model.objects.count() > 0 and
            obj.id != model.objects.get().id):
        raise ValidationError("Can only create 1 %s instance" % model.__name__)


class SolutionRouter(models.Model):
    name = models.CharField(blank=True, max_length=500)
    coach = models.ForeignKey(Profile, blank=True, default='', on_delete=models.CASCADE, null=True)
    challenge = models.ManyToManyField(Challenge, blank=True, default='')
    solutionInstance = models.ForeignKey(SolutionInstance, blank=True, default='', on_delete=models.CASCADE, null=True)
    automate = models.BooleanField(default=False)
    routerChoices = models.IntegerField(choices=(
                                        (1, "Subject Matter"),
                                        (2, "Challenge Specific"),
                                        (3, "Manually Assign"),
                                        (4, "Legacy Challenge"),
                                        ), null=True, blank=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=SolutionInstance, dispatch_uid=str(SolutionInstance))
def create_solution_router(sender, **kwargs):
    if kwargs.get('created', False):
        SolutionRouter.objects.create(solutionInstance=kwargs['instance'],
                                      name=(str(kwargs['instance'].name + ' router')))


# Generated on Solution submission. Reviews are manually assigned by admin at the moment
class AssignmentKeeper(models.Model):
    evaluator = models.ForeignKey(Profile, null=True, on_delete=models.PROTECT, related_name='evaluator', blank=True,
                                  limit_choices_to=Q(role=2) | Q(role=3))
    coach = models.ForeignKey(Profile, null=True, on_delete=models.PROTECT, related_name='coach', blank=True,
                              limit_choices_to=Q(role=2) | Q(role=3))
    userSolution = models.ForeignKey(UserSolution, blank=True, default='', on_delete=models.CASCADE)

    def __str__(self):
        return self.userSolution.__str__()


@receiver(post_save, sender=UserSolution, dispatch_uid=str(UserSolution))
def create_assignment_keeper(sender, **kwargs):
    if kwargs.get('created', False):
        AssignmentKeeper.objects.create(userSolution=kwargs['instance'], )


class SomethingHappened(models.Model):
    time = ArrayField(models.DateTimeField(), default=list)
    userSolution = models.ForeignKey(UserSolution, on_delete=models.SET_NULL, null=True, default='')
    archivedName = models.CharField(max_length=1000, default='')

    def __str__(self):
        return self.userSolution.__str__()


@receiver(post_save, sender=UserSolution, dispatch_uid=str(UserSolution) + str(datetime.now()))
def create_something_happened(sender, **kwargs):
    if kwargs.get('created', False):
        sh = SomethingHappened.objects.create(
            userSolution=kwargs['instance'],
            archivedName=str(kwargs['instance'],)
        )
        sh.time.append(datetime.now())
        sh.save()


@receiver(post_save, sender=UserSolution, dispatch_uid=str(UserSolution) + str(datetime.now()) + 'update')
def update_something_happened(sender, **kwargs):
    if kwargs.get('created', True):
        if SomethingHappened.objects.filter(userSolution=kwargs['instance']).exists():
            sh = SomethingHappened.objects.get(userSolution=kwargs['instance'])
            sh.time.append(datetime.now())
            sh.save()
        else:
            sh = SomethingHappened.objects.create(
                userSolution=kwargs['instance'],
                archivedName=str(kwargs['instance'], )
            )
            sh.time.append(datetime.now())
            sh.save()


