from django.contrib import admin

# Register your models here.
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe

from TweetManagement import settings
from tweet.models import TweetCategory, Tweet, Comment

change_form_template = "admin/tweet_change_list.html"


class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'tweet',
        'content',
        'visibility',
        'parent',
        'timestamp',

    ]


class TweetCategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]


class TweetAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'title',
        'category',
        'tweet',
        'created_at',
        'approval'
    ]


admin.site.register(Tweet, TweetAdmin)
admin.site.register(TweetCategory, TweetCategoryAdmin)
admin.site.register(Comment, CommentAdmin)
