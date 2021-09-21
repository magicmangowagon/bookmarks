from django.db import models
from django.contrib.auth.models import User, Group
from djrichtextfield.models import RichTextField
from taggit.managers import TaggableManager
from datetime import datetime
from rubrics.models import Challenge, LearningExperience, Evaluated
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.serializers import json, serialize


# Categories for posts
class InfoCategory(models.Model):
    infoClass = models.CharField(max_length=600)

    def __str__(self):
        return self.infoClass


class Prompts(models.Model):
    question = models.CharField(max_length=500, default='', blank=True)
    response = RichTextField()


# BASE INFO MODEL
class BaseInfo(models.Model):
    title = models.CharField(max_length=600)
    mainText = RichTextField()
    prompts = models.ManyToManyField(Prompts, blank=True)
    dateCreated = models.DateTimeField(auto_now=True)
    occurrenceDate = models.DateTimeField(default=datetime.now())
    learningExpos = models.ManyToManyField(LearningExperience, blank=True)
    category = models.ManyToManyField(InfoCategory, blank=True)

    def get_absolute_url(self):
        return reverse('infodetail', args=(self.id,))

    def __str__(self):
        return self.title


class DiscussionBoard(models.Model):
    challenge = models.ForeignKey(Challenge, default='', null=False, on_delete=models.CASCADE)
    description = RichTextField(default='')

    def get_absolute_url(self):
        return reverse('discussion-board', args=(self.id, ))

    def __str__(self):
        return self.challenge.name + ' discussion'


class DiscussionTopic(models.Model):
    title = models.CharField(max_length=500, default='', blank=False)
    creationDate = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, default='', blank=False, on_delete=models.CASCADE)
    description = RichTextField(default='')
    board = models.ForeignKey(DiscussionBoard, null=False, on_delete=models.CASCADE, default='')

    def get_absolute_url(self):
        return reverse('discussion-topic', args=(self.id, ))

    def __str__(self):
        return self.title


@receiver(post_save, sender=Challenge, dispatch_uid=str(Challenge))
def create_discussion_board(sender, **kwargs):
    if kwargs.get('created', False):
        DiscussionBoard.objects.create(challenge=kwargs['instance'])


class QuestionStub(models.Model):
    question = models.CharField(max_length=1000, default='')
    custom = models.CharField(max_length=1000, blank=True, default='')

    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'

    compGroupChoices = (
        ('A', "Elicit"),
        ('B', "Go Deeper"),
        ('C', "Step Back"),
        ('D', "Take Action"),

    )
    questionCategory = models.CharField(max_length=1, choices=compGroupChoices, default=A)

    def __str__(self):
        return self.question


class FakeLO(models.Model):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'

    compGroupChoices = (
        ('A', "A"),
        ('B', "B"),
        ('C', "C"),
        ('D', "D"),
        ("E", "E"),
        ('F', "F")
    )
    compGroup = models.CharField(max_length=1, choices=compGroupChoices, default=A)
    compNumber = models.IntegerField(choices=(
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
        (6, "6"),
        (7, "7")
    ))
    loNumber = models.IntegerField(choices=(
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
        (6, "6"),
        (7, "7"),
        (8, "8")
    ))
    name = models.TextField(blank=True, default='')
    tags = TaggableManager(blank=True)
    archive = models.BooleanField('Archive (hides LO)', default=False)
    questionGroup = models.ManyToManyField(QuestionStub, blank=True)

    def get_questions(self):
        return serialize('json', self.questionGroup.all())

    def __str__(self):
        return self.name


class CommentContainer(models.Model):
    comment = models.ForeignKey(QuestionStub, blank=True, default='', on_delete=models.CASCADE)
    baseInfo = models.ForeignKey(BaseInfo, blank=True, default='', on_delete=models.CASCADE)
    coordinates = models.IntegerField(blank=True, default=0)


class FakeCompetency(models.Model):
    fakeLos = models.ManyToManyField(FakeLO, blank=True)
    name = models.CharField(max_length=400, blank=True, default='')

    def get_los(self):
        return serialize('json', self.fakeLos.all())

    def __str__(self):
        return self.name
