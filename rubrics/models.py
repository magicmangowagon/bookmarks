from django.db import models
from django.contrib.auth.models import User, Group
from djrichtextfield.models import RichTextField
from taggit.managers import TaggableManager


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
    tags = TaggableManager(blank=True)

    def __str__(self):
        fullname = str(self.compGroup) + "-" + str(self.compNumber) + "." + str(self.loNumber) + " " + str(self.name)
        return fullname

#____________________
#CHALLENGE COVER PAGE
# New model of challenges, linear structure


# __________
# CHALLENGES
# Works as the main/only way to organize learningObjectives and therefore rubricLines for TC completion.
# This is how users do things


class Challenge(models.Model):

    name = models.CharField(max_length=250)
    description = RichTextField('Challenge Overview', )
    clinicalNeeds = RichTextField('Clinical Needs', default='')
    standardSolution = RichTextField('Standard Solution', default='')
    pullQuote = models.CharField('Pull Quote', max_length=500, default='')

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
    DESIGN = models.BooleanField('Design', default=False)
    SIMULATE = models.BooleanField('Simulate', default=False)
    IMPLEMENT = models.BooleanField('Implement', default=False)

    degreeImplementation = [DESIGN, SIMULATE, IMPLEMENT]

    ONEONONE = models.BooleanField('One on One', default=False)
    SMALLGROUP = models.BooleanField('Small Group', default=False)
    FULLCLASS = models.BooleanField('Full Class', default=False)

    scaleImplementation = [ONEONONE, SMALLGROUP, FULLCLASS]

    REFLECTION = models.BooleanField('Reflection', default=False)
    CLASSROOMEVIDENCE = models.BooleanField('Classroom Evidence', default=False)
    OBSERVATION = models.BooleanField('Observation', default=False)

    typeImplementation = [REFLECTION, CLASSROOMEVIDENCE, OBSERVATION]

    '''
    degree = (
        (DESIGN, 'Design'),
        (SIMULATE, 'Simulate'),
        (IMPLEMENT, 'Implement'),
    )
    scale = (
        (ONEONONE, 'One on One'),
        (SMALLGROUP, 'Small Group'),
        (FULLCLASS, 'Full Class'),
    )
    type = (
        (REFLECTION, 'Reflection'),
        (CLASSROOMEVIDENCE, 'Classroom Evidence'),
        (OBSERVATION, 'Observation'),
    )
    '''
    # degreeImplementation = models.BooleanField('Degree of Implementation', choices=degree, default=DESIGN)
    # scaleImplementation = models.BooleanField('Scale of Implementation', choices=scale, default=ONEONONE)
    # typeImplementation = models.BooleanField('Type of Implementation', choices=type, default=REFLECTION)

    learningObjs = models.ManyToManyField(LearningObjective, blank=True, related_name="challenge")
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.name


# __________
# LEARNING EXPERIENCE

class LearningExperience(models.Model):
    name = models.CharField(max_length=600)
    challenge = models.ForeignKey(Challenge, blank=True, on_delete=models.CASCADE, related_name="challenge")
    learningObjectives = models.ManyToManyField(LearningObjective, blank=True, related_name="learningObjective")
    index = models.IntegerField('Index', default=0)
    description = RichTextField()
    tags = TaggableManager(blank=True)

    class Meta:
        order_with_respect_to = 'challenge'

    def __str__(self):
        return self.name


# __________
# COMPETENCY

class Competency(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    learningObjs = models.ForeignKey(LearningObjective, blank=True, null=True, on_delete=models.CASCADE)
    tags = TaggableManager(blank=True)

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
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.name


# _____________
# USER SOLUTION
# The connector of the TC submitted work with the admin defined objects.
# Uploaded by a TC in response to a challenge and assessed with rubricLines
# dictated by learningObjectives attached to the Challenge

class UserSolution(models.Model):
    file = models.FileField(upload_to='uploads/', blank=True)
    solution = models.CharField(max_length=2000, blank=False)
    userOwner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    challengeName = models.ForeignKey(Challenge, blank=True, null=True, on_delete=models.CASCADE)
    goodTitle = models.TextField(verbose_name='What’s a good title for your work?', blank=True, default='', )
    workFit = models.TextField('How does this piece of work fit into the story of your development as a teacher? (*required)', blank=False, default='')
    proudDetail = models.TextField('What’s a specific detail in this work that you are especially proud of? why? (*required)', blank=False, default='')
    hardDetail = models.TextField('Which detail shows what was especially hard for you?  how? (*required)', blank=False, default='')
    objectiveWell = models.TextField('What’s one objective that you met really well? What’s your evidence?',blank=True, default='')
    objectivePoor = models.TextField('What’s one objective that you still want to work on? What evidence leads you to think this is  an area of growth for you?', blank=True, default='')
    personalLearningObjective = models.TextField('Do you have any learning objectives of your own--in addition to those specified below--that you’d like the Observer to consider when they look at your work?  If so, add them at the top of the Observation Form.', blank=True, default='')
    helpfulLearningExp = models.TextField('Choose one of the above learning experiences that you found helpful. How did it help you? (*required)', blank=False, default='')
    notHelpfulLearningExp = models.TextField("Choose one of the above learning experiences that was less helpful. Why wasn't it helpful? (*required)", blank=False, default='')
    changeLearningExp = models.TextField('What is one learning experience that you would change? How would you change it?', blank=True, default='')
    notIncludedLearningExp = models.TextField('Did you engage in any helpful learning experiences that were not included in the challenge guide? Please let us know what they were so that we can think about adding them.', blank=True, default='')
    customized = models.BooleanField(default=False)


# ___________
# LEARNING EXPERIENCE LIKERT ENTRIES
# Model to store the TCs bool responses to learning expo matrix table thing

class LearningExpoResponses(models.Model):
    learningExperience = models.ForeignKey(LearningExperience, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    NOTAPPLICABLE = '0'
    NEGATIVE = '1'
    NEUTRAL = '2'
    POSITIVE = '3'
    experienceChoices = [
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
# Named for the app and one of the simpler models. Stores the generalFeedback for a challenge, as well
# as the completionScore for the challenge.

class Rubric(models.Model):
    # competencies = models.ForeignKey(Competency, on_delete=models.CASCADE)
    generalFeedback = models.TextField(blank=True, default='')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE)
    userSolution = models.ForeignKey(UserSolution, on_delete=models.CASCADE, default='0')
    challengeCompletionLevel = models.IntegerField(default=0)


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

