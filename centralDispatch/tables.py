import django_tables2 as tables
from .models import SolutionStatus, ChallengeStatus
from django.utils.html import mark_safe


class SolutionTable(tables.Table):

    class Meta:
        model = SolutionStatus

        fields = {'userSolution__userOwner__last_name', 'userSolution__userOwner__first_name',  'challengestatus__solutionStatusByInstance__challengestatus__challengeAccepted',
                  'userSolution__solutionInstance', 'solutionSubmitted', 'solutionEvaluated',
                  'solutionCoachReviewed', 'solutionRejected', 'returnedTo', 'solutionCompleted'}
        sequence = ('userSolution__userOwner__last_name', 'userSolution__userOwner__first_name',  'challengestatus__solutionStatusByInstance__challengestatus__challengeAccepted',
                  'userSolution__solutionInstance', 'solutionSubmitted', 'solutionEvaluated',
                  'solutionCoachReviewed', 'solutionRejected', 'returnedTo', 'solutionCompleted')
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
