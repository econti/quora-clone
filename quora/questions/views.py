from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponse
from quora.questions.models import Question, Tag, QuestionComment, UserUpvote
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from quora.questions.forms import QuestionForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from quora.decorators import ajax_required
import markdown
from django.template.loader import render_to_string
from quora.questions.lib.decorators import ajax_login_required
import ujson

def _questions(request, questions):
    paginator = Paginator(questions, 10)
    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    popular_tags = Tag.get_popular_tags()
    top_users = list(User.objects.filter(is_active=True))
    top_users.sort(key=lambda x: x.questioncomment_set.count(), reverse=True)
    return render(
        request,
        'questions/questions.html',
        {'questions': questions, 'popular_tags': popular_tags, 'users': top_users},
    )

def questions(request):
    all_questions = Question.get_published()
    return _questions(request, all_questions)

def question(request, slug):
    question = get_object_or_404(Question, slug=slug, status=Question.PUBLISHED)
    return render(request, 'questions/question.html', {'question': question})

def tag(request, tag_name):
    tags = Tag.objects.filter(tag=tag_name)
    questions = []
    for tag in tags:
        if tag.question.status == Question.PUBLISHED:
            questions.append(tag.question)
    return _questions(request, questions)

@login_required
def write(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = Question()
            question.create_user = request.user
            question.title = form.cleaned_data.get('title')
            question.content = form.cleaned_data.get('content')
            status = form.cleaned_data.get('status')
            if status in [Question.PUBLISHED, Question.DRAFT]:
                question.status = form.cleaned_data.get('status')
            question.save()
            tags = form.cleaned_data.get('tags')
            question.create_tags(tags)
            return redirect('/questions/')
    else:
        form = QuestionForm()
    return render(request, 'questions/write.html', {'form': form})

@login_required
def drafts(request):
    drafts = Question.objects.filter(create_user=request.user, status=Question.DRAFT)
    return render(request, 'questions/drafts.html', {'drafts': drafts})

@login_required
def edit(request, id):
    tags = ''
    if id:
        question = get_object_or_404(Question, pk=id)
        for tag in question.get_tags():
            tags = u'{0} {1}'.format(tags, tag.tag)
        tags = tags.strip()
    else:
        question = Question(create_user=request.user)

    if request.POST:
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('/questions/')
    else:
        form = QuestionForm(instance=question, initial={'tags': tags})
    return render(request, 'questions/edit.html', {'form': form})


@login_required
@ajax_required
def preview(request):
    try:
        if request.method == 'POST':
            content = request.POST.get('content')
            html = 'Nothing to display :('
            if len(content.strip()) > 0:
                html = markdown.markdown(content, safe_mode='escape')
            return HttpResponse(html)
        else:
            return HttpResponseBadRequest()
    except Exception, e:
        return HttpResponseBadRequest()


@ajax_login_required
def comment(request):
    try:
        if request.method == 'POST':
            question_id = request.POST.get('question')
            question = Question.objects.get(pk=question_id)
            comment = request.POST.get('comment')
            comment = comment.strip()
            if len(comment) > 0:
                question_comment = QuestionComment(user=request.user, question=question, comment=comment)
                question_comment.save()
            html = u''
            for comment in question.get_comments():
                html = u'{0}{1}'.format(html, render_to_string('questions/partial_question_comment.html', {'comment': comment}))
            return HttpResponse(html)
        else:
            return HttpResponseBadRequest()
    except Exception, e:
        return HttpResponseBadRequest()


@ajax_login_required
def vote(request):
    user = request.user
    comment_id = request.POST['comment']
    comment = QuestionComment.objects.get(pk=comment_id)
    upvote = UserUpvote.objects.filter(comment=comment, user=user).first()
    if upvote is None:
        comment.upvotes += 1
        comment.save()
        new_upvote = UserUpvote(comment=comment, user=user)
        new_upvote.save()
        return HttpResponse(
            ujson.dumps({'upvotes': comment.upvotes, 'highlight': True})
        )
    else:
        existing_upvote = UserUpvote.objects.filter(comment=comment, user=user).first()
        existing_upvote.delete()
        comment.upvotes -= 1
        comment.save()
        return HttpResponse(
            ujson.dumps({'upvotes': comment.upvotes, 'highlight': False})
        )
