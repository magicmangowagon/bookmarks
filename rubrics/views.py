from django.shortcuts import render, get_object_or_404
from .models import Challenge
from .forms import ChallengeForm
from django.views.generic import ListView, DetailView


def update_challenge(request):
    challenge = Challenge.objects.get()
    if request.method == 'POST':
        form = ChallengeForm(request.POST, instance=challenge)
        if form.is_valid():
            form.save()
    else:
        form = ChallengeForm(instance=challenge)
    return render(request, 'rubrics/rubric_form.html', {'form': form, 'challenge': challenge})


class challenge_detail(DetailView):
    model = Challenge

    def get_context_data(self, **kwargs):
        context = super(challenge_detail, self).get_context_data(**kwargs)
        context['rubric_list'] = Challenge.objects.all()
        return context

    # challenge = get_object_or_404(Challenge)
    # return render(request, 'rubrics/challenge_detail.html', {'challenge': challenge, 'int': int})


class ChallengeListView(ListView):
    queryset = Challenge.objects.all()
    context_object_name = 'challenges'
    # paginate_by = 3
    template_name = 'rubrics/list.html'
