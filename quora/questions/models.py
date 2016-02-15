import markdown
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from datetime import datetime
from django.template.defaultfilters import slugify


class Question(models.Model):
    DRAFT = 'D'
    PUBLISHED = 'P'
    STATUS = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    content = models.TextField(max_length=4000, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS, default=DRAFT)
    create_user = models.ForeignKey(User)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)
    update_user = models.ForeignKey(User, null=True, blank=True, related_name="+")

    class Meta:
        db_table = '"questions"'
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ("-create_date",)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Question, self).save(*args, **kwargs)
        else:
            self.update_date = datetime.now()
        if not self.slug:
            slug_str = "%s" % (self.title.lower())
            self.slug = slugify(slug_str)
        super(Question, self).save(*args, **kwargs)

    def get_content_as_markdown(self):
        return markdown.markdown(self.content, safe_mode='escape')

    @staticmethod
    def get_published():
        questions = Question.objects.filter(status=Question.PUBLISHED)
        return questions

    def create_tags(self, tags):
        tags = tags.strip()
        tag_list = tags.split(' ')
        for tag in tag_list:
            if tag:
                t, created = Tag.objects.get_or_create(tag=tag.lower(), question=self)

    def get_tags(self):
        return Tag.objects.filter(question=self)

    def get_summary(self):
        if len(self.content) > 255:
            return u'{0}...'.format(self.content[:255])
        else:
            return self.content

    def get_summary_as_markdown(self):
        return markdown.markdown(self.get_summary(), safe_mode='escape')

    def get_comments(self):
        """Returns comments sorted by upvotes and then by date"""
        comments = QuestionComment.objects.filter(question=self)
        comments = [comment for comment in comments]
        comments.sort(key=lambda x: (x.upvotes, x.date), reverse=True)
        return comments

    def get_num_comments(self):
        return len(QuestionComment.objects.filter(question=self))

    def get_top_comment(self):
        max_upvotes = QuestionComment.objects.filter(question=self).aggregate(models.Max('upvotes'))['upvotes__max']
        top_comment = QuestionComment.objects.filter(upvotes=max_upvotes).first()
        if top_comment:
            return {
                'content': markdown.markdown(top_comment.comment, safe_mode='escape'),
                'ts': top_comment.date,
                'user': top_comment.user,
            }
        return None


class Tag(models.Model):
    tag = models.CharField(max_length=50)
    question = models.ForeignKey(Question)

    class Meta:
        db_table = '"tags"'
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        unique_together = (('tag', 'question'),)
        index_together = [['tag', 'question'],]

    def __unicode__(self):
        return self.tag

    @staticmethod
    def get_popular_tags():
        tags = Tag.objects.all()
        count = {}
        for tag in tags:
            if tag.question.status == Question.PUBLISHED:
                if tag.tag in count:
                    count[tag.tag] = count[tag.tag] + 1
                else:
                    count[tag.tag] = 1
        sorted_count = sorted(count.items(), key=lambda t: t[1], reverse=True)
        return sorted_count[:20]


class QuestionComment(models.Model):
    question = models.ForeignKey(Question)
    comment = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    upvotes = models.IntegerField(default=0)

    class Meta:
        db_table = '"answers"'
        verbose_name = _("Question Comment")
        verbose_name_plural = _("Question Comments")
        ordering = ("date",)

    def __unicode__(self):
        return u'{0} - {1}'.format(self.user.username, self.question.title)

    def get_comment_as_markdown(self):
        return markdown.markdown(self.comment, safe_mode='escape')

    def get_up_voters(self):
        upvotes = UserUpvote.objects.filter(comment=self)
        upvote_users = [upvote.user.id for upvote in upvotes]
        return upvote_users


class UserUpvote(models.Model):
    user = models.ForeignKey(User)
    comment = models.ForeignKey(QuestionComment)

    class Meta:
        db_table = '"upvotes"'
