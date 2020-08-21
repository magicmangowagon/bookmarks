import django_tables2 as tables
from .models import SolutionStatus, ChallengeStatus
from rubrics.models import Evaluated
from django.utils.html import mark_safe
from rubrics.views import SolutionDetailView


class SolutionTable(tables.Table):
    userSolution = tables.Column(linkify={"viewname": "solution-detail", "args": [tables.A("userSolution__pk")]},)
    # tc = tables.Column(accessor='challengestatus', verbose_name='Last Name')
    challenge = tables.Column(accessor='challengestatus', verbose_name='Challenge')
    challengeAccepted = tables.BooleanColumn(accessor='challengestatus', verbose_name='Challenge Accepted')
    completionDate = tables.Column(accessor='userSolution__evaluated')

    def render_completionDate(self, value):
        try:
            return value.all().last().date
        except:
            return 'no eval'

    def render_challengeAccepted(self, value):
        try:
            ca = value.all().first().challengeAccepted
        except:
            ca = 'Not Found'
        return ca

    def render_challenge(self, value):
        try:
            mc = value.all().first().challenge.megaChallenge.name
            return mc
        except:
            try:
                mc = self.userSolution.challenge
            except:
                mc = 'Not Found'
            return mc

    def render_userSolution(self, value):
        try:
            return value.solutionInstance
        except:
            return 'Not Found'

    # Pick back up here tomorrow: Need to extend this to find the user/challenge name when there isn't a
    # challengeStatus
    # def render_tc(self, value):
    #    if value.all().first().exists():
    #        challenge = value.all().first().user.last_name
    #    elif value.all().first():
    #        challenge = value.all().first().userSolution.userOwner.last_name

    #    return challenge

    class Meta:
        model = SolutionStatus

        fields = {'userSolution__userOwner__last_name',
                  'userSolution__userOwner__first_name',
                  'challenge',
                  'challengeAccepted',
                  'userSolution', 'solutionSubmitted', 'solutionEvaluated',
                  'solutionCoachReviewed', 'solutionRejected', 'returnedTo', 'solutionCompleted', 'completionDate'}
        sequence = ('userSolution__userOwner__last_name',
                    'userSolution__userOwner__first_name',
                    'challenge',
                    'challengeAccepted',
                  'userSolution', 'solutionSubmitted', 'solutionEvaluated',
                  'solutionCoachReviewed', 'solutionRejected', 'returnedTo', 'solutionCompleted', 'completionDate')
        attrs = {"class": "solutionStatusTable"}
        # solutions = tables.ManyToManyColumn(transform='challengestatus__solutionStatusByInstance__challengestatus')
        # fields = ('user', 'challenge', 'solutions', 'cs')


class ChallengeTable(tables.Table):
    solutionStatus = tables.ManyToManyColumn(accessor='solutionStatusByInstance')

    def render_solutionStatus(self, value, record):
        ss = ''
        sFirst = True
        sList = list(value.all())

        for s in sList:
            if not sFirst:
                ss += "<br/ >"
            else:
                sFirst = False
            ss += str(s.userSolution.solutionInstance) + ' ' + str(s.solutionSubmitted) + ' ' + str(
                s.solutionEvaluated) + ' ' + str(s.solutionCoachReviewed)

        return mark_safe(ss)

    class Meta:
        model = ChallengeStatus
