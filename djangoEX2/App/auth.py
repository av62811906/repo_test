from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from App.models import *


class LoginAuthenticate(BaseAuthentication):
    """登录校验"""

    def authenticate(self, request):

        token = request._request.GET.get('token')
        uid = request._request.GET.get('uid')

        if all([token, uid]):
            utk = UserToken.objects.filter(user_id=uid, token=token).first()
            if not utk:
                raise exceptions.AuthenticationFailed('登录状态异常')

            # 返回后续view中可以使用的user,auth对象
            return utk.user, utk
        else:
            raise exceptions.AuthenticationFailed('未登录')
