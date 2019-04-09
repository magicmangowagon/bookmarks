from .models import RubricLine, Competency, CompetencyProgress
from django.db import transaction


def process_rubricLine(rubricLines):
    for RubricLine in rubricLines:
        if (RubricLine.completionLevel < 50 and RubricLine.needsLaterAttention is not True) or (RubricLine.completionLevel >= 50 and RubricLine.needsLaterAttention is True):
            RubricLine.ready = False
        else:
            RubricLine.ready = True

    assess_competency_done(rubricLines)

    return rubricLines


def assess_competency_done(rubricLines):
    competencies = Competency.objects.all()
    user = rubricLines[0].student.userOwner
    for competencies in competencies:
        neededID = type(competencies).objects.get(id=competencies.id)
        compProg = CompetencyProgress(
            competency=neededID,
            student=user
        )
        compProg.save()

    compProgs = CompetencyProgress.objects.all()

    for object in compProgs:
        for RubricLine in rubricLines:
            if RubricLine.learningObjective.compGroup == object.competency.compGroup and RubricLine.learningObjective.compNumber == object.competency.compNumber:
                compProg = type(object).objects.get(pk=object.id)
                rbID = type(RubricLine).objects.get(pk=RubricLine.id)
                compProg.save()

                compProg.rubricLines.add(rbID)

                if RubricLine.ready is False:
                    object.complete = False
                    break
                else:
                    object.complete = True

    return compProgs
    # take list of RubricLines, break down into compLetter-compNumber
    # evaluate if ready bool is checked for all in group, record this bool
    # and add to a list, return list
