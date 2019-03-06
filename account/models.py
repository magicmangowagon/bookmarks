from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class Profile(models.Model):
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

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)
    email = models.EmailField(default="")

    def __str__(self):
        return 'Profile for user {}' .format(self.user.username)


@receiver(post_save, sender=User, dispatch_uid="something_here")
def create_profile(sender, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.create(user=kwargs['instance'])
