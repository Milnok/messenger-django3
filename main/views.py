from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from messenger.settings import prime_Q, prime_P
from .functions import RSA, safe_transfer
from .models import friend, keys, message


def home(request):
    if request.user.is_authenticated:
        return redirect('friends')
    else:
        return render(request, 'home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'signupuser.html', {'Form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                new_keys = keys()
                new_keys.keys_user = user
                open_key, secret_key, none = RSA.RSA_gen(prime_P, prime_Q)
                new_keys.open_key, new_keys.secret_key = str(open_key), str(secret_key)
                new_keys.save()
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signupuser.html',
                              {'Form': UserCreationForm(), 'error': 'this user name already used'})
        else:
            return render(request, 'signupuser.html',
                          {'Form': UserCreationForm(), 'error': 'password did not match'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'Form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html',
                          {'Form': AuthenticationForm(), 'error': 'Логин и пароль не совпадают'})
        else:
            login(request, user)
            return redirect('home')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    else:
        logout(request)
        return redirect('home')


@login_required
def friends(request):
    friends_list = friend.objects.filter(user=request.user)
    return render(request, 'friends.html', {'friends': friends_list})


@login_required
def add_friend(request):
    if request.method == 'POST':
        error = ''
        try:
            search_friend = User.objects.get(username=request.POST['friend'])
            if request.user == search_friend:
                error = 'Вы не можете добавить самого себя в друзья'
            else:
                new_friend = friend()
                new_friend.user = request.user
                new_friend.users_friend = search_friend
                new_friend.save()
        except ObjectDoesNotExist:
            error = 'Пользователь не найден'
        except IntegrityError:
            error = 'Пользователь уже у вас в друзьях'
        friends_list = friend.objects.filter(user=request.user)
        return render(request, 'friends.html', {'error': error, 'friends': friends_list})


@login_required
def chat(request, friend_pk):
    if request.method == 'GET':
        all_messages = (message.objects.filter(sender=request.user) | message.objects.filter(receiver=request.user)).order_by('-date')[:5][::-1]
        messages_list = safe_transfer.from_server_to_client(all_messages)
        for i in range(len(messages_list)):
            all_messages[i].text = messages_list[i]
        return render(request, 'chat.html', {'friend': friend_pk, 'messages': all_messages})


@login_required
def send_message(request, friend_pk):
    if request.method == 'POST':
        receiver = get_object_or_404(User, pk=friend_pk)
        new_message = message()
        new_message.sender = request.user
        new_message.receiver = receiver

        clear_message = safe_transfer.from_client_to_server(request.POST['message'])
        new_message.text = clear_message

        new_message.save()
        return redirect('chat', friend_pk)