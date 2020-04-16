from rubrics.models import Challenge, UserSolution, SolutionInstance
from centralDispatch.models import SolutionRouter, AssignmentKeeper
from account.models import Profile
from django.contrib.auth.models import User
from account.models import Profile
from django.core.mail import send_mail


def submissionAlert(challenge, tc):
    print('submission alert called')
    # if SolutionRouter.objects.all().filter(solutionInstance=challenge).exists():
    users = User.objects.all().filter(profile__role=4)
    email_recipients = []
    for user in users:
        email_recipients.append(user.email)
    send_mail('The Orchard: New TC submission', tc.first_name + ' has submitted a solution for ' + challenge.name,
              'noreply@wwgradschool.org', email_recipients, fail_silently=False)
    return


def evaluatorAssigned(assignmentKeeper):
    email_recipient = assignmentKeeper.evaluator.user.email
    print('email ' + str(email_recipient))
    send_mail('The Orchard: New TC submission', assignmentKeeper.userSolution.userOwner.first_name +
              ' has submitted a solution ',
              'noreply@wwgradschool.org', [email_recipient, ], fail_silently=False)
    return


def evaluationCompleted(userSolution, user):
    try:
        email_recipient = AssignmentKeeper.objects.get(userSolution=userSolution).coach.user.email
        send_mail('The Orchard: New evaluator submission', user.first_name +
                  ' has submitted an evaluation for ' + str(userSolution),
                  'noreply@wwgradschool.org', [email_recipient, ], fail_silently=False)
    except:
        users = User.objects.all().filter(profile__role=4)
        email_recipients = []
        for user in users:
            email_recipients.append(user.email)
        email_recipient = email_recipients
        send_mail('The Orchard: New evaluator submission', user.first_name +
                  ' has submitted an evaluation for ' + str(userSolution),
                  'noreply@wwgradschool.org', email_recipient, fail_silently=False)

