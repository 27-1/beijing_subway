import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection

from backends.result import *
from sub.models.models import User, History, Prediction


# 管理后台用户操作
class UserView(APIView):
    # 分页查出所有用户数据
    def get(self, request, *args, **kwargs):
        try:
            page = int(request.GET.get("page_num", 1))
            page_size = int(request.GET.get("page_size", 10))
            user_name = request.GET.get("user_name", None)
            user_list = []
            if user_name:
                cursor = connection.cursor()
                cursor.execute(
                    "select count(*) from user_info where  user_name like '%{0}%';".format(user_name))
                user_count = cursor.fetchall()
                total = user_count[0][0]
                start = (page - 1) * page_size
                remaining_num = total - (page - 1) * page_size
                end = page_size
                if remaining_num < page_size:
                    end = remaining_num
                cursor = connection.cursor()
                cursor.execute(
                    "select ID, user_name, create_time from user_info where user_name like '%{0}%' order by create_time desc LIMIT {1},{2};".format(user_name, start, end))
                user_tuples = cursor.fetchall()
                if len(user_tuples) > 0:
                    for user_tuple in user_tuples:
                        user_dict = dict()
                        user_dict["ID"] = user_tuple[0]
                        user_dict["user_name"] = user_tuple[1]
                        user_dict["create_time"] = user_tuple[2]
                        user_list.append(user_dict)
                bean = {"total": total}

            else:
                cursor = connection.cursor()
                cursor.execute("select count(*) from user_info;")
                user_count = cursor.fetchall()
                total = user_count[0][0]
                start = (page - 1) * page_size
                remaining_num = total - (page - 1) * page_size
                end = page_size
                if remaining_num < page_size:
                    end = remaining_num
                cursor = connection.cursor()
                cursor.execute(
                    "select ID, user_name, create_time from user_info order by create_time desc LIMIT {0},{1};".format(
                        start, end))
                user_tuples = cursor.fetchall()
                if len(user_tuples) > 0:
                    for user_tuple in user_tuples:
                        user_dict = dict()
                        user_dict["ID"] = user_tuple[0]
                        user_dict["user_name"] = user_tuple[1]
                        user_dict["create_time"] = user_tuple[2]
                        user_list.append(user_dict)
                bean = {"total": total}
            result = general_message(200, "success", "查询成功", bean=bean, list=user_list)
            return Response(result, status=200)
        except Exception as e:
            result = error_message(e)
            return Response(result, status=500)

    # 添加用户
    def post(self, request, *args, **kwargs):
        try:
            user_name = request.data.get("user_name", None)
            password = request.data.get("password", None)
            note = request.data.get("note", None)
            if not user_name or not password:
                return Response(general_message(400, "params error", "参数异常"), status=400)
            user_repo = User.objects.filter(user_name=user_name).first()
            if user_repo:
                return Response(general_message(400, "user_name is exist", "用户名已存在"), status=400)
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            user_info = dict()
            user_info["user_name"] = user_name
            user_info["password"] = password
            user_info["note"] = note
            user_info["create_time"] = create_time
            user_info["update_time"] = update_time
            User.objects.create(**user_info)
            result = general_message(200, "success", "添加成功")
            return Response(result, status=200)
        except Exception as e:
            result = error_message(e)
            return Response(result, status=500)

    # 修改用户
    def put(self, request, *args, **kwargs):
        try:
            old_name = request.data.get("old_name", None)
            new_name = request.data.get("user_name", None)
            password = request.data.get("password", None)
            note = request.data.get("note", None)
            if not old_name:
                return Response(general_message(400, "params error", "参数异常"), status=400)
            if not new_name and not password and not note:
                return Response(general_message(400, "params error", "参数异常"), status=400)

            user_repo = User.objects.filter(user_name=new_name).first()
            if user_repo:
                return Response(general_message(400, "user_name is exist", "用户名已存在"), status=400)

            user_repo = User.objects.filter(user_name=old_name).first()

            if new_name:
                user_repo.user_name = new_name
            if password:
                user_repo.password = password
            if note:
                user_repo.note = note
            update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            user_repo.update_time = update_time

            user_repo.save()
            result = general_message(200, "success", "修改成功")
            return Response(result, status=200)
        except Exception as e:
            result = error_message(e)
            return Response(result, status=500)

    # 删除用户
    def delete(self, request, *args, **kwargs):
        try:
            user_name = request.data.get("user_name", None)
            if not user_name:
                return Response(general_message(400, "user_name is null", "请指明要删除的用户"), status=400)
            user_repo = User.objects.filter(user_name=user_name).first()
            if not user_repo:
                return Response(general_message(400, "user is null", "用户不存在"), status=400)
            user_repo.delete()
            result = general_message(200, "success", "删除成功")
            return Response(result, status=200)
        except Exception as e:
            result = error_message(e)
            return Response(result, status=500)


class QueryHistoryView(APIView):
    # 查询历史记录
    def get(self, request, *args, **kwargs):
        try:
            user_id = request.GET.get("user_id", 0)
            if not user_id:
                return Response(general_message(400, "params error", "参数异常"), status=400)

            historys = History.objects.filter(user_id=user_id).all()
            history_list = []
            if historys:
                for history in historys:
                    history_dict = dict()
                    history_dict["ID"] = history.ID
                    history_dict["create_time"] = history.create_time
                    prediction_id = history.prediction_id
                    pr_repo = Prediction.objects.filter(ID=prediction_id).first()
                    if pr_repo:
                        history_dict["station_name"] = pr_repo.station_name
                        history_dict["prediction_time"] = pr_repo.prediction_time
                        history_dict["prediction_index"] = pr_repo.prediction_index
                        history_dict["update_time"] = pr_repo.update_time
                    history_list.append(history_dict)
            result = general_message(200, "success", "查询成功")
            return Response(result, status=200)
        except Exception as e:
            result = error_message(e)
            return Response(result, status=500)








