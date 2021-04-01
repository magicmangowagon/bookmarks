from rubrics.models import Challenge, MegaChallenge, UserSolution, SolutionInstance, Rubric, RubricLine, \
    ChallengeAddendum, Competency, LearningObjective, LearningExperience
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
# this is breaking when there are connection issues
# need to investigate the db hits not triggering this check
def process_rubricLine(rubricLines):
    completed = False
    for rubricLine in rubricLines:
        if rubricLine.completionLevel < 50:
            print('not ready')
            rubricLine.ready = False
            completed = False
            print('breaking')
            break
        else:
            rubricLine.ready = True
            completed = True
        rubricLine.save()
    if completed:
        print('complete')
        solutionStatus = SolutionStatus.objects.get(userSolution=rubricLines[0].student)
        solutionStatus.solutionCompleted = True
        solutionStatus.save()
        print('returning rubricLines')
    # return rubricLines


# generate dataset for D3
def processCompetencyD3(user):
    challenges = Challenge.objects.all().filter(display=True)

    comps = []
    competencies = Competency.objects.all().filter(archive=False).order_by('compGroup', 'compNumber')
    i = 1
    for competency in competencies:
        comp = {
                    'name': str(competency.compGroup) + '.' + str(competency.compNumber),
                    'fullName': str(competency.name),
                    'id': competency.pk,
                    'type': 'competency',
                    'children': []
                }
        for lo in competency.learningObjs.all():
            lo = {
                    'name': str(lo.compGroup) + '.' + str(lo.compNumber) + '-' + str(lo.loNumber),
                    'fullName': lo.name,
                    'completionLevel': 0,
                    'competency': str(competency),
                    'children': returnChallenge(lo, user),
                    'type': 'learningObj'

                  }
            comp['children'].append(lo)
        comps.append(comp)
    # this needs to be reworked, I don't think we actually care about
    # each lo/rubricLine, pull one instance of each lo (link it up
    # with any other versions of it) and then move on to the challenge/megaChallenge
    # and solutionInstance collection

    newNode = comps
    return newNode


# pull out the challenges that this LO is in
# change it to pull the megachallenge, and
# create an aggregate list of solution instances
def returnChallenge(learningObj, user):
    challengeArray = []
    challenges = learningObj.challenge.all()
    megaChallenge = challenges.first()
    for challenge in list(challenges):
        complete = 0
        solutions = challenge.solutions.all()
        si = []
        for solution in solutions:
            sol = {
                'name': solution.name,
                'complete': checkCompletion(solution, user),
                'type': 'solution'
            }
            if checkCompletion(solution, user) != 0:
                complete = 1
            si.append(sol)
        challenge = {
            'name': generateShortName(str(challenge.name)),
            'fullName': str(challenge.name),
            'complete': complete,
            'type': 'challenge',
            'children': si,
        }
        challengeArray.append(challenge)

    # return nestList(challengeArray)
    return challengeArray


def checkCompletion(solution, user):
    try:
        status = SolutionStatus.objects.get(solutionInstance=solution, userSolution__userOwner=user)
        if status.solutionCompleted:
            return 2
        else:
            return 1
    except SolutionStatus.DoesNotExist:
        return 0


# Truncate the long names in the platform
# until a shortname model field is in place
# and populated by the learning designers
def generateShortName(name):
    shortName = name.split()
    result = ''
    if len(shortName) > 1:
        for i in range(len(shortName)):
            result += shortName[i][0].upper()
    else:
        result = name
    return result


# Iterate through a list and make the preceding element
# a child of the current element
# a somewhat hacky way to get the data structured
# for a D3 Sunburst used in the Competency Tracker
# should probably be on the front end when I get a moment
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


def shit():
    solutionStatus = SolutionStatus.objects.all()
    for ss in solutionStatus:
        ss.solutionCompleted = False
        ss.save()


def fixIncompletes():
    userSolutions = UserSolution.objects.filter(evaluated__whoEvaluated__profile__role__gte=3).filter(solutionstatus__solutionCompleted=False)
    solutionStatus = SolutionStatus.objects.all()
    for u in userSolutions:
        s = solutionStatus.get(userSolution=u)
        rs = RubricLine.objects.filter(student=u).filter(evaluated__whoEvaluated__profile__role__gte=3).order_by(
            'learningObjective_id', '-evaluated__date').distinct('learningObjective_id')
        for r in rs:
            if r.completionLevel < 50:
                s.solutionCompleted = False
                break
            else:
                s.solutionCompleted = True
        s.save()
    # solutionStatus = SolutionStatus.objects.filter(solutionCompleted=False)
    # for ss in solutionStatus:
    #     # ss.solutionCompleted = False
    #     rs = RubricLine.objects.filter(student=ss.userSolution).filter(
    #         evaluated__whoEvaluated__profile__role=3).order_by('evaluated__whoEvaluated',
    #                                                            '-evaluated__date').distinct('evaluated__whoEvaluated')
    #
    #     for r in rs:
    #         print(str(r.student) + ' ' + str(r.evaluated.whoEvaluated) + ' ' + str(r.evaluated.date))
    #         if r.completionLevel < 50:
    #             ss.solutionCompleted = False
    #             ss.save()
    #             break
    #         else:
    #             ss.solutionCompleted = True
    #             ss.save()
    # print(userSolutions.count())


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


def cloneChallenge(challenge):
    originalChallenge = Challenge.objects.get(pk=challenge)
    challengeClone = Challenge.objects.get(pk=challenge)
    challengeClone.pk = None
    challengeClone.name = 'Copy ' + challengeClone.name
    challengeClone.display = False
    challengeClone.save()
    print(originalChallenge.name + str(originalChallenge.learningObjs.all().count()))
    learningExpos = LearningExperience.objects.filter(challenge_id=challenge)
    for lo in originalChallenge.learningObjs.all():
        challengeClone.learningObjs.add(lo)
        print(lo)
        challengeClone.save()
    for learningExpo in learningExpos:
        newLearningExpo = learningExpo
        newLearningExpo.pk = None
        newLearningExpo.name = 'Copy ' + learningExpo.name
        newLearningExpo.challenge = challengeClone
        newLearningExpo.save()

    for solution in originalChallenge.solutions.all():
        newSolution = solution
        newSolution.pk = None
        newSolution.name = 'Copy ' + solution.name
        newSolution.save()
        challengeClone.solutions.add(newSolution)
        challengeClone.save()
