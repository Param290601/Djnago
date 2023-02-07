from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_fun(request,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_fun

def allowed_user(allowed_rolse=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            group =  None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                print(group)
            if group in allowed_rolse:
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse('You are un-authorized to home page')
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_fun(request,*args, **kwargs):
        group =  None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'customer':
            return redirect('user-page')
        if group == 'admin':
            return view_func(request,*args, **kwargs)
    return wrapper_fun