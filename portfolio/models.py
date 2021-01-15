from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from djrichtextfield.models import RichTextField
from rubrics.models import Challenge, SolutionInstance, UserSolution, LearningObjective, Evaluated, RubricLine, Rubric


# Create your models here.
class BaseUserGeneratedObject(models.Model):
    creator = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name='creator')
    name = models.CharField(default='', max_length=1000)
    creation_date = models.DateTimeField(auto_now_add=True)
    evaluated = models.ForeignKey(Evaluated, null=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Portfolio(SolutionInstance):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, null=False)


class UserPortfolio(BaseUserGeneratedObject):
    team = models.ManyToManyField(User, blank=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, null=False)
    chosenLearningObjs = models.ManyToManyField(LearningObjective, blank=True)
    link = RichTextField(default='')
    proudDetail = models.TextField('What’s a specific detail in this work that you are especially proud of? why? (*required)', blank=False, default='')
    hardDetail = models.TextField('Which detail shows what was especially hard for you?  how? (*required)', blank=False, default='')
    rubricLines = models.ManyToManyField(RubricLine, blank=True)
    finalRubric = models.ForeignKey(Rubric, null=True, on_delete=models.CASCADE)


class TempUserPortfolio(UserSolution):
    team = models.ManyToManyField(User, null=True)

