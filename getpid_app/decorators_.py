from django.http import HttpResponseRedirect
from django.shortcuts import render


def custom_login_required(function):
    def wrap(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return HttpResponseRedirect('index')  # Redirect ถ้าไม่มี session
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


# ใช้กับ view
@custom_login_required
def my_protected_view(request):
    # Assuming the user ID is stored in the session upon login
    username = request.session.get('user_id')

    if username:
        #     redirect('/login/')
        return HttpResponseRedirect('/home/')
    else:
        return render(request, 'login.html')

    # Render and return the HTML page with the user profile data

# @custom_login_required
# def my_protected_view(request):
#     # Your protected view logic here
#     return render(request, 'protected.html')
