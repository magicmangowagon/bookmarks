from .models import RubricLine, Competency

def somethingswrong(rubricLine):
        if rubricLine.completionLevel < 50 and rubricLine.needsLaterAttention is not True:
            return True

        elif rubricLine.completionLevel >= 50 and rubricLine.needsLaterAttention is True:
            return True

        else:
            return False


def process_rubricLine(rubricLines):
    for RubricLine in rubricLines:
        if (RubricLine.completionLevel < 50 and RubricLine.needsLaterAttention is not True) or (RubricLine.completionLevel >= 50 and RubricLine.needsLaterAttention is True):
            RubricLine.ready = False
        else:
            RubricLine.ready = True

    return rubricLines


def assess_competency_done(rubricLines):
    choices = Competency.objects.all()

    # take list of RubricLines, break down into compLetter-compNumber
    # evaluate if ready bool is checked for all in group, record this bool
    # and add to a list, return list
