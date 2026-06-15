"""Представления приложения проектов"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from .models import Project, STATUS_ACTIVE, STATUS_CLOSED
from .forms import ProjectForm
from constants import PROJECTS_PER_PAGE, STATUS_400, STATUS_403
from utils import paginate_queryset


def project_list(request):
    """Главная страница со списком проектов"""
    projects = Project.objects.filter(status=STATUS_ACTIVE)
    projects_page = paginate_queryset(request, projects, PROJECTS_PER_PAGE)

    context = {
        'page_obj': projects_page,
        'is_paginated': projects_page.has_other_pages(),
    }
    return render(request, 'projects/project_list.html', context)


def project_detail(request, project_id):
    """Страница проекта"""
    project = get_object_or_404(Project, id=project_id)
    user_is_participant = (request.user.is_authenticated
                           and request.user in project.participants.all())
    user_is_owner = request.user == project.owner
    is_favorited = request.user.is_authenticated and project in request.user.favorites.all()

    context = {
        'project': project,
        'user_is_participant': user_is_participant,
        'user_is_owner': user_is_owner,
        'is_favorited': is_favorited,
    }
    return render(request, 'projects/project-details.html', context)


@login_required
@require_http_methods(['POST'])
def toggle_favorite(request, project_id):
    """Добавление/удаление из избранного"""
    project = get_object_or_404(Project, id=project_id)

    is_favorited = request.user.favorites.filter(id=project_id).exists()
    
    if is_favorited:
        request.user.favorites.remove(project)
    else:
        request.user.favorites.add(project)

    return JsonResponse({'status': 'ok', 'favorited': not is_favorited})


@login_required
def favorite_projects(request):
    """Страница избранных проектов"""
    projects = request.user.favorites.all()

    projects_page = paginate_queryset(request, projects, PROJECTS_PER_PAGE)

    context = {'projects': projects_page}
    return render(request, 'projects/favorite_projects.html', context)


@login_required
@require_http_methods(['POST'])
def complete_project(request, project_id):
    """Завершение проекта"""
    project = get_object_or_404(Project, id=project_id, owner=request.user)

    if request.user != project.owner:
        return JsonResponse({
            'status': 'error', 
            'message': 'Только автор может завершить проект'
        }, status=STATUS_403)
    
    # Затем проверяем статус
    if project.status == STATUS_ACTIVE:
        project.status = STATUS_CLOSED
        project.save()
        return JsonResponse({'status': 'ok', 'project_status': project.status})

    return JsonResponse({
        'status': 'error', 
        'message': 'Проект уже завершён'
    }, status=STATUS_400)


@login_required
@require_http_methods(['POST'])
def toggle_participate(request, project_id):
    """Присоединение/отказ от участия в проекте"""
    project = get_object_or_404(Project, id=project_id)

    # Нельзя участвовать в своём проекте
    if request.user == project.owner:
        return JsonResponse({
            'status': 'error',
            'message': 'Вы автор проекта'
        }, status=STATUS_400)

    is_participant = project.participants.filter(id=request.user.id).exists()
    # Добавляем или удаляем участника
    if is_participant:
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)

    return JsonResponse({
        'status': 'ok',
        'participated': not is_participant,
        'participants_count': project.participants.count()
    })


@login_required
def create_project(request):
    """Создание проекта"""
    form = ProjectForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'projects/create-project.html', {
            'form': form,
            'is_edit': False
        })
        
    project = form.save(commit=False)
    project.owner = request.user
    project.save()
    project.participants.add(request.user)  # Автор автоматически участник
    return redirect('projects:project_detail', project_id=project.id)


@login_required
def edit_project(request, project_id):
    """Редактирование проекта"""
    project = get_object_or_404(Project, id=project_id, owner=request.user)

    if project.owner != request.user:
        messages.error(request, 'Вы не можете редактировать чужой проект')
        return redirect('projects:project_detail', project_id=project.id)
    
    form = ProjectForm(request.POST or None, instance=project)
    if not form.is_valid():
        return render(request, 'projects/create-project.html', {
            'form': form,
            'is_edit': True,
            'project': project
        })

    form.save()
    return redirect('projects:project_detail', project_id=project.id)
