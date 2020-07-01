from rubrics.models import Challenge, UserSolution, SolutionInstance, Rubric, RubricLine
from centralDispatch.models import SolutionRouter, AssignmentKeeper, SolutionStatus, ChallengeStatus
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
              ' has submitted a solution for ' + assignmentKeeper.userSolution,
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


# script to call when tracking stack goes live to update old
# solutions and correctly mark status
def generateStatus():
    userSolutions = UserSolution.objects.all().filter(archived=False)

    for userSolution in userSolutions:
        if SolutionStatus.objects.filter(userSolution=userSolution).exists():

            solutionStatus = SolutionStatus.objects.get(userSolution=userSolution)
            if solutionStatus.solutionSubmitted is False:
                solutionStatus.solutionSubmitted = True

        else:
            solutionStatus = SolutionStatus.objects.create(userSolution=userSolution,
                                                           solutionInstance=userSolution.solutionInstance,
                                                           solutionSubmitted=True)

        if Rubric.objects.filter(userSolution=userSolution):
            print('found Rubric')
            rubrics = Rubric.objects.filter(userSolution=userSolution)
            for rubric in rubrics:
                if rubric.evaluator.profile.role == 2:
                    solutionStatus.solutionEvaluated = True
                if rubric.evaluator.profile.role >= 3:
                    solutionStatus.solutionCoachReviewed = True
            rubricLines = RubricLine.objects.filter(student=userSolution, evaluated__whoEvaluated__profile__role=3)
            for rubricLine in rubricLines:
                if rubricLine.completionLevel < 50:
                    solutionStatus.solutionCompleted = False
                    break
                else:
                    solutionStatus.solutionCompleted = True
        solutionStatus.save()


def GenerateChallengeStatus():
    tcs = User.objects.all().filter(profile__role=1)
    challenges = Challenge.objects.all().filter(display=True, solutions__isnull=False)
    userSolutions = UserSolution.objects.all().filter(archived=False)
    for userSolution in userSolutions:
        if ChallengeStatus.objects.filter(user=userSolution.userOwner, challenge=userSolution.challengeName).exists():
            print('Challenge Status Already Exists')
        else:
            ChallengeStatus.objects.create(user=userSolution.userOwner, challenge=userSolution.challengeName)


