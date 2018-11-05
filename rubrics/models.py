from django.db import models
from django.contrib.auth.models import User


class Competency(models.Model):
    name = models.CharField(max_length=250)
    # learningObjs = models.ForeignKey(LearningObjective, on_delete=models.CASCADE)


class LearningObjective(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    competency = models.ForeignKey(Competency, on_delete=models.CASCADE)


class Criterion(models.Model):
    name = models.CharField(max_length=250)
    learningObj = models.ForeignKey(LearningObjective, on_delete=models.CASCADE)


class Challenge(models.Model):
    name = models.CharField(max_length=250)
    competencies = models.ForeignKey(Competency, on_delete=models.CASCADE)


class Rubric(models.Model):
    competencies = models.ForeignKey(Competency, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    evidenceMissing = models.TextField()
    evidencePresent = models.TextField()
    feedback = models.TextField()
    completionLevel = models.IntegerField()




