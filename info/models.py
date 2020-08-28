from django.db import models
from django.contrib.auth.models import User, Group
from djrichtextfield.models import RichTextField
from taggit.managers import TaggableManager
from datetime import datetime
from rubrics.models import Challenge, LearningExperience, Evaluated
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save


# Categories for posts
class InfoCategory(models.Model):
    infoClass = models.CharField(max_length=600)

    def __str__(self):
        return self.infoClass


# BASE INFO MODEL
class BaseInfo(models.Model):
    title = models.CharField(max_length=600)
    mainText = RichTextField()
    dateCreated = models.DateTimeField(auto_now=True)
    occurrenceDate = models.DateTimeField(default=datetime.now())
    learningExpos = models.ManyToManyField(LearningExperience, blank=True)
    category = models.ManyToManyField(InfoCategory, blank=True)

    def get_absolute_url(self):
        return reverse('infodetail', args=(self.id,))

    def __str__(self):
        return self.title


class DiscussionBoard(models.Model):
    challenge = models.ForeignKey(Challenge, default='', null=False, on_delete=models.PROTECT)
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
