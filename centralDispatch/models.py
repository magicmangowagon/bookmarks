from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from account.models import Profile
from rubrics.models import Challenge, MegaChallenge, UserSolution, RubricLine, Rubric, SolutionInstance, LearningExperience
# from .functions import htmlMessage
from info.models import BaseInfo
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
                                  limit_choices_to=Q(role=2) | Q(role=3) | Q(role=4))
    coach = models.ForeignKey(Profile, null=True, on_delete=models.PROTECT, related_name='coach', blank=True,
                              limit_choices_to=Q(role=2) | Q(role=3) | Q(role=4))
    userSolution = models.ForeignKey(UserSolution, blank=True, default='', on_delete=models.CASCADE)

    def __str__(self):
        return self.userSolution.__str__()


# tracks submission and subsequent updates to user solutions by TC
class SomethingHappened(models.Model):
    time = ArrayField(models.DateTimeField(), default=list)
    userSolution = models.ForeignKey(UserSolution, on_delete=models.SET_NULL, null=True, default='')
    archivedName = models.CharField(max_length=1000, default='')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, null=True)
    modCount = models.IntegerField(default=0)

    def __str__(self):
        return self.userSolution.__str__()

    def save(self, *args, **kwargs):
        self.modCount += 1
        return super(SomethingHappened, self).save(*args, **kwargs)


class SolutionStatus(models.Model):
    solutionSubmitted = models.BooleanField(default=False, verbose_name='Submitted')
    solutionEvaluated = models.BooleanField(default=False, verbose_name='Evaluated')
    solutionCoachReviewed = models.BooleanField(default=False, verbose_name='Coach Reviewed')
    solutionRejected = models.BooleanField(default=False, verbose_name='Needs Revision')
    solutionCompleted = models.BooleanField(default=False, verbose_name='Completed')
    userSolution = models.ForeignKey(UserSolution, null=True, default='', on_delete=models.CASCADE)
    solutionInstance = models.ForeignKey(SolutionInstance, default='', on_delete=models.PROTECT, null=True)
    returnTo = models.ForeignKey(User, null=True, default='', blank=True, on_delete=models.CASCADE, limit_choices_to=models.Q(profile__role__gte=2))

    def __str__(self):
        if self.solutionInstance:
            try:
                return self.challengestatus.first().user.__str__() + ' ' + self.solutionInstance.__str__() + ' status'
            except:
                return ' status'
        else:
            return self.userSolution.__str__() + ' status'

    def get_somethingHappened(self):
        somethingHappened = SomethingHappened.objects.get(userSolution=self.userSolution)
        return somethingHappened


class ChallengeStatus(models.Model):
    challengeAccepted = models.BooleanField(default=False)
    challenge = models.ForeignKey(Challenge, default='', on_delete=models.CASCADE)
    user = models.ForeignKey(User, default='', on_delete=models.CASCADE)
    solutionStatusByInstance = models.ManyToManyField(SolutionStatus, blank=True, default='', related_name='challengestatus')
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.challenge.name + ' ' + self.user.__str__()


class StudioExpoChoice(models.Model):
    date = models.DateField(auto_now=True)
    user = models.ForeignKey(User, null=False, default='', on_delete=models.CASCADE)
    learningExpoChoice = models.ForeignKey(LearningExperience, null=True, default='', on_delete=models.CASCADE)
    session = models.ForeignKey(BaseInfo, null=False, default='', on_delete=models.CASCADE)


class EmailEvent(models.Model):
    event = models.CharField(max_length=200, default='')
    urlPath = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.event


class EmailMessage(models.Model):
    body = models.TextField(default='')
    name = models.CharField(max_length=200, default='')
    solutionInstance = models.ForeignKey(SolutionInstance, default='', null=True, on_delete=models.CASCADE)
    event = models.ForeignKey(EmailEvent, default='', null=True, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=UserSolution, dispatch_uid=str(UserSolution) + str(datetime.now()))
def create_assignment_tracking_models(sender, **kwargs):
    if kwargs.get('created', False):
        AssignmentKeeper.objects.create(userSolution=kwargs['instance'], )
        try:
            print('got challenge status')
            challengeStatus = ChallengeStatus.objects.get(challenge=kwargs['instance'].challengeName, user=kwargs['instance'].userOwner)
        except ChallengeStatus.DoesNotExist:
            print('created challenge status')
            challengeStatus = ChallengeStatus.objects.create(challenge=kwargs['instance'].challengeName, user=kwargs['instance'].userOwner)
        # what the fuck is going on here! Clean this up, figure out how to call this
        if SolutionStatus.objects.filter(solutionInstance=kwargs['instance'].solutionInstance,
                                         userSolution=kwargs['instance']).exists():
            print('found solution status object' + str(kwargs['instance'].solutionInstance))
            s = SolutionStatus.objects.get(solutionInstance=kwargs['instance'].solutionInstance, userSolution=kwargs['instance'])
            s.userSolution = kwargs['instance']
            s.solutionInstance = kwargs['instance'].solutionInstance
            s.solutionSubmitted = True
            s.save()
        else:
            s = SolutionStatus.objects.create(userSolution=kwargs['instance'], solutionSubmitted=True,
                                              solutionInstance=kwargs['instance'].solutionInstance)
            challengeStatus.solutionStatusByInstance.add(s)
            challengeStatus.save()


@receiver(post_save, sender=ChallengeStatus, dispatch_uid=str(ChallengeStatus.challenge) + str(ChallengeStatus.user))
def create_complete_assignment_tracking_stack(sender, **kwargs):
    if kwargs.get('created', False):

        for solutionInstance in kwargs['instance'].challenge.solutions.all():

            # No idea what I'm doing here. Just want to check if a solution exists for this instance before
            # generating a solution status, 06/17/2020, highly distracted by non work things...
            if kwargs['instance'].solutionStatusByInstance.filter(solutionInstance=solutionInstance).exists():
                print('solution status already exists')
            else:
                print('inside existence check')
                s = SolutionStatus.objects.create(solutionInstance=solutionInstance)
                kwargs['instance'].solutionStatusByInstance.add(s)
                kwargs['instance'].save()


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


@receiver(post_save, sender=Rubric, dispatch_uid=str(Rubric) + str(datetime.now()))
def update_solution_status(sender, **kwargs):
    assignmentKeeper = AssignmentKeeper.objects.get(userSolution=kwargs['instance'].userSolution)
    # print(str(assignmentKeeper) + 'fart')
    if kwargs.get('created', False):
        try:
            solutionStatus = SolutionStatus.objects.get(userSolution=kwargs['instance'].userSolution)
        except SolutionStatus.DoesNotExist:
            solutionStatus = SolutionStatus.objects.create(userSolution=kwargs['instance'].userSolution,
                                                           solutionInstance=kwargs['instance'].userSolution.solutionInstance)
            challengeStatus = ChallengeStatus.objects.get(challenge=kwargs['instance'].challenge, user=kwargs['instance'].userSolution.userOwner)
            challengeStatus.solutionStatusByInstance.add(solutionStatus)
            challengeStatus.save()
        print(assignmentKeeper.evaluator, kwargs['instance'].evaluator.profile)

        if (kwargs['instance'].evaluator.profile.role == 2) or (kwargs['instance'].evaluator.profile == assignmentKeeper.evaluator):
            solutionStatus.solutionEvaluated = True
            solutionStatus.save()
        if (kwargs['instance'].evaluator.profile.role >= 3) and \
                (kwargs['instance'].evaluator.profile != assignmentKeeper.evaluator):
            solutionStatus.solutionCoachReviewed = True
            solutionStatus.save()



