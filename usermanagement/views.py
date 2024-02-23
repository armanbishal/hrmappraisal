import json

from django.contrib import messages
from django.shortcuts import render
from django import forms
from django.shortcuts import render, redirect
from usermanagement.forms import LoginForm, PrivilegedForm
from usermanagement.models import *
import datetime, time
from datetime import datetime, date
import json
import requests
from django.conf import settings
from usermanagement.decorators import *

def login(request):
    if 'logged_in' in request.session:
        if request.session['logged_in'] is True:
            return redirect('usermanagement:dashboard')
    else:
        form = LoginForm
        return render(request, 'user/login.html', {'form': form})


def login_validate(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        username = form['username'].value()
        password = form['password'].value()
        try:

            user = User.objects.get(username=username)
            if user:
                if user.username == username.upper():
                    groupid = user.group.split(',')
                    request.session['logged_in'] = True
                    request.session['username'] = user.username
                    request.session['firstname'] = user.first_name
                    request.session['id'] = user.pk
                    request.session['group_id'] = groupid
                    request.session['employee'] = user.employee
                    logindate = datetime.now()
                    Log.objects.create(
                        user_id=request.session['id'],
                        date_time=logindate,
                        login_data=logindate,
                        action='1',
                        component='login',
                        ip=request.META.get('REMOTE_ADDR')
                        # ip=request.META.get('HTTP_X_REAL_IP')
                    )
                    # messages.success(request, "Successfully Logged In")
                    return redirect("usermanagement:dashboard")
                else:
                    messages.error(request, 'Incorrect  User name  or Password')
                    return redirect('usermanagement:login')
            else:
                obj = {
                    "username": username,
                    "password": password
                }
                payload = json.dumps(obj)
                headers = {'Content-Type': 'application/json'}
                try:
                    re = requests.post(settings.HRMLOGIN, data=payload, headers=headers)
                    ress = re.json()
                    # print(ress)
                    if ress["isLoginSuccess"] == True:
                        user = User.objects.get(username=username.upper(), is_active=1)
                        groupid = user.group.split(',')
                        request.session['logged_in'] = True
                        request.session['username'] = user.username
                        request.session['firstname'] = user.first_name
                        request.session['id'] = user.pk
                        request.session['group_id'] = groupid
                        request.session['employee'] = user.employee
                        logindate = datetime.now()
                        Log.objects.create(
                            user_id=request.session['id'],
                            date_time=logindate,
                            login_data=logindate,
                            action='1',
                            component='login',
                            ip=request.META.get('REMOTE_ADDR')
                            # ip=request.META.get('HTTP_X_REAL_IP')
                        )
                        return redirect("usermanagement:dashboard")
                    else:
                        messages.error(request, 'Incorrect  User name  or Password')
                        return redirect('usermanagement:login')
                except Exception as e:
                    print(e)
                    messages.error(request, 'Smart Enterprise Connection Error!')
                    return redirect('usermanagement:login')
        except Exception as e:
            print(e)
            messages.error(request, 'Account is not active. Please contact HR.')
            return redirect('usermanagement:login')
    else:
        return render(request, 'user/login.html', {'form': form})


def dashboard(request):
    module = list()
    user = User.objects.get(id=request.session['id'])
    user_permissions = Privileged.objects.filter(group_id=user.group)
    module = Privileged.objects.filter(group_id=user.group).values('module_type_id').distinct()
    list_result = [entry for entry in module]
    request.session['module'] = list_result
    try:
        urls = list()
        for p in user_permissions:
            userurl = Moduleurl.objects.filter(id=p.moduleurl_id)
            for url in userurl:
                urls.append(url.url)
                request.session['urls'] = urls
    except:
        user = None
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'firstname': request.session['firstname'],
        'urls': urls,
        'module': module,
    }
    context = {'data': userdata}
    return render(request, 'includes/home.html', context)


def logout(request):
    user_log = Log.objects.filter(user_id=request.session['id']).last()
    user_log.logout_data = datetime.now()
    user_log.save()
    try:
        del request.session['logged_in']
        return redirect('usermanagement:login')
    except:
        return redirect('usermanagement:login')

@login_required("logged_in", 'usermanagement:login')
def authUserList(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'firstname': request.session['firstname'],
        'urls': request.session['urls'],
    }

    auth_user_list = User.objects.all()

    context = {
        'data': userdata,
        'auth_user_list': auth_user_list,
    }
    return render(request, 'user/authuser/authuserlist.html', context)

@login_required("logged_in", 'usermanagement:login')
def authUserRole(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'firstname': request.session['firstname'],
        'urls': request.session['urls'],
    }

    auth_user_group_list = Group.objects.all()

    context = {
        'data': userdata,
        'auth_user_group_list': auth_user_group_list
    }
    return render(request, 'user/authuser/authuserrole.html', context)


def authUserPriviledge(request, id):
    try:
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'urls': request.session['urls'],

        }
        modulelists = list()
        modulelall = list()

        privileged = Privileged.objects.filter(group_id=id).order_by('module_id')

        if privileged.count() == 0:
            modulelall = Modulename.objects.all()
            moduleurl = Moduleurl.objects.all()
        else:
            modulelall = Modulename.objects.all()
            moduleurl = Moduleurl.objects.all()

        context = {
            'data': userdata,
            'modulelall': modulelall,
            'id': id,
            'group_id': id,
            'privileged': privileged,
            'modulelists': modulelists,
            'moduleurl': moduleurl,
        }

        return render(request, 'user/authuser/authuserpriviliedge.html', context)
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('usermanagement:authuserrole')


def add_role_with_permission(request):
    try:
        form = PrivilegedForm
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'urls': request.session['urls'],
        }
        context = {
            'data': userdata,
            'form': form
        }
        if request.method == 'POST':
            list = request.POST.getlist('list')
            user_id = request.POST['user_id']
            group_id = request.POST['group_id']
            Privileged.objects.filter(group_id=group_id).delete()
            for id in list:
                id = id.split(',')
                Privileged.objects.create(moduleurl_id=id[0], module_id=id[1], module_type_id=id[2],
                                          group_id=group_id, created_by_id=user_id, created_at=datetime.now())
            messages.success(request, 'Data Saved  Successfully')
            return redirect('usermanagement:authuserrole')
        else:
            context = {
                'data': userdata,
                'form': form
            }
        return render(request, 'user/authuser/authuserpriviliedge.html', context)
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('usermanagement:authuserrole')
