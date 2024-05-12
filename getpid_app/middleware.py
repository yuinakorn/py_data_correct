from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/':
            return self.get_response(request)  # Allow the request to continue without redirection
            
        elif not request.path.startswith(('/login/')):
            if not request.session.get('user_info'):
                return redirect('login')
        else:
            if request.session.get('user_info'):
                return redirect('home')

        print(f"Request path: {request.path}")  # พิมพ์ path ของ request
        # print(f"Is authenticated: {request.user.is_authenticated}")  # พิมพ์สถานะ authentication
        response = self.get_response(request)
        return response

    # def process_view(self, request, view_func, view_args, view_kwargs):
    #     exempt_urls = [
    #         '/',
    #         '/login/',
    #         '/person/',
    #         '/hoscode/',
    #         '/provider/',
    #         '/home/',
    #         '/ncd/',
    #         '/labor/',
    #         '/palliative/',
    #     ]

    #     if not any(request.path.startswith(path) for path in exempt_urls):
    #         if not request.session.get('user_info') or request.session.get('user_info').length == 0:
    #             return redirect('/login/')  # Redirect ไปที่หน้า login ถ้าไม่พบ session
    #         else:
    #             return redirect('/home/')

    #     return None
