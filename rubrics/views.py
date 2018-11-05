from django.shortcuts import render
from .models import Challenge
from .forms import ChallengeForm


def update_challenge(request):
    challenge = Challenge.objects.get()
    if request.method == 'POST':
        form = ChallengeForm(request.POST, instance=challenge)
        if form.is_valid():
            form.save()
    else:
        form = ChallengeForm(instance=challenge)
    return render(request, 'rubrics/rubric_form.html', {'form': form, 'challenge': challenge})
