from tweet.models import Comment


def my_scheduled_job():
    Comment.objects.all().delete()

