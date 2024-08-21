from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from detectionsite import settings
from .forms import LoginForm, UserRegisration, UserEditForm, ProfileEditForm, TokenLoginForm
from .models import Profile
import requests
import jwt

# Create your views here.


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, "account/login.html", context={"form": form})


def token_is_expired(token):
    try:

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        exp = payload.get('exp')
        if exp:
            return datetime.fromtimestamp(exp) < datetime.now()
    except jwt.ExpiredSignatureError:
        return True
    except jwt.DecodeError:
        return True
    return False


@login_required
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('account:login')
    return render(request,'account/dashboard.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegisration(request.POST)
        if user_form.is_valid():
            # Создает новый объект пользователя, не сохраняет его
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Сохраняет юзера
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegisration()
    return render(request, 'account/register.html',
                  {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
            instance=request.user.profile)
    return render(request, 'account/edit.html',
                      {'user_form': user_form, 'profile_form': profile_form})


@login_required
def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, 'account/profile_list.html',{'profiles': profiles})

@login_required
def profile_detail(request,username):
    profile = get_object_or_404(Profile, user__username=username)
    return render(request, 'account/profile_detail.html',{'profile':profile})


def token_login(request):
    if request.method == 'POST':
        form = TokenLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Получение токена
            token_url = 'http://127.0.0.1:8000/api/token/'
            user_data = {
                'username': username,
                'password': password
            }
            response = requests.post(token_url, data=user_data)

            if response.status_code == 200:
                tokens = response.json()
                access_token = tokens['access']
                refresh_token = tokens['refresh']

                # Сохраняет токен
                request.session['access_token'] = access_token
                request.session['refresh_token'] = refresh_token

                # Отладка: вывод токена в консоль
                print(f"Access Token: {access_token}")
                print(f"Refresh Token: {refresh_token}")
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)  # Вход пользователя в сессию
                    return redirect("account:dashboard")

            else:
                return render(request, 'account/token_login.html', {'form': form, 'error': 'Invalid credentials'})

    else:
        form = TokenLoginForm()

    return render(request, 'account/token_login.html', {'form': form})


def refresh_access_token(request):
    refresh_token = request.session.get('refresh_token')
    if refresh_token:
        response = requests.post('http://127.0.0.1:8000/api/token/refresh/', data={'refresh': refresh_token})
        if response.status_code == 200:
            tokens = response.json()
            request.session['access_token'] = tokens['access']
            return True  # Успешное обновление
    return False  # Не удалось обновить токен