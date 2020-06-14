import hashlib
import time

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView

from App.models import *
from App.permission import *


class AuthView(APIView):
    """用于登录校验"""

    authentication_classes = []

    def md5(self, user):
        ctime = time.time()
        m = hashlib.md5(str(user).encode('utf-8'))
        m.update(str(ctime).encode('utf-8'))
        return m.hexdigest()

    def get(self, request, *args, **kwargs):
        return HttpResponse('auth view')

    def post(self, request, *args, **kwargs):
        ret = {'code': 10000, 'msg': 'ok'}

        username = request._request.POST.get('username')
        password = request._request.POST.get('password')

        user = User.objects.filter(username=username, password=password).first()
        if not user:
            ret['msg'] = '密码错误'
        if user:
            token = self.md5(user)
            print(token)
            UserToken.objects.update_or_create(user=user, defaults={'token': token})

        ret['token'] = token
        return JsonResponse(data=ret)


class OrderView(APIView):
    """订单"""

    permission_classes = [UserPermission]

    def get(self, request, *args, **kwargs):

        ret = {'code': 10000, 'msg': 'ok', 'data': None, 'token': request.auth.token}

        uid = request.user.id
        orders = Order.objects.filter(user_id=uid)
        data = []
        if orders:
            for order in orders:
                data.append({
                    'name': order.name,
                    'create_date': order.createDate,
                })
            ret['data'] = data

        return JsonResponse(ret)
