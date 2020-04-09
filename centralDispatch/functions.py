from rubrics.models import Challenge, UserSolution, SolutionInstance
from centralDispatch.models import SolutionRouter, AssignmentKeeper
from account.models import Profile
from django.contrib.auth.models import User
from django.core.mail import send_mail


def submissionAlert(challenge, user):
    print('submission alert called')
    # if SolutionRouter.objects.all().filter(solutionInstance=challenge).exists():
    email_recipient = 'liamphunt@gmail.com'  # 'hausman@wwgradschool.org'
    print('email ' + str(email_recipient))
    send_mail('The Orchard: New TC submission', user.first_name + ' has submitted a solution for' + challenge.name,
              'noreply@wwgradschool.org', [email_recipient, ], fail_silently=False)
    return


def evaluatorAssigned(assignmentKeeper):
    email_recipient = assignmentKeeper.evaluator.user.email
    print('email ' + str(email_recipient))
    send_mail('The Orchard: New TC submission', assignmentKeeper.userSolution.userOwner.first_name +
              ' has submitted a solution ',
              'noreply@wwgradschool.org', [email_recipient, ], fail_silently=False)
    return
