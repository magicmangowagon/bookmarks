from django.db import models
from django.contrib.auth.models import User
from djrichtextfield.models import RichTextField
from tinymce import models as tinymce_models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Many-to-many with, connected to competencies and challenges
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


class Challenge(models.Model):
    name = models.CharField(max_length=250)
    description = RichTextField()
    learningObjs = models.ManyToManyField(LearningObjective, blank=True)

    def __str__(self):
        return self.name


# Unsure, might be a one-to-many with LO's in it's bucket. Not sure if it needs to be
# controlled by the Challenge model
class Competency(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
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


# One-to-many with their parent LO
class Criterion(models.Model):
    name = models.CharField(max_length=250)
    learningObj = models.ForeignKey(LearningObjective, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class UserSolution(models.Model):
    file = models.FileField(upload_to='uploads/', blank=True)
    solution = tinymce_models.HTMLField()
    userOwner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    challengeName = models.ForeignKey(Challenge, blank=True, null=True, on_delete=models.CASCADE)


class Rubric(models.Model):
    competencies = models.ForeignKey(Competency, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)


class RubricLine(models.Model):
    evidenceMissing = models.TextField(blank=True, default='')
    evidencePresent = models.TextField(blank=True, default='')
    feedback = models.TextField(blank=True, default='')
    suggestions = models.TextField(blank=True, default='')
    completionLevel = models.IntegerField(default=0)
    student = models.ForeignKey(UserSolution, on_delete=models.CASCADE)
    learningObjective = models.ForeignKey(LearningObjective, on_delete=models.CASCADE)


class UserProfile(models.Model):
    TC = 1
    CLINICALSUPER = 2
    COACH = 3
    ADMIN = 4
    ROLE_CHOICES = (
        (TC, 'Teaching Candidate'),
        (CLINICALSUPER, 'Clinical Supervisor'),
        (COACH, 'Challenge Coach'),
        (ADMIN, 'Admin')
    )

    user = models.OneToOneField(User, related_name='role', on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()


