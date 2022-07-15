from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from TweetManagement import settings


# Create your models here.

class TweetCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Tweet(models.Model):
    APPROVAL_CHOICE = (
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("pending", "Pending"),

    )
    START_REGEX = RegexValidator(r'^[A-Za-z]*$',
                                 'Tweet must start with Character')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    category = models.ForeignKey(TweetCategory, on_delete=models.CASCADE)
    tweet = models.TextField(validators=[START_REGEX])
    created_at = models.DateTimeField()
    expiry_at = models.DateTimeField(null=True,blank=True)
    approval = models.CharField(
        max_length=20,
        choices=APPROVAL_CHOICE,
        default='pending'
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    VISIBILITY_CHOICE = (
        ("show", "SHOW"),
        ("hidden", "HIDDEN"),

    )
    timestamp = models.DateTimeField(auto_now_add=True)
    tweet = models.ForeignKey(Tweet, related_name='tweet_comments',
                              blank=True, null=True,
                              on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    reply = models.ForeignKey("self",blank=True,null=True,
                              on_delete=models.CASCADE,
                              related_name='comments_reply')
    visibility = models.CharField(
        max_length=20,
        choices=VISIBILITY_CHOICE,
        default='show'
    )

    parent = models.BooleanField(default=False)

