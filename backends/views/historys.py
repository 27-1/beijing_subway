from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection

from backends.result import *
from sub.models.models import User, Prediction


class AllHistorysView(APIView):
    # 获取所有查询记录表
    def get(self, request, *args, **kwargs):
        try:
            page = int(request.GET.get("page_num", 1))
            page_size = int(request.GET.get("page_size", 10))
            history_list = []
            cursor = connection.cursor()
            cursor.execute("select count(*) from history;")
            history_count = cursor.fetchall()
            total = history_count[0][0]
            start = (page - 1) * page_size
            remaining_num = total - (page - 1) * page_size
            end = page_size
            if remaining_num < page_size:
                end = remaining_num
            cursor = connection.cursor()
            cursor.execute(
                "select ID, user_id, prediction_id from history order by create_time desc LIMIT {0},{1};".format(
                    start, end))
            history_tuples = cursor.fetchall()
            if len(history_tuples) > 0:
                for history_tuple in history_tuples:
                    history_dict = dict()
                    history_dict["ID"] = history_tuple[0]
                    user_id = history_tuple[1]
                    prediction_id = history_tuple[2]
                    user_repo = User.objects.filter(user_id=user_id).first()
                    if user_repo:
                        history_dict["user_name"] = user_repo.user_name

                    prediction_repo = Prediction.objects.filter(ID=prediction_id).first()
                    if prediction_repo:
                        history_dict["station_name"] = prediction_repo.station_name
                        history_dict["prediction_time"] = prediction_repo.prediction_time
                        history_dict["prediction_index"] = prediction_repo.prediction_index
                        history_dict["update_time"] = prediction_repo.update_time

                    history_list.append(history_dict)
            bean = {"total": total}
            result = general_message(200, "success", "查询成功", bean=bean, list=history_list)
            return Response(result, status=200)
        except Exception as e:
            result = error_message(e)
            return Response(result, status=500)
