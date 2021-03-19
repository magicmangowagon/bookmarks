from django.db import models
from django.contrib.auth.models import User
from djrichtextfield.models import RichTextField
from rubrics.models import Challenge, SolutionInstance, UserSolution, LearningObjective, Evaluated, RubricLine, Rubric, \
    Criterion


# Create your models here.
class BaseUserGeneratedObject(models.Model):
    creator = models.ForeignKey(User, default=None, on_delete=models.CASCADE,
                                related_name='%(class)s_related',
                                related_query_name='%(class)s_related')
    name = models.CharField(default='', max_length=1000)
    creation_date = models.DateTimeField(auto_now_add=True)
    evaluated = models.ForeignKey(Evaluated, null=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class GeneralEvaluation(BaseUserGeneratedObject):
    # competencies = models.ForeignKey(Competency, on_delete=models.CASCADE)
    generalFeedback = RichTextField(blank=True, default='')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    userSolution = models.ForeignKey(UserSolution, on_delete=models.CASCADE, default='0')
    challengeCompletionLevel = models.IntegerField(default=0)


class LoEvaluation(BaseUserGeneratedObject):
    learningObjective = models.ForeignKey(LearningObjective, on_delete=models.CASCADE, default=None)
    generalEval = models.ForeignKey(GeneralEvaluation, on_delete=models.CASCADE, default=None)
    evidenceMissing = RichTextField(blank=True, default='')
    evidencePresent = RichTextField(blank=True, default='')
    feedback = RichTextField(blank=True, default='')
    suggestions = RichTextField(blank=True, default='')
    completionLevel = models.IntegerField(default=0)
    A = 'A'
    B = 'B'
    attentionChoices = (
        ('A', "Yes"),
        ('B', "No")
    )
    needsLaterAttention = models.CharField(max_length=1, choices=attentionChoices, default='B')
    BOOL_CHOICES = (
        (True, "Yes"),
        (False, "No")
    )
    ready = models.BooleanField(default=False)
    ignore = models.BooleanField(choices=BOOL_CHOICES, default=False)

    def __str__(self):
        name = self.creator.__str__() + self.learningObjective.name.__str__()
        return name


class CriteriaEvaluation(BaseUserGeneratedObject):
    criteria = models.ForeignKey(Criterion, on_delete=models.CASCADE)
    loEvaluation = models.ForeignKey(LoEvaluation, on_delete=models.CASCADE, default=None)
    A = 'A'
    B = 'B'
    C = 'C'
    groupLetter = (
        ('0', "--"),
        ('A', "Yes"),
        ('B', "No"),
        ('C', "Evidence for and against")
    )
    achievement = models.CharField(max_length=1, choices=groupLetter, default='')



