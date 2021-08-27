from django.db import models
from django.contrib.auth.models import User, Group
from djrichtextfield.models import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from datetime import datetime
from django.core.files.base import ContentFile
from zipfile import ZipFile
# import boto3
# from io import BytesIO
import os
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


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
    name = models.TextField(blank=True, default='')
    tags = TaggableManager(blank=True)
    archive = models.BooleanField('Archive (hides LO)', default=False)
    pass

    def __str__(self):
        fullname = str(self.compGroup) + "-" + str(self.compNumber) + "." + str(self.loNumber) + " " + str(self.name)
        return fullname

    class Meta:
        ordering = ['compGroup', 'compNumber', 'loNumber']

    def return_all_criterion(self):
        return Criterion.objects.filter(learningObj=self)


# __________
# CHALLENGES
# Works as the main/only way to organize learningObjectives and therefore rubricLines for TC completion.
# This is how users do things
# _________________
# SOLUTION INSTANCE
class SolutionInstance(models.Model):
    # solution = models.ForeignKey(UserSolution, blank=True, null=True, on_delete=models.CASCADE)
    name = models.TextField(blank=True, default='')
    learningObjectives = models.ManyToManyField(LearningObjective, blank=True)
    prompt = RichTextField('Solution Prompt', default='')
    DESIGN = models.BooleanField(verbose_name='Design', default=False)
    SIMULATE = models.BooleanField(verbose_name='Simulate', default=False)
    IMPLEMENT = models.BooleanField(verbose_name='Implement', default=False)
    specialized = models.CharField(default='', max_length=20, blank=True)

    degreeImplementation = [DESIGN, SIMULATE, IMPLEMENT]

    ONEONONE = models.BooleanField(verbose_name='One on One', default=False)
    SMALLGROUP = models.BooleanField(verbose_name='Small Group', default=False)
    FULLCLASS = models.BooleanField(verbose_name='Full Class', default=False)

    scaleImplementation = [ONEONONE, SMALLGROUP, FULLCLASS]

    REFLECTION = models.BooleanField(verbose_name='Reflection', default=False)
    CLASSROOMEVIDENCE = models.BooleanField(verbose_name='Classroom Evidence', default=False)
    OBSERVATION = models.BooleanField(verbose_name='Observation', default=False)
    order = models.PositiveIntegerField(default=0, blank=True)
    typeImplementation = [REFLECTION, CLASSROOMEVIDENCE, OBSERVATION]

    def __str__(self):
        return self.name


# MEGACHALLENGE - Ties multiple challenges into one
class MegaChallenge(models.Model):
    name = models.CharField(default='', max_length=500)
    display = models.BooleanField('Show Challenge', default=True)
    collapse = models.BooleanField(default=False, verbose_name='Collapse sub challenges')
    solutions = models.ManyToManyField(SolutionInstance, blank=True, related_name="mega_challenge_that_owns_me")
    overRide = models.BooleanField(default=False)
    description = RichTextUploadingField('Challenge Overview', default='', blank=True)
    clinicalNeeds = RichTextField('Clinical Needs', default='', blank=True)
    standardSolution = RichTextField('Standard Solution', default='', blank=True)
    pullQuote = models.CharField('Pull Quote', max_length=1000, default='', blank=True)
    drivingQ = RichTextUploadingField(verbose_name='Driving Questions', default='', blank=True)
    soldThemes = RichTextUploadingField('SoLD Themes', default='', blank=True)
    tfjFocus = RichTextUploadingField('Teaching for Justice Focus', default='', blank=True)
    picture = models.ImageField(upload_to='uploads/challenges/', blank=True, height_field='height', default='')
    height = models.IntegerField(default=0, blank=True)
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    group = [
        (A, 'A'),
        (B, 'B'),
        (C, 'C'),
        (D, 'D')
    ]
    challengeGroupChoices = models.CharField(
        'Challenge Group',
        max_length=2,
        choices=group,
        default=''
    )
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta(object):
        ordering = ['my_order', ]

    def __str__(self):
        return self.name

    def return_all_learningObjectives(self):
        learningObjectives = LearningObjective.objects.filter(challenge__megaChallenge=self).order_by(
            'compGroup', 'compNumber', 'loNumber').distinct('compGroup', 'compNumber', 'loNumber').filter(archive=False)
        return learningObjectives


class Challenge(models.Model):
    name = models.CharField(max_length=250)
    display = models.BooleanField('Show Challenge', default=True)
    description = RichTextUploadingField('Challenge Overview', )
    clinicalNeeds = RichTextField('Clinical Needs', default='')
    standardSolution = RichTextField('Standard Solution', default='')
    pullQuote = models.CharField('Pull Quote', max_length=1000, default='')

    megaChallenge = models.ForeignKey(MegaChallenge, null=True, on_delete=models.CASCADE, blank=True)
    picture = models.ImageField(upload_to='uploads/challenges/', blank=True, height_field='height', default='')
    height = models.IntegerField(default=0)
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    group = [
        (A, 'A'),
        (B, 'B'),
        (C, 'C'),
        (D, 'D')
    ]
    challengeGroupChoices = models.CharField(
        'Challenge Group',
        max_length=2,
        choices=group,
        default=''
    )

    solutions = models.ManyToManyField(SolutionInstance, blank=True, related_name="challenge_that_owns_me", )
    learningObjs = models.ManyToManyField(LearningObjective, blank=True, related_name="challenge")
    tags = TaggableManager(blank=True)
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ['my_order', ]

    def __str__(self):
        return self.name


# __________
# CHALLENGE/SOLUTION INSTANCE JUNCTION MODEL
# Allows sorting of solution instance order in admin

class ChallengeSolutionJunction(models.Model):
    challenge = models.ForeignKey(Challenge, blank=True, on_delete=models.CASCADE)
    solutionInstance = models.ForeignKey(SolutionInstance, blank=True, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ('order',)


# __________
# LEARNING EXPERIENCE

class LearningExperience(models.Model):
    name = models.CharField(max_length=600)
    challenge = models.ForeignKey(Challenge, blank=True, on_delete=models.CASCADE)
    learningObjectives = models.ManyToManyField(LearningObjective, blank=True, related_name="learningExpo")
    index = models.IntegerField('Index', default=0)
    description = RichTextUploadingField(default='')
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ['index', ]

    def __str__(self):
        return self.name


# __________
# CHALLENGE RESOURCES
# holds zip file of challenge resources, separate file class handles each individual file

class ChallengeResources(models.Model):
    challenge = models.ForeignKey(Challenge, blank=True, null=True, on_delete=models.SET_NULL)
    megaChallenge = models.ForeignKey(MegaChallenge, blank=True, null=True, on_delete=models.SET_NULL)
    learningExperience = models.ManyToManyField(LearningExperience, blank=True)
    fileContainer = models.FileField(upload_to='resources/', default='', blank=True)
    name = models.CharField(max_length=500, null=True, blank=True)
    description = RichTextField(blank=True, default='')

    def save(self, delete_zipFile=False, *args, **kwargs):
        super(ChallengeResources, self).save(*args, **kwargs)
        with ZipFile(self.fileContainer, 'r') as resource:
            for name in resource.namelist():
                current_file = resource.open(name)
                f = ChallengeResourcesFile(challengeResources=self)
                f.file.save(current_file.name, ContentFile(current_file.read()))


class ChallengeResourcesFile(models.Model):
    challengeResources = models.ForeignKey(ChallengeResources, related_name='resource_file', on_delete=models.CASCADE, default='', blank=True)
    file = models.FileField(max_length=200, upload_to='resources/')
    order = models.PositiveIntegerField(default=0, blank=False, null=True)

    class Meta:
        ordering = ['order', ]

    @property
    def filename(self):
        return os.path.basename(self.file.name)


# __________
# COMPETENCY

class Competency(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    learningObjs = models.ManyToManyField(LearningObjective, blank=True)
    tags = TaggableManager(blank=True)
    archive = models.BooleanField(default=False)
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
    learningObj = models.ForeignKey(LearningObjective, on_delete=models.CASCADE, related_name='learningObj_that_owns_me')
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.name


# ___________
# Evaluated
# Many to many model to hold user solution, who evaluated it, and when

class Evaluated(models.Model):
    whoEvaluated = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, default=1,)
    date = models.DateTimeField(auto_now_add=datetime.now, blank=True)

    def __str__(self):
        return self.whoEvaluated.username


# _____________
# USER SOLUTION
# The connector of the TC submitted work with the admin defined objects.
# Uploaded by a TC in response to a challenge and assessed with rubricLines
# dictated by learningObjectives attached to the Challenge

class GeneralSolution(models.Model):
    creator = models.ForeignKey(User, null=False, default='', on_delete=models.CASCADE)
    creationDate = models.DateTimeField(auto_created=True)
    solutionInstance = models.ForeignKey(SolutionInstance, null=True, on_delete=models.CASCADE)
    evaluated = models.ManyToManyField(Evaluated, blank=True, related_name='evaluator')


class TempUserSolution(GeneralSolution):
    # file = models.FileField(upload_to='uploads/', blank=True)
    solution = RichTextField()
    archived = models.BooleanField(default=False)
    # userOwner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    # challengeName = models.ForeignKey(Challenge, blank=True, null=True, on_delete=models.CASCADE)
    # solutionInstance = models.ForeignKey(SolutionInstance, null=True, on_delete=models.CASCADE)
    goodTitle = models.TextField(verbose_name='What’s a good title for your work?', blank=True, default='', )
    workFit = models.TextField('How does this piece of work fit into the story of your development as a teacher? (*required)', blank=False, default='')
    proudDetail = models.TextField('What’s a specific detail in this work that you are especially proud of? why? (*required)', blank=False, default='')
    hardDetail = models.TextField('Which detail shows what was especially hard for you?  how? (*required)', blank=False, default='')
    objectiveWell = models.TextField('What’s one objective that you met really well? What’s your evidence?', blank=True, default='')
    objectivePoor = models.TextField('What’s one objective that you still want to work on? What evidence leads you to think this is  an area of growth for you?', blank=True, default='')
    personalLearningObjective = models.TextField('Do you have any learning objectives of your own--in addition to those specified below--that you’d like the Observer to consider when they look at your work?  If so, add them at the top of the Observation Form.', blank=True, default='')
    helpfulLearningExp = models.TextField('Choose one of the above learning experiences that you found helpful. How did it help you? (*required)', blank=False, default='')
    notHelpfulLearningExp = models.TextField("Choose one of the above learning experiences that was less helpful. Why wasn't it helpful? (*required)", blank=False, default='')
    changeLearningExp = models.TextField('What is one learning experience that you would change? How would you change it?', blank=True, default='')
    notIncludedLearningExp = models.TextField('Did you engage in any helpful learning experiences that were not included in the challenge guide? Please let us know what they were so that we can think about adding them.', blank=True, default='')
    customized = models.BooleanField(default=False)
    # evaluated = models.ManyToManyField(Evaluated, blank=True, related_name='evaluated')

    def __str__(self):
        if self.solutionInstance is not None:
            name = self.creator.username.__str__() + ' ' + self.solutionInstance.name.__str__()
        else:
            name = self.creator.username.__str__()
        return name


class TempTfJSolution(GeneralSolution):
    tcLO = models.ForeignKey(LearningObjective, default='', null=False, on_delete=models.CASCADE)
    coachLO = models.ForeignKey(LearningObjective, default='', null=False, on_delete=models.CASCADE, related_name='TempCoachLO')
    solution = RichTextUploadingField()
    # solutionInstance = models.ForeignKey(SolutionInstance, default='', null=False, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, default='', null=False, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.solutionInstance) + ' ' + str(self.user)


class UserSolution(models.Model):
    file = models.FileField(upload_to='uploads/', blank=True)
    solution = RichTextField()
    archived = models.BooleanField(default=False)
    userOwner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    challengeName = models.ForeignKey(Challenge, blank=True, null=True, on_delete=models.CASCADE)
    solutionInstance = models.ForeignKey(SolutionInstance, null=True, on_delete=models.CASCADE)
    goodTitle = models.TextField(verbose_name='What’s a good title for your work?', blank=True, default='', )
    workFit = models.TextField('How does this piece of work fit into the story of your development as a teacher? (*required)', blank=False, default='')
    proudDetail = models.TextField('What’s a specific detail in this work that you are especially proud of? why? (*required)', blank=False, default='')
    hardDetail = models.TextField('Which detail shows what was especially hard for you?  how? (*required)', blank=False, default='')
    objectiveWell = models.TextField('What’s one objective that you met really well? What’s your evidence?', blank=True, default='')
    objectivePoor = models.TextField('What’s one objective that you still want to work on? What evidence leads you to think this is  an area of growth for you?', blank=True, default='')
    personalLearningObjective = models.TextField('Do you have any learning objectives of your own--in addition to those specified below--that you’d like the Observer to consider when they look at your work?  If so, add them at the top of the Observation Form.', blank=True, default='')
    helpfulLearningExp = models.TextField('Choose one of the above learning experiences that you found helpful. How did it help you? (*required)', blank=False, default='')
    notHelpfulLearningExp = models.TextField("Choose one of the above learning experiences that was less helpful. Why wasn't it helpful? (*required)", blank=False, default='')
    changeLearningExp = models.TextField('What is one learning experience that you would change? How would you change it?', blank=True, default='')
    notIncludedLearningExp = models.TextField('Did you engage in any helpful learning experiences that were not included in the challenge guide? Please let us know what they were so that we can think about adding them.', blank=True, default='')
    customized = models.BooleanField(default=False)
    evaluated = models.ManyToManyField(Evaluated, blank=True, related_name='evaluated')

    def __str__(self):
        if self.solutionInstance is not None:
            name = self.userOwner.username.__str__() + ' ' + self.solutionInstance.name.__str__()
        else:
            name = self.userOwner.username.__str__() + ' ' + self.challengeName.name.__str__()
        return name


# __________
# TFJ Solution Instance
# modified solution for Teaching for Justice curriculum

class TfJSolution(models.Model):
    tcLO = models.ForeignKey(LearningObjective, default='', null=False, on_delete=models.CASCADE)
    coachLO = models.ForeignKey(LearningObjective, default='', null=False, on_delete=models.CASCADE, related_name='coachLO')
    solution = RichTextUploadingField()
    solutionInstance = models.ForeignKey(SolutionInstance, default='', null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default='', null=False, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.solutionInstance) + ' ' + str(self.user)


class TfJQuestionField(models.Model):
    question = models.CharField(default='', blank=False, max_length=1000)
    response = RichTextUploadingField()


class TfJEval(models.Model):
    learningObjective = models.ForeignKey(LearningObjective, default='', null=False, on_delete=models.CASCADE)
    userSolution = models.ForeignKey(TfJSolution, blank=True, default='', on_delete=models.CASCADE)
    # question = models.ManyToManyField(TfJQuestionField, blank=True)
    question1 = models.TextField('Why did you pick this TFJ learning objective?', default='', blank=True)
    question2 = models.TextField('How does TFJ intersect with this challenge and your solutions?', default='', blank=True)
    question3 = models.TextField('How do you interpret this learning objective?', default='', blank=True)
    question4 = models.TextField('What resources did you use to grow in this area?', default='', blank=True)
    question5 = models.TextField('How did this work move you forward in Teaching for Justice? What are your next steps for this competency?', default='', blank=True)
    evaluator = models.ForeignKey(Evaluated, blank=False, default='', null=False, on_delete=models.CASCADE)


# ___________
# LEARNING EXPERIENCE LIKERT ENTRIES
# Model to store the TCs bool responses to learning expo matrix table thing

class LearningExpoResponses(models.Model):
    learningExperience = models.ForeignKey(LearningExperience, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    NOANSWER = '4'
    NOTAPPLICABLE = '0'
    NEGATIVE = '1'
    NEUTRAL = '2'
    POSITIVE = '3'
    experienceChoices = [
        (NOANSWER, '-'),
        (NOTAPPLICABLE, 'Not Applicable'),
        (NEGATIVE, 'Negative'),
        (NEUTRAL, 'Neutral'),
        (POSITIVE, 'Positive')
    ]
    learningExperienceResponse = models.CharField(
        'Response',
        max_length=2,
        choices=experienceChoices,
        default=''
    )


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

    evaluated = models.ForeignKey(Evaluated, default='', null=True, on_delete=models.CASCADE)
    learningObjective = models.ForeignKey(LearningObjective, on_delete=models.CASCADE)
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
        name = self.student.userOwner.__str__() + self.learningObjective.name.__str__()
        return name


# _____________
# CRITERIA LINE
# An attempt to model a sub-learningObjective for each learningObjective on the rubricLine relationship
# to the learningObjective used for the next level of granularity up.

class CriteriaLine(models.Model):
    criteria = models.ForeignKey(Criterion, on_delete=models.CASCADE)
    # rubricLine = models.ForeignKey(RubricLine, on_delete=models.CASCADE)
    userSolution = models.ForeignKey(UserSolution, on_delete=models.CASCADE)
    evaluator = models.ForeignKey(Evaluated, on_delete=models.CASCADE, null=True, default='', related_name='criteriaLine_evaluator')
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


# _________
# RUBRIC
# Named for the app and one of the simpler models. Stores the generalFeedback for a challenge, as well
# as the completionScore for the challenge.

class Rubric(models.Model):
    # competencies = models.ForeignKey(Competency, on_delete=models.CASCADE)
    generalFeedback = models.TextField(blank=True, default='')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE)
    userSolution = models.ForeignKey(UserSolution, on_delete=models.CASCADE, default='0')
    challengeCompletionLevel = models.IntegerField(default=0)


# ____________
# COACH REVIEW
# Coach reviews submitted rublines from evaluator, releases them for review with TC and
# adds comments as needed

class CoachReview(models.Model):
    userSolution = models.ForeignKey(UserSolution, on_delete=models.CASCADE, default='', related_name='coachReview')
    release = models.BooleanField(default=False, verbose_name='Release to TC?')
    comment = models.TextField(blank=True, default='', max_length=None)
    # evaluator = models.ForeignKey(Evaluated, on_delete=models.CASCADE, default='', related_name='evaluator')


# __________
# CompetencyProgress
# Store TC progress on attached learning objectives
# Act as a place for Evaluators to record different metrics in the future
# (namely, I think a human override of machine decisions would occur here)

class CompetencyProgress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    competency = models.ForeignKey(Competency, on_delete=models.CASCADE)
    rubricLines = models.ManyToManyField(RubricLine, blank=True)
    attempted = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    manualOverride = models.BooleanField(default=False)


# _________
# ChallengeAddendum
# First attempt at a flexible model for creating
# individualized challenges

class ChallengeAddendum(models.Model):
    name = models.CharField(max_length=250)
    note = models.TextField(blank=True, default='')
    parentChallenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    userSolution = models.ForeignKey(UserSolution, on_delete=models.CASCADE)
    learningObjs = models.ManyToManyField(LearningObjective, blank=True)
    group = models.ForeignKey(Group, blank=True, null=True, on_delete=models.CASCADE)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.name

