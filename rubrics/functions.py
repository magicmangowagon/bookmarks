
from .models import RubricLine


def somethingswrong(rubricLine):
        if rubricLine.completionLevel < 50 and rubricLine.needsLaterAttention != True:
            return True
