from rubrics.models import Challenge, MegaChallenge, UserSolution, SolutionInstance, Rubric, RubricLine, ChallengeAddendum, Competency, LearningObjective
from centralDispatch.models import SolutionRouter, AssignmentKeeper, SolutionStatus, ChallengeStatus, SomethingHappened
from account.models import Profile
from django.contrib.auth.models import User
from account.models import Profile
from django.core.mail import send_mail
from datetime import datetime, timedelta


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
    if assignmentKeeper.evaluator:
        email_recipient = assignmentKeeper.evaluator.user.email
        print('email ' + str(email_recipient))
    elif assignmentKeeper.coach:
        email_recipient = assignmentKeeper.coach.user.email
        print('email ' + str(email_recipient))
    else:
        print('not assigned')
        return

    send_mail('The Orchard: New TC submission', assignmentKeeper.userSolution.userOwner.first_name +
              ' has submitted a solution for ' + str(assignmentKeeper.userSolution.solutionInstance),
              'noreply@wwgradschool.org', [email_recipient, ], fail_silently=False)
    return


def evaluationCompleted(userSolution, user):
    print('evaluationCompletedFunctionRunning')
    try:
        email_recipient = AssignmentKeeper.objects.get(userSolution=userSolution).coach.user.email
        send_mail('The Orchard: New evaluator submission', user.first_name +
                  ' has submitted an evaluation for ' + str(userSolution),
                  'noreply@wwgradschool.org', [email_recipient, ], fail_silently=False)
        print('evaluationCompletedFunctionRunning "within try"')

    except:
        users = User.objects.all().filter(profile__role=4)
        print('evaluationCompletedFunctionRunning "within except"')
        email_recipients = []
        for user in users:
            email_recipients.append(user.email)
        email_recipient = email_recipients
        send_mail('The Orchard: New evaluator submission', user.first_name +
                  ' has submitted an evaluation for ' + str(userSolution),
                  'noreply@wwgradschool.org', email_recipient, fail_silently=False)


# moved processRubricLines in to CentralDispatch
def process_rubricLine(rubricLines):
    completed = False
    for RubricLine in rubricLines:
        if RubricLine.completionLevel < 50:
            RubricLine.ready = False
            completed = False
            break
        else:
            RubricLine.ready = True
            completed = True
        RubricLine.save()
    if completed:
        solutionStatus = SolutionStatus.objects.get(userSolution=rubricLines.first().student)
        solutionStatus.solutionCompleted = True
        solutionStatus.save()
    return rubricLines


def processCompetencyD3(user):
    challenges = Challenge.objects.all().filter(display=True)
    # learningObjs = {}
    comps = []
    learningsObjs = []
    competencies = Competency.objects.all().filter(archive=False).order_by('compGroup', 'compNumber')
    i = 1
    for competency in competencies:
        comps.append({'name': str(competency.compGroup) + '.' + str(competency.compNumber),
                      'fullName': str(competency.name),
                      'id': competency.pk,
                      'children': []})

    # this needs to be reworked, I don't think we actually care about
    # each lo/rubricLine, pull one instance of each lo (link it up
    # with any other versions of it) and then move on to the challenge/megaChallenge
    # and solutionInstance collection
    for challenge in challenges:
        for solutionInstance in challenge.solutions.all():
            if UserSolution.objects.filter(solutionInstance=solutionInstance, userOwner=user).exists():
                userSolution = UserSolution.objects.get(solutionInstance=solutionInstance, userOwner=user)
                if SolutionStatus.objects.get(userSolution=userSolution).solutionCompleted is True:
                    for learningObjective in solutionInstance.learningObjectives.all().order_by('id').distinct('id'):
                        # comps['competencies'][str(learningObjective.competency_set.first())].update(
                        learningsObjs.append(
                            {
                                'name': str(learningObjective.compGroup) + '.' + str(learningObjective.compNumber) + '-' + str(learningObjective.loNumber),
                                'fullName': learningObjective.name,
                                'completionLevel': 1,
                                'size': 3,
                                'competency': str(learningObjective.competency_set.first()),
                                'children': returnChallenge(learningObjective, 1)
                            }
                        )
                else:
                    for learningObjective in solutionInstance.learningObjectives.all():
                        # comps['competencies'][str(learningObjective.competency_set.first())].update(
                        learningsObjs.append(
                            {
                                'name': str(learningObjective.compGroup) + '.' + str(learningObjective.compNumber) + '-' + str(learningObjective.loNumber),
                                'fullName': learningObjective.name,
                                'completionLevel': 2,
                                'size': 3,
                                'competency': str(learningObjective.competency_set.first()),
                                'children': returnChallenge(learningObjective, 2)

                            }
                        )

            else:
                for learningObjective in solutionInstance.learningObjectives.all().order_by('id').distinct('id'):
                    # comps['competencies'][str(learningObjective.competency_set.first())].update(
                    learningsObjs.append(
                        {
                            'name': str(learningObjective.compGroup) + '.' + str(learningObjective.compNumber) + '-' + str(learningObjective.loNumber),
                            'fullName': learningObjective.name,
                            'completionLevel': 0.1,
                            'size': 3,
                            'competency': str(learningObjective.competency_set.first()),
                            'children': returnChallenge(learningObjective, 0.1)
                        }
                        )

    for comp in comps:
        for lo in learningsObjs:
            if lo['competency'] == comp['fullName'] and lo not in comp['children']:
                comp['children'].append(lo)

    dataNode = {'name': 'Competencies',
                'children': comps}

    return dataNode


# pull out the challenges that this LO is in
# change it to pull the megachallenge, and
# create an aggregate list of solution instances
def returnChallenge(learningObj, cl):
    challengeArray = []
    challenges = learningObj.challenge.all()

    for challenge in list(challenges):

        challenge = {
            'name': generateShortName(str(challenge.name)),
            'fullName': str(challenge.name),
            'size': 5,
            'children': [],
            'completionLevel': cl
        }
        challengeArray.append(challenge)

    return nestList(challengeArray)


def generateShortName(name):
    shortName = name.split()
    result = ''
    if len(shortName) > 1:
        for i in range(len(shortName)):
            result += shortName[i][0].upper()
    else:
        result = name
    return result


def nestList(array):
    x = len(array)
    for i, item in enumerate(array):
        if 0 < i < x:
            item['children'].append(array.pop(array.index(item) - 1))
            nestList(array)
    return array


def processCompetency(rubricLines):
    learningObjectives = LearningObjective.objects.all().filter(archive=False).order_by('compGroup', 'compNumber',
                                                                                        'loNumber').distinct()
    challenges = Challenge.objects.all().filter(display=True)
    los = []

    print('learningObjectives Length' + str(len(learningObjectives)))
    for challenge in challenges:
        for learningObjective in challenge.learningObjs.all():
            los.append(learningObjective)
    competencies = Competency.objects.all().order_by('compGroup', 'compNumber')
    print('los Length' + str(len(los)))
    compiledRubricLines = {}
    for competency in competencies:
        compiledRubricLines.update({str(competency): {}
                                    })
        i = 0
        for lo in los:
            i += 1
            loLabel = str(lo.compGroup) + '.' + str(lo.compNumber) + '-' + str(lo.loNumber)
            if lo in competency.learningObjs.all():
                if rubricLines.filter(learningObjective=lo):
                    rl = rubricLines.filter(learningObjective=lo)
                    for r in rl:
                        if UserSolution.objects.get(rubricline=r).solutionstatus_set.first().solutionCompleted is True:
                            compiledRubricLines[str(competency)].update({r.id: [2, loLabel]})
                        else:
                            compiledRubricLines[str(competency)].update({r.id: [1, loLabel]})
                else:
                    compiledRubricLines[str(competency)].update({lo.id + i: [0, loLabel]})

    return compiledRubricLines


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


def fixEmptySolutionStatus():
    cas = ChallengeStatus.objects.all()
    for ca in cas:
        # print(ca)
        for solutionStatus in ca.solutionStatusByInstance.all():
            if solutionStatus.userSolution is None:
                # print(solutionStatus)
                if UserSolution.objects.filter(userOwner=ca.user, solutionInstance=solutionStatus.solutionInstance).exists():
                    print(UserSolution.objects.get(userOwner=ca.user, solutionInstance=solutionStatus.solutionInstance))

                    userSolution = UserSolution.objects.get(userOwner=ca.user, solutionInstance=solutionStatus.solutionInstance)
                    solutionStatus.userSolution = userSolution
                    solutionStatus.save(update_fields=['userSolution'])


def GenerateChallengeStatus():
    tcs = User.objects.all().filter(profile__role=1)
    challenges = Challenge.objects.all().filter(display=True, solutions__isnull=False)
    userSolutions = UserSolution.objects.all().filter(archived=False)
    for userSolution in userSolutions:
        if ChallengeStatus.objects.filter(user=userSolution.userOwner, challenge=userSolution.challengeName).exists():
            print('Challenge Status Already Exists')
        else:
            ChallengeStatus.objects.create(user=userSolution.userOwner, challenge=userSolution.challengeName)


def CreateEvaluation(userSolution):
    solutionStatus = SolutionStatus.objects.get(userSolution=userSolution)
    if solutionStatus.solutionEvaluated:
        rubricLines = RubricLine.objects.all().filter(userSolution=userSolution).distinct().latest()
        return rubricLines
    else:
        if not userSolution.customized:
            learningObjectives = userSolution.solutionInstance.learningObjectives.all()
        else:
            challengeAddendum = ChallengeAddendum.objects.get(userSolution=userSolution)
            learningObjectives = challengeAddendum.learningObjs.all()
        return learningObjectives


def PopulateSomethingHappened():
    somethings = SomethingHappened.objects.all()

    for s in somethings:
        if s.time[0]:
            s.created = s.time[0]
        else:
            newTime = datetime.now() - timedelta(days=260)
            s.time.append(newTime)
        try:
            s.modified = s.time[-1]
            s.modCount = len(s.time)
        except:
            pass
        s.save()


def createSomethings():
    userSolutions = UserSolution.objects.all().filter(somethinghappened__isnull=True)

    for solution in userSolutions:
        SomethingHappened.objects.create(userSolution=solution)
        newTime = datetime.now() - timedelta(days=260)
        SomethingHappened.objects.filter(userSolution=solution).update(created=newTime)

