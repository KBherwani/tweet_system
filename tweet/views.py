from django.shortcuts import render, redirect

# Create your views here.
from django.utils import timezone
from django.views.generic import CreateView, TemplateView

from account.views import LoginRequired
from tweet.forms import TweetForm
from tweet.models import Tweet


class AddTweet(LoginRequired, CreateView):
    template_name = "tweet_form.html"
    form_class = TweetForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        return context

    def form_invalid(self, form):
        form = self.form_class(self.request.POST)
        return render(self.request, self.template_name, {'form': form})

    def form_valid(self, form):
        if form.is_valid():
            form = form.save(commit=False)
            form.user = self.request.user
            form.created_at = timezone.now()
            form.save()
        return redirect("account:home")

