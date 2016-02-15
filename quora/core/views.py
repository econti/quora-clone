from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from quora.questions.models import Question
from django.contrib.auth.decorators import login_required
from quora.core.forms import ProfileForm, ChangePasswordForm
from django.contrib import messages
from django.conf import settings as django_settings
import os

from django.shortcuts import render_to_response
from django.template.context import RequestContext

def home(request):
    if request.user.is_authenticated():
        return redirect('/questions/')
    else:
        all_questions = Question.get_published()[:10]
        return render(request, 'core/splash.html', {'questions': all_questions})

def fblogin(request):
   context = RequestContext(request,
                           {'request': request,
                            'user': request.user})
   return render_to_response('core/fblogin.html',
                             context_instance=context)

def hidden_login(request):
    return render(request, 'core/cover.html')

@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.email = form.cleaned_data.get('email')
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Your profile were successfully edited.')
    else:
        form = ProfileForm(instance=user, initial={
            'email': user.email
            })
    return render(request, 'core/profile.html', {'form':form})

def public_profile(request, id):
    public_user = User.objects.filter(id=id).first()
    return render(request, 'core/public_profile.html', {'public_user': public_user})

@login_required
def settings(request):
    user = request.user
    return render(request, 'core/activity.html')

@login_required
def picture(request):
    uploaded_picture = False
    try:
        if request.GET.get('upload_picture') == 'uploaded':
            uploaded_picture = True
    except Exception, e:
        pass
    return render(request, 'core/picture.html', {'uploaded_picture': uploaded_picture})

@login_required
def password(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Your password were successfully changed.')
    else:
        form = ChangePasswordForm(instance=user)
    return render(request, 'core/password.html', {'form':form})

@login_required
def upload_picture(request):
    pass

@login_required
def save_uploaded_picture(request):
    try:
        x = int(request.POST.get('x'))
        y = int(request.POST.get('y'))
        w = int(request.POST.get('w'))
        h = int(request.POST.get('h'))
        tmp_filename = django_settings.MEDIA_ROOT + '/profile_pictures/' + request.user.username + '_tmp.jpg'
        filename = django_settings.MEDIA_ROOT + '/profile_pictures/' + request.user.username + '.jpg'
        im = Image.open(tmp_filename)
        cropped_im = im.crop((x, y, w+x, h+y))
        cropped_im.thumbnail((200, 200), Image.ANTIALIAS)
        cropped_im.save(filename)
        os.remove(tmp_filename)
    except Exception, e:
        pass
    return redirect('/settings/picture/')
