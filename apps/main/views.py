import json

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from apps.project.models import Project
from django.contrib.auth.models import User
from apps.user.models import UserProfile

from django.db.models import Q

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_context(request, pagename):
    context = {
        'pagename': pagename,
    }
    context.update({'user': request.user})
    if request.user.is_authenticated:
        context.update({'nav_projects' : Project.objects.filter(collaborators__member=request.user).order_by("-created_at")})
    # TEMP FIX OF MISSING MEDIA_URL AND STATIC_URL
    # context.update({'BASE_DIR': settings.BASE_DIR})
    return context


def ajax_messages(request):
    django_messages = []

    for message in messages.get_messages(request):
        django_messages.append({
            "level": settings.MESSAGE_TAGS[message.level],
            "message": message.message,
            "extra_tags": message.tags,
        })

    return django_messages


def json_skills(tags = UserProfile.skills.all()):
    tag_list = []
    for i in range(len(tags)):
        tag = tags[i].name
        tag_list.append({ "value" : str(i), "text" : tag })
    return json.dumps(tag_list, ensure_ascii=False).replace('\"','"')


def index(request, projects_list=None, type='projects', sort='-created_at'):
    if request.user.is_authenticated:
        context = get_context(request, 'Dashboard')
        # print(request.user.profile)
        # context.update({'projects': Project.objects.all()})

        # arguments = {'template_name' : 'concat_reset.html',
        #         'link' : 'http://127.0.0.1:8000/',
        #         'unsub' : 'http://127.0.0.1:8000/',
        #         'domain' : 'concat.org'}

        # user = User.objects.get(username=request.user.username)
        # github_login = user.social_auth.get(provider='github')
        # user.profile.reset_password()
        # print(user.profile.github_stars)
        if projects_list is None:
            projects_list = Project.objects.all().order_by("-created_at")

        page = request.GET.get('page', 1)
        paginator = Paginator(projects_list, 20)
        try:
            projects = paginator.page(page)
        except PageNotAnInteger:
            projects = paginator.page(1)
        except EmptyPage:
            projects = paginator.page(paginator.num_pages)

        context.update({'object_list' : projects})
        context.update({'type' : type})
        context.update({'sort' : sort})


        return render(request, 'index.html', context)
    else:
        context = get_context(request, 'greetings')
        return redirect('account/login')



def search_engine(request):

    data = request.GET['q'].split('+')
    type = request.GET['type']
    sort = request.GET['sort']
    #TODO

    projects_list = Project.objects.none()
    if type == 'projects':
        for i in data:
            s = Project.objects.filter(Q(name__icontains=i) | Q(tags__name=i)).order_by(sort)
            projects_list |= s

    page = request.GET.get('page', 1)
    paginator = Paginator(projects_list, 1000)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)

    context = get_context(request, 'Dashboard')
    context.update({'object_list' : projects})
    context.update({'type' : type})
    context.update({'value' : ' '.join(data)})
    context.update({'sort': sort})

    return render(request, 'search.html', context)









class Messages():
    def __init__(self):
        pass

    def parse_messages(self, st):
        msgs = {}
        for k in st.keys():
            if k != 'inactive':
                if k == 'invalid_login':
                    msgs.update({'error': 'Неправильный логин/пароль'})
                else:
                    msgs.update({'error': st[k]})
        return msgs

    def add(self, request, level, message):
        if level == 'error':
            messages.error(request, message, extra_tags='safe')
        elif level == 'warning':
            messages.warning(request, message, extra_tags='safe')
        elif level == 'success':
            messages.success(request, message, extra_tags='safe')
        elif level == 'info':
            messages.info(request, message, extra_tags='safe')