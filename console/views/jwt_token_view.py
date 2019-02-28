import re
from datetime import datetime
from rest_framework_jwt.views import JSONWebTokenAPIView, jwt_response_payload_handler
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from backends.result import *
from sub.models.models import User

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserLoginView(JSONWebTokenAPIView):
    # 用户登录
    def post(self, request, *args, **kwargs):
        try:
            user_name = request.data.get("user_name", None)
            password = request.data.get("password", None)

            if not user_name:
                code = 400
                result = general_message(code, "username is missing", "请填写用户名")
                return Response(result, status=code)
            elif not password:
                code = 400
                result = general_message(code, "password is missing", "请填写密码")
                return Response(result, status=code)

            user_repo = User.objects.filter(user_name=user_name).first()
            if not user_repo:
                return Response(general_message(400, "user is null", "用户不存在"), status=400)
            if password != user_repo.password:
                return Response(general_message(400, "password id error", "密码不正确"), status=400)
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user = serializer.object.get('user') or request.user
                token = serializer.object.get('token')
                response_data = jwt_response_payload_handler(token, user, request)
                result = general_message(200, "login success", "登录成功", bean=response_data)
                response = Response(result)
                if api_settings.JWT_AUTH_COOKIE:
                    expiration = (datetime.utcnow() +
                                  api_settings.JWT_EXPIRATION_DELTA)
                    response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                        token,
                                        expires=expiration,
                                        httponly=True)
                return response
            result = general_message(400, "login failed", "{}".format(list(dict(serializer.errors).values())[0][0]))
            return Response(result, status=400)

        except Exception as e:
            result = error_message(e)
            return Response(result, status=500)


class UserRegisterView(APIView):
    # 用户注册
    def post(self, request, *args, **kwargs):
        try:
            user_name = request.data.get("user_name", None)
            password = request.data.get("password", None)
            note = request.data.get("note", None)
            if not user_name:
                code = 400
                result = general_message(code, "username is missing", "请填写用户名")
                return Response(result, status=code)
            elif not password:
                code = 400
                result = general_message(code, "password is missing", "请填写密码")
                return Response(result, status=code)
            # 简单校验
            r = re.compile(u'^[a-zA-Z0-9_\\-\u4e00-\u9fa5]+$')
            if not r.match(user_name.decode("utf-8")):
                result = general_message(400, "faild", "用户名称只支持中英文下划线和中划线")
                return Response(result, status=400)

            user_repo = User.objects.filter(user_name=user_name).first()
            if user_repo:
                return Response(general_message(400, "user_name is exist", "用户名已存在"), status=400)
            if len(password) < 8:
                result = general_message(400, "len error", "密码长度最少为8位")
                return Response(result)
            # 创建
            user_info = dict()
            user_info["user_name"] = user_name
            user_info["password"] = password
            if note:
                user_info["note"] = note
            user_obj = User.objects.create(**user_info)

            data = dict()
            data["user_id"] = user_obj.ID
            data["user_name"] = user_obj.user_name
            data["note"] = user_obj.note
            payload = jwt_payload_handler(user_obj)
            token = jwt_encode_handler(payload)
            data["token"] = token
            result = general_message(200, "register success", "注册成功", bean=data)
            return Response(result, status=200)

        except Exception as e:
            result = error_message(e)
            return Response(result, status=500)
