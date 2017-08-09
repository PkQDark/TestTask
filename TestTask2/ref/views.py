from .models import ReferalUser, ReferalNumber
from django.contrib.auth.forms import UserCreationForm
from .forms import AddSystemUserForm, ReferalNumberForm, EmailForm
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import login, logout, authenticate
import random
from django.contrib.auth.decorators import login_required


def login_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/tables/')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        cur_user = authenticate(username=username, password=password)
        if cur_user is not None:
            login(request, cur_user)
            return HttpResponseRedirect('/tables/')
        else:
            messages.add_message(request, messages.ERROR, 'Неверный логин/пароль.')
    return render(request, 'index.html')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def check_fives_user():
    all_users = ReferalUser.objects.all()
    if len(all_users) >= 5:
        return False
    else:
        return True


def register(request):
    ref_num = 0
    if request.GET.get('ref_num'):
        ref_num = int(request.GET.get('ref_num'))
    if ref_num:
        try:
            ref_number = ReferalNumber.objects.get(link=ref_num)
            if request.method == 'POST':
                general = UserCreationForm(request.POST)
                additional = AddSystemUserForm(request.POST)
                if general.is_valid() and additional.is_valid():
                    e_mail = additional.cleaned_data['email']
                    if len(User.objects.filter(email=e_mail)):
                        messages.add_message(request, messages.ERROR,
                                             'Пользователь с почтовым ящиком ' + e_mail + ' уже зарегистрирован')
                    else:
                        user = general.save()
                        user.first_name = additional.cleaned_data['first_name']
                        user.last_name = additional.cleaned_data['last_name']
                        user.email = e_mail
                        user.is_staff = True
                        user.save()
                        email = ''
                        if request.GET.get('email'):
                            email = str(request.GET.get('email'))
                        ref_user = ReferalUser(user_stat=user,
                                               referal=email)
                        ref_user.save()
                        ref_number.activate_link(joiner=ref_user)
                        messages.add_message(request, messages.SUCCESS,
                                             'Пользователь успешно зарегистрирован')
                        return HttpResponseRedirect('/')
            else:
                general = UserCreationForm()
                additional = AddSystemUserForm()
            return render(request, 'ref/reg.html',
                          {'general': general, 'additional': additional})
        except ReferalNumber.DoesNotExist:
            messages.add_message(request, messages.WARNING, 'Извините, но реферальная ссылка, не существует')
    else:
        if check_fives_user():
            if request.method == 'POST':
                general = UserCreationForm(request.POST)
                additional = AddSystemUserForm(request.POST)
                if general.is_valid() and additional.is_valid():
                    e_mail = additional.cleaned_data['email']
                    if len(User.objects.filter(email=e_mail)):
                        messages.add_message(request, messages.ERROR,
                                             'Пользователь с почтовым ящиком ' + e_mail + ' уже зарегистрирован')
                        return HttpResponseRedirect('/tables/')
                    else:
                        user = general.save()
                        user.first_name = additional.cleaned_data['first_name']
                        user.last_name = additional.cleaned_data['last_name']
                        user.email = e_mail
                        user.is_staff = True
                        user.save()
                        if additional.cleaned_data['link']:
                            l = ReferalNumber.objects.get(link=additional.cleaned_data['link'])
                            ref_u = ReferalUser(user_stat=user, referal=l.ref_user.user_stat.email)
                            l.activate_link(joiner=l.ref_user)
                        else:
                            ref_u = ReferalUser(user_stat=user)
                        ref_u.save()
                        messages.add_message(request, messages.SUCCESS,
                                             'Пользователь успешно зарегистрирован')
                        return HttpResponseRedirect('/tables/')
            else:
                general = UserCreationForm()
                additional = AddSystemUserForm()
            return render(request, 'ref/reg.html',
                          {'general': general, 'additional': additional})
        else:
            if request.method == 'POST':
                ref_form = ReferalNumberForm(request.POST)
                messages.add_message(request, messages.WARNING, 'Введите номер, или перейдите по ссылке в письме')
                if ref_form.is_valid():
                    refer_num = ref_form.cleaned_data['referal_number']
                    try:
                        ref_obj = ReferalNumber.objects.get(link=refer_num)
                        joiner = ReferalUser.objects.get(referalnumber__link=refer_num)
                        ref_obj.activate_link(joiner=joiner)
                    except ReferalNumber.DoesNotExist:
                        messages.add_message(request, messages.WARNING, 'Извините, но реферальная ссылка, не существует')
                        return HttpResponseRedirect('/')
                    referal = ReferalUser.objects.get(referalnumber__link=refer_num)
                    return HttpResponseRedirect('/register/?ref_num=' + str(refer_num) + '&email=' + str(referal.user_stat.email))
            else:
                ref_form = ReferalNumberForm()
            return render(request, 'ref/ref_link.html',
                          {'ref_form':ref_form})


@login_required
def generate_referal(request):
    u = request.user
    cur_user = ReferalUser.objects.get(user_stat=u)
    try:
        cur_link = ReferalNumber.objects.get(ref_user=cur_user)
    except ReferalNumber.DoesNotExist:
        ref = random.randint(1, 10000)
        cur_link = ReferalNumber(ref_user=cur_user, link=ref)
        cur_link.save()
    if request.method == 'POST':
        email_form = EmailForm(request.POST)
        if email_form.is_valid():
            ref_link = 'Перейдите пожалуйста по ссылке, для продолжения регистрации http:/127.0.0.1:8000/register?ref_' \
                       'num=' + str(cur_link.link) + '&email=' + str(cur_user.user_stat.email)
            send_mail('Register', ref_link, 'vladyslavponomaryov@gmail.com',
                      [email_form.cleaned_data['email']], fail_silently=False)
            messages.add_message(request, messages.SUCCESS, 'Письмо отправлено')
            return HttpResponseRedirect('/tables/')
    else:
        email_form = EmailForm()
    return render(request, 'ref/gen_ref.html',
                      {'email_form': email_form, 'link': cur_link.link})

@login_required
def top10(request):
    all_users = ReferalUser.objects.all().order_by('-point')
    if len(all_users) > 10:
        all_users = all_users[:10]
    return render(request, 'ref/top.html', {'top': all_users})


@login_required
def tables(request):
    u = request.user
    try:
        user = ReferalUser.objects.get(user_stat=u)
    except ReferalUser.DoesNotExist:
        user = None
    try:
        my_ref = ReferalUser.objects.get(user_stat__email=user.referal)
    except ReferalUser.DoesNotExist:
        my_ref = None
    except AttributeError:
        my_ref = None
    referals = ReferalUser.objects.filter(referal=user.user_stat.email)
    return render(request, 'ref/tables.html', {'referals': referals, 'my_ref': my_ref})
