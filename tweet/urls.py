from django.urls import path
from .views import *

app_name = "tweet"

urlpatterns = [
    path("tweet/", AddTweet.as_view(), name="tweet"),

]
