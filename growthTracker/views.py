from django.shortcuts import render
from rubrics.models import Rubric, RubricLine, CoachReview
from collections import namedtuple
from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response
from .serializers import RubricSerializer, RubricLineSerializer, CoachReviewSerializer, CompletedFeedbackSerializer


class RubricList(generics.ListCreateAPIView):
    queryset = Rubric.objects.all()
    serializer_class = RubricSerializer
    permission_classes = [permissions.IsAuthenticated]


class RubricDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rubric.objects.all()
    serializer_class = RubricSerializer
    permission_classes = [permissions.IsAuthenticated]


class CompletedFeedback(viewsets.ViewSet):

    def list(self, request):
        completedFeedback = namedtuple('completedFeedback', ('rubric', 'rubricLine', 'coachReview'))

        completedFeedback = completedFeedback(
            rubric=Rubric.objects.all(),
            rubricLine=RubricLine.objects.all(),
            coachReview=CoachReview.objects.all()
        )
        serializer = CompletedFeedbackSerializer(completedFeedback)
        return Response(serializer.data)
    permission_classes = [permissions.IsAuthenticated]
