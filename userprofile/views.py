from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from .models import Profile


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            data = user_login_form
            print(data['username'])
            print(data['password'])
            print(request.POST.get('username'))
            user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            if user:
                login(request, user)
                return redirect('article:article_list')
            else:
                return HttpResponse("账号或密码输入错误，请重新输入~")
        else:
            return HttpResponse('账号或密码输入不合法')

    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse('请使用GET或POST请求数据')


def user_logout(request):
    logout(request)
    return redirect('article:article_list')


def user_register(request):
    if request.method == 'POST':
        data = request.POST
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('article:article_list')
        else:
            return HttpResponse('注册信息填写有误，请重新输入！')
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse('请使用GET或POST请求数据！')


@login_required(login_url='/userprofile/login/')
def user_delete(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        if request.user == user:
            logout(request)
            user.delete()
            return redirect('article:article_list')
        else:
            return HttpResponse('当前无删除操作权限')
    else:
        return HttpResponse('仅接受POST请求！')


@login_required(login_url='/userprofile/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user_id=id)
    if request.method == 'POST':
        print('post1')
        if request.user != user:
            return HttpResponse('当前无修改权限')
        profile_form = ProfileForm(data=request.POST)
        if profile_form.is_valid():
            print('valid')
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']
            profile.save()
            print(id)
            return redirect('user:edit', id=id)
        else:
            profile_cd = profile_form.cleaned_data
            print(profile_cd)
            print(profile_cd['phone'])
            return HttpResponse('注册表单有误，请重新输入！')
    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = {'profile_form': profile_form, 'profile': profile, 'user': user}
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse('请使用POST或GET请求数据')
