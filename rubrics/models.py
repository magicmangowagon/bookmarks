from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField


# Many-to-many with, connected to competencies and challenges
class LearningObjective(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    # challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Challenge(models.Model):
    name = models.CharField(max_length=250)
    # competencies = models.ForeignKey(Competency, on_delete=models.CASCADE)
    description = HTMLField()
    learningObjs = models.ManyToManyField(LearningObjective, blank=True)

    def __str__(self):
        return self.name


# Unsure, might be a one-to-many with LO's in it's bucket. Not sure if it needs to be
# controlled by the Challenge model
class Competency(models.Model):
    name = models.CharField(max_length=250)
    # challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.name


# One-to-many with their parent LO
class Criterion(models.Model):
    name = models.CharField(max_length=250)
    learningObj = models.ForeignKey(LearningObjective, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Rubric(models.Model):
    competencies = models.ForeignKey(Competency, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    evidenceMissing = models.TextField()
    evidencePresent = models.TextField()
    feedback = models.TextField()
    completionLevel = models.IntegerField()




