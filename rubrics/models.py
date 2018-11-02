from django.db import models


class Criterion(models.Model):
    name = models.CharField(max_length=250)


class LearningObjective(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    criteria = models.ForeignKey(Criterion, on_delete=models.CASCADE)



