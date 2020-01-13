from rest_framework import serializers
from rubrics.models import Rubric, RubricLine, CoachReview, UserSolution


class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = ('generalFeedback', 'challenge', 'evaluator', 'userSolution', 'challengeCompletionLevel')


class RubricLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = RubricLine
        fields = ('evidenceMissing', 'evidencePresent', 'feedback', 'suggestions', 'completionLevel', 'student',
                  'evaluated', 'learningObjective', 'needsLaterAttention', 'ready', 'ignore')


class CoachReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoachReview
        fields = ('release', 'comment', 'userSolution')


class CompletedFeedbackSerializer(serializers.Serializer):
    rubric = RubricSerializer(many=True)
    rubricLine = RubricLineSerializer(many=True)
    coachReview = CoachReviewSerializer(many=True)
