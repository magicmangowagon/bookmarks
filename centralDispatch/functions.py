from rubrics.models import Challenge, UserSolution, SolutionInstance
from centralDispatch.models import SolutionRouter
from account.models import Profile
from django.contrib.auth.models import User
from django.core.mail import send_mail


def submissionAlert(challenge, user):
    print('submission alert called')
    if SolutionRouter.objects.all().filter(challenge=challenge).exists():
        email_recipient = SolutionRouter.objects.get(challenge=challenge).profile.user.email
        print('email ' + str(email_recipient))
        send_mail('The Orchard: New TC submission', user.first_name + ' has submitted a challenge solution',
                  'noreply@wwgradschool.org', [email_recipient, ], fail_silently=False)
        return

    else:
        send_mail('The Orchard: New TC submission', user.first_name + ' has submitted a challenge solution',
                  'noreply@wwgradschool.org', ['liamphunt@gmail.com', ], fail_silently=False)
        print('submission not found')
        return
