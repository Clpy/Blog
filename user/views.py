from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import LoginForm, RegForm
from django.urls import reverse
from django.http import JsonResponse


def login_for_modal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def login(request):
    if request.method == 'POST':  # 如果是提交数据
        login_form = LoginForm(request.POST)  # 提交数据是否有效
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('index')))

    else:  # 其他是加载页面的行为
        login_form = LoginForm()

    context = {
        'login_form': login_form
    }
    return render(request, 'login.html', context)


def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            password = reg_form.cleaned_data['password']
            email = reg_form.cleaned_data['email']
            # 创建用户
            user = User.objects.create_user(username,password,email)
            user.save()
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('form', reverse('index')))  # 跳转到注册之前的页面
    else:
        reg_form = RegForm()

    context = {
        'reg_form': reg_form
    }
    return render(request, 'register.html', context)


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('index')))


def user_info(request):
    return render(request, 'user_info.html', context={})