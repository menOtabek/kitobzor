from django.http import JsonResponse
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from .utils import validate_token


class AuthenticationRequiredMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        exclude_target_urls = [
            reverse('bot_register'),
            reverse('update_bot_user_data'),
            reverse('generate_otp_code'),
            reverse('login')
        ]
        if request.path.startswith('/api/v1/') and request.path not in exclude_target_urls:
            token = request.headers.get('Authorization')
            payload = validate_token(token)
            if payload is None:
                return JsonResponse(
                    data={'result': "", "error": "Unauthorized access", 'ok': False},
                    status=401
                )
        return None
