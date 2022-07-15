from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import AccessMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import FormView, TemplateView, UpdateView, View, \
    DetailView, ListView

from tweet.forms import CommentForm
from tweet.models import Tweet
from .forms import SignUpForm, UserLoginForm
from .token import account_activation_token

User = get_user_model()


class LoginRequired(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account:login")
        return super().dispatch(request, *args, **kwargs)


class HomeView(TemplateView):
    template_name = "home.html"
    model = Tweet

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data()
        comment = CommentForm()
        tweet_obj = Tweet.objects.filter(approval='approved')
        context['tweets'] = tweet_obj
        context['comment_form'] = comment
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if 'comment_id' in self.request.POST:
            obj = form.save(commit=False)
            obj.reply_id = self.request.POST.get('comment_id')
            obj.tweet_id = self.request.POST.get('tweet_id')
            obj.timestamp = timezone.now()
            obj.visibility = 'hidden'
            obj.save()
        else:
            obj = form.save(commit=False)
            obj.tweet_id = self.request.POST.get('tweet_id')
            obj.timestamp = timezone.now()
            obj.parent = True
            obj.save()
        return self.get(request)


class SignUpView(View):
    form_class = SignUpForm
    template_name = "signup.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = "Activate Your MySite Account"
            message = render_to_string(
                "account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(subject, message)

            messages.success(
                request, ("Please Confirm your email to complete registration.")
            )

            return redirect("account:login")

        return render(request, self.template_name, {"form": form})


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user,
                                                                     token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            messages.success(request, ("Your account have been confirmed."))
            return redirect("account:login")
        else:
            messages.warning(
                request,
                (
                    "The confirmation link was invalid, possibly because it has already been used."
                ),
            )
            return redirect("account:home")


class LoginView(FormView):
    form_class = UserLoginForm
    template_name = "login.html"

    def form_valid(self, form):
        user = form.cleaned_data
        user.backend = "django.contrib.auth.backends.ModelBackend"
        login(self.request, user)
        return redirect("account:home")

    def form_invalid(self, form):
        messages.error(self.request,
                       'Your account is Inactive. Please check your registered email for account activation.')
        return super().form_invalid(form)


class LogoutView(FormView):
    def get(self, *args, **kwargs):
        logout(self.request)
        messages.success(self.request, "User logged out successfully.")
        return redirect("account:login")
