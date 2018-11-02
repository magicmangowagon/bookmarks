from django.db import models


class LearningObjective(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()

