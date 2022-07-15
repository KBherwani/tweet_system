from django import forms

from tweet.models import Tweet, Comment


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = [
            "title",
            "category",
            "tweet",
        ]


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'id': 'message',

            }
        )
    )

    class Meta:
        model = Comment
        fields = ['content']
