from django.db import models
from django.contrib.auth.models import User
from djrichtextfield.models import RichTextField
from tinymce import models as tinymce_models


# __________________
# LEARNING OBJECTIVE
# they are the source of everything. TCs are assessed on mastery of competency that is comprised of Learning Objectives.
# They are the objects that make up a Challenge. rubricLines, the stores of user answers are tied to them.

class LearningObjective(models.Model):
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
    name = models.CharField(max_length=250)

    def __str__(self):
        fullname = str(self.compGroup) + "-" + str(self.compNumber) + "." + str(self.loNumber) + " " + str(self.name)
        return fullname


# __________
# CHALLENGES
# Works as the main/only way to organize learningObjectives and therefore rubricLines for TC completion.
# This is how users do things

class Challenge(models.Model):

    name = models.CharField(max_length=250)
    description = RichTextField()
    learningObjs = models.ManyToManyField(LearningObjective, blank=True)

    def __str__(self):
        return self.name


# __________
# COMPETENCY

class Competency(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    learningObjs = models.ForeignKey(LearningObjective, blank=True, null=True, on_delete=models.CASCADE)

    # may want to store something called hasCompleted, and/or hasCompletedPreviously
    # if competence is based on mastery of learningObjectives, does that assessment ever change?
    # re-score of a challenge solution could lead to mastery being removed, we should track if that happens

    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'
    groupLetter = (
        ('A', "A"),
        ('B', "B"),
        ('C', "C"),
        ('D', "D"),
        ("E", "E"),
        ('F', "F")
    )
    compGroup = models.CharField(max_length=1, choices=groupLetter, default=A)
    compNumber = models.IntegerField(choices=(
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
        (6, "6"),
        (7, "7")
    ))

    def __str__(self):
        return self.name


# _________
# CRITERION
# One-to-many with their parent LO

class Criterion(models.Model):
    name = models.CharField(max_length=250)
    learningObj = models.ForeignKey(LearningObjective, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# _____________
# USER SOLUTION
# The connector of the TC submitted work with the admin defined objects.
# Uploaded by a TC in response to a challenge and assessed with rubricLines
# dictated by learningObjectives attached to the Challenge

class UserSolution(models.Model):
    file = models.FileField(upload_to='uploads/', blank=True)
    solution = tinymce_models.HTMLField()
    userOwner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    challengeName = models.ForeignKey(Challenge, blank=True, null=True, on_delete=models.CASCADE)


# ___________
# RUBRIC LINE
# Evaluator submitted response to learningObjectives

class RubricLine(models.Model):
    evidenceMissing = models.TextField(blank=True, default='')
    evidencePresent = models.TextField(blank=True, default='')
    feedback = models.TextField(blank=True, default='')
    suggestions = models.TextField(blank=True, default='')
    completionLevel = models.IntegerField(default=0)
    student = models.ForeignKey(UserSolution, on_delete=models.CASCADE)
    learningObjective = models.ForeignKey(LearningObjective, on_delete=models.CASCADE)
    A = 'A'
    B = 'B'
    attentionChoices = (
        ('A', "Yes"),
        ('B', "No")
    )
    needsLaterAttention = models.CharField(max_length=1, choices=attentionChoices, default='B')
    # ready = models.BooleanField(default=False)


# _____________
# CRITERIA LINE
# An attempt to model a sub-learningObjective for each learningObjective on the rubricLine relationship
# to the learningObjective used for the next level of granularity up.

class CriteriaLine(models.Model):
    criteria = models.ForeignKey(Criterion, on_delete=models.CASCADE)
    # rubricLine = models.ForeignKey(RubricLine, on_delete=models.CASCADE)
    userSolution = models.ForeignKey(UserSolution, on_delete=models.CASCADE)
    A = 'A'
    B = 'B'
    C = 'C'
    groupLetter = (
        ('A', "Yes"),
        ('B', "No"),
        ('C', "Evidence for and against")
    )
    achievement = models.CharField(max_length=1, choices=groupLetter, default='')


# _________
# RUBRIC
# Named for the app and one of the simpler models. Stores the generalFeedback for a userSolution, as well
# as the completionScore for the challenge.

class Rubric(models.Model):
    # competencies = models.ForeignKey(Competency, on_delete=models.CASCADE)
    generalFeedback = models.TextField(blank=True, default='')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE)
    userSolution = models.ForeignKey(UserSolution, on_delete=models.CASCADE, default='0')
    challengeCompletionLevel = models.IntegerField(default=0)





