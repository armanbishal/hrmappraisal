from django.shortcuts import render
from functools import wraps
from usermanagement.models import User,Privileged
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import resolve

def access_permission_required(view_func):
    """This is The custome decorator for checking permission of a controller function"""
    def _decorator(request, *args, **kwargs):
        # #check if the user has proper permission to access this function
        myfunc, myargs, mykwargs = resolve(request.get_full_path())
        view_function = myfunc.__name__
        user = request.session['id']
        if user is None:
            return render(request, 'user/login.html')
        user_profile = User.objects.get(id=user)
        role_id = user_profile.group
        access = Privileged.objects.filter(group=role_id, moduleurl__url=view_function)
        # print(view_function)
        if not access.exists():
            userdata = {
                'user_id': request.session['id'],
                'username': request.session['username'],
                'urls': request.session['urls'],
            }
            context = {
                'data': userdata,
            }
            return render(request, 'includes/404.html',context)
        response = view_func(request, *args, **kwargs)
        # maybe do something after the view_func call
        return response
    return wraps(view_func)(_decorator)

def login_required(session_key, fail_redirect_to):
    def _session_required(view_func):
        @wraps(view_func)
        def __session_required(request, *args, **kwargs):
            try:
                session = request.session.get(session_key)
                if session is None:
                    raise ValueError('Login Session is Expired Please Login Again!')
            except KeyError as e:
                messages.error(request, 'Login Session is Expired Please Login Again!')
                return redirect(fail_redirect_to)
            except ValueError as e:
                messages.error(request, 'Login Session is Expired Please Login Again!')
                return redirect(fail_redirect_to)
            else:
                return view_func(request, *args, **kwargs)
        return __session_required
    return _session_required


def session_required(session_key, fail_redirect_to):
    def _session_required(view_func):
        @wraps(view_func)
        def __session_required(request, *args, **kwargs):
            current_url = resolve(request.path_info).url_name
            request.session['redirect_to'] = 'epub:' + current_url
            # print (request.session['redirect_to'])
            # ipdb.set_trace()
            try:
                session = request.session.get(session_key)
                if session is None:
                    raise ValueError('Login Session is Expired Please Login Again!')
            except KeyError as e:
                # messages.error(request, 'You Are Not Logged In!')
                return redirect(fail_redirect_to)
            except ValueError as e:
                # messages.error(request, e.message)
                return redirect(fail_redirect_to)
            else:
                return view_func(request, *args, **kwargs)
        return __session_required
    return _session_required
