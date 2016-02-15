import os.path
import urllib, hashlib

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django.conf import settings

from quora.questions.models import Question, QuestionComment


class Profile(models.Model):
    user = models.OneToOneField(User)
    url = models.CharField(max_length=500, null=True, blank=True)
    dollars_earned = models.FloatField(default=0.00)

    class Meta:
        db_table = '"profiles"'

    def get_activity(self):
        """Returns sorted list of tuples:
            (created_at, content, question_slug, type)
        """
        activity = []
        for question in Question.objects.filter(create_user=self.user.id):
            activity.append(
                (question.create_date, question.title, question.slug, 'q')
            )
        for comment in QuestionComment.objects.filter(user=self.user):
            activity.append(
                (comment.date,
                 comment.get_comment_as_markdown()[0:200] + '...',
                 comment.question.slug,
                 'c')
            )

        sorted(activity, key=lambda x: x[1])
        return activity

    def get_url(self):
        url = self.url
        if "http://" not in self.url and "https://" not in self.url and len(self.url) > 0:
            url = "http://" + str(self.url)
        return url

    def get_picture(self):
        return self.url or 'https://qsf.is.quoracdn.net/-72c091d25b3e045b.png'

    def get_private_screen_name(self):
        return self.user.first_name or 'Anon'

    def get_non_private_screen_name(self):
        return self.user.first_name or self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
