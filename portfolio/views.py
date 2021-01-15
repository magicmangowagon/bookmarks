from django.shortcuts import render, redirect
from .models import Portfolio
from django.views.generic import ListView, DetailView, FormView
from .forms import UserPortfolioForm
# Create your views here.


class PortfolioUploadView(FormView):
    form_class = UserPortfolioForm
    template_name = 'portfolioUpload.html'
    model = Portfolio

    def get_form_kwargs(self, **kwargs):
        kwargs = super(PortfolioUploadView, self).get_form_kwargs()
        kwargs['portfolio'] = Portfolio.objects.get(id=self.kwargs['pk'])

        return kwargs

    def get_initial(self, **kwargs):
        initial = super(PortfolioUploadView, self).get_initial()
        initial['creator'] = self.request.user
        initial['portfolio'] = Portfolio.objects.get(id=self.kwargs['pk'])
        return initial

    def get_context_data(self, **kwargs):
        context = super(PortfolioUploadView, self).get_context_data(**kwargs)
        portfolio = Portfolio.objects.get(id=self.kwargs['pk'])
        context['portfolioForm'] = UserPortfolioForm(portfolio=portfolio, initial={'creator': self.request.user, 'portfolio': portfolio})
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            portfolio = Portfolio.objects.get(id=self.kwargs['pk'])
            form = UserPortfolioForm(portfolio, request.POST)
            if form.is_valid():
                form.save()
                return redirect('eval-list')
            else:
                print(form.errors)
                return redirect('portfolioUpload.html')
        return render(request, self.get_template_names())


class PortfolioListView(ListView):
    model = Portfolio
    queryset = Portfolio.objects.all()
    template_name = 'portfoliolist.html'

