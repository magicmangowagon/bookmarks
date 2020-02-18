from django.db import models
from django.contrib.auth.models import User, Group
from djrichtextfield.models import RichTextField
from taggit.managers import TaggableManager
from datetime import datetime
from rubrics.models import Challenge, LearningExperience, Evaluated

# Create your models here.


# BASE INFO MODEL
class BaseInfo(models.Model):
    title = models.CharField(max_length=600)
    mainText = RichTextField()
    dateCreated = models.DateTimeField(auto_now=True)
    occurrenceDate = models.DateTimeField(default=datetime.now())
    learningExpos = models.ManyToManyField(LearningExperience, blank=True)
