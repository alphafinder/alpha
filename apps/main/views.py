import json

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
from apps.project.models import Project, ProjectRequest
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
        context.update(
            {'nav_projects': Project.objects.filter(collaborators__member=request.user).order_by("-created_at")[:7]})
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


def json_skills(tags=UserProfile.skills.all()):
    tag_list = []
    for i in range(len(tags)):
        tag = tags[i].name
        tag_list.append({"value": str(i), "text": tag})
    return json.dumps(tag_list, ensure_ascii=False).replace('\"', '"')


def index(request, projects_list=None, type='projects', sort='-created_at'):
    context = get_context(request, 'Лента Проектов')
    m = Messages()
    if projects_list is None:
        projects_list = Project.objects.filter(is_public=True).order_by("-created_at")

    page = request.GET.get('page', 1)
    paginator = Paginator(projects_list, 20)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        requested = [i.project for i in ProjectRequest.objects.filter(user=request.user, status=1)]
        context.update({'requested': requested})
    else:
        context.update({'requested' : []})

    context.update({'object_list': projects})
    context.update({'type': type})
    context.update({'sort': sort})
    try:
        skills = ["'" + n.name + "'" for n in request.user.profile.skills.all()]
        context.update({'skills': ", ".join(skills) })
    except AttributeError:
        pass
    if not request.user.is_authenticated:
        m.add(request, 'warning', 'Вы незарегистрированы в системе.')
        m.add(request, 'warning', 'Для отправки запросов тимлидам проектов и создания проектов, пожалуйста, зарегистрируйтесь или войдите')
    return render(request, 'index.html', context)


def search_engine(request):
    data = request.GET['q'].split('+')
    type = request.GET['type']
    sort = request.GET['sort']
    # TODO

    # print(sort)
    if type == 'projects':
        object_list = Project.objects.none()
        for i in data:
            s = Project.objects.filter(
                (Q(name__icontains=i) | Q(collaborators__member__username__contains=i)) & Q(
                    is_public=True))
            object_list |= s
            object_list = object_list.union(Project.objects.filter(tags__name__icontains=i).distinct())
    elif type == 'users':
        object_list = UserProfile.objects.none()
        if len(data) == 1 and data[0] == '':
            object_list |= UserProfile.objects.all()
        else:
            for i in data:
                s = UserProfile.objects.filter((Q(user__username__contains=i) | Q(user__first_name__contains=i) | Q(user__last_name__contains=i)))
                object_list |= s
                object_list = object_list.union(UserProfile.objects.filter(skills__name__icontains=i).distinct())
    page = request.GET.get('page', 1)
    context = get_context(request, f'Поиск | {data}')
    if type == 'projects':
        context.update({'object_list': object_list.order_by(sort)})
    else:
        context.update({'object_list' : object_list})
    context.update({'type': type})
    context.update({'value': ' '.join(data)})
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
