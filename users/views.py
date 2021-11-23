from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserOurReg
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test


def not_agent(user):
    if user:
        return user.groups.filter(name='agent').count() == 0
    return False

@login_required
@user_passes_test(not_agent)
def register(request):
    if request.method == "POST":
        form = UserOurReg(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            user.profile.super_id = request.user.id
            user.profile.name = form.cleaned_data.get('name')
            user.profile.save()
            agent_group = Group.objects.get(name='agent')
            agent_group.user_set.add(user)
            messages.success(request, f'Пользователь {username} успешно создан')
            return redirect('/')
    else:
        form = UserOurReg()
    return render(request, 'users/registration.html', {'form': form})
