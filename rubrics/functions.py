from .models import RubricLine, Competency, CompetencyProgress, LearningObjective, ChallengeAddendum, Challenge, MegaChallenge
from zipfile import ZipFile


# processes rubriclines from view, checks if ready conditions are met, records result, saves the
# variable to the model instance in the DB, and returns list to the view
def process_rubricLine(rubricLines):
    for RubricLine in rubricLines:
        if (RubricLine.completionLevel < 50 and RubricLine.needsLaterAttention is 'B') or (RubricLine.completionLevel >= 50 and RubricLine.needsLaterAttention is 'A'):
            RubricLine.ready = False

        else:
            RubricLine.ready = True
        RubricLine.save()

    return rubricLines


# Takes list of rubricLines from view, checks if there is a corresponding competency progress instance for this user
# if not, creates them and saves to DB with rubric lines tied to it.
def assess_competency_done(rubricLines):
    competencies = Competency.objects.all()
    user = rubricLines[0].student.userOwner

    for competencies in competencies:
        if CompetencyProgress.objects.filter(competency=competencies, student=user).exists():
            break
        else:
            neededID = type(competencies).objects.get(id=competencies.id)
            compProg = CompetencyProgress(
                competency=neededID,
                student=user
            )
            compProg.save()

    compProgs = CompetencyProgress.objects.all().filter(student=user)

    learningObjs = LearningObjective.objects.all()
    print('Running assessment for ' + user.first_name)

    for learningObj in learningObjs:
        if rubricLines.filter(learningObjective=learningObj.id).exists() is False:
            compProgs.filter(competency__learningObjs=learningObj.id).complete = False

    for object in compProgs:
        # User has attempted all LO's in the competency, proceed to check each one for completion
        for RubricLine in rubricLines:
            # checks for existing rubricLines
            if RubricLine.learningObjective.compGroup == object.competency.compGroup \
                    and RubricLine.learningObjective.compNumber == object.competency.compNumber \
                    and RubricLine.student.userOwner == object.student:

                # get compProg instance and add a rubricLine relationship to it
                compProg = type(object).objects.get(pk=object.id)
                rbID = type(RubricLine).objects.get(pk=RubricLine.id)
                compProg.rubricLines.add(rbID)
                compProg.save()

                object.attempted = True
                if RubricLine.ready is False:
                    object.complete = False
                    break
                else:
                    object.complete = True
        # save the competencyProgress instance
        object.save()

    return compProgs


def get_filenames(path_to_zip):
    with ZipFile(path_to_zip, 'r') as zip:
        return zip.namelist()


# def evaluation_initializer():
