import django_tables2 as tables
from .models import SolutionStatus


class SolutionTable(tables.Table):
    # cs = tables.Column(empty_values=())

    class Meta:
        model = SolutionStatus

        solutions = tables.ManyToManyColumn(transform='challengeStatus__solutionStatusByInstance__set')
        # fields = ('user', 'challenge', 'solutions', 'solutionStatusByInstance')
