from rest_framework.views import APIView
from rest_framework.response import Response

from backends.result import *
from sub.models.models import History, Prediction


class HistoryRecordView(APIView):
    # 查询用户查询历史记录
    def get(self, request, *args, **kwargs):
        try:
            user_id = request.GET.get("user_id", None)
            if not user_id:
                return Response(general_message(400, "params error", "参数异常"), status=400)
            history_list = list()
            history_objs = History.objects.filter(user_id=user_id).all()
            if history_objs:
                for history_obj in history_objs:
                    history_dict = dict()
                    history_dict["create_time"] = history_obj.create_time
                    prediction_id = history_obj.prediction_id
                    pre_obj = Prediction.objects.filter(ID=prediction_id).all()
                    if pre_obj:
                        history_dict["station_name"] = pre_obj.station_name
                        history_dict["prediction_time"] = pre_obj.prediction_time
                        history_dict["prediction_index"] = pre_obj.prediction_index
                        history_dict["update_time"] = pre_obj.update_time
                    history_list.append(history_dict)
            result = general_message(200, "success", "查询成功", list=history_list)
            return Response(result, status=200)

        except Exception as e:
            result = error_message(e)
            return Response(result, status=500)

    # 清空记录
    def delete(self, request, *args, **kwargs):
        try:
            user_id = request.data.get("user_id", None)
            if not user_id:
                return Response(general_message(400, "params error", "参数异常"), status=400)
            history_objs = History.objects.filter(user_id=user_id).all()
            # 清空
            if history_objs:
                for history_obj in history_objs:
                    history_obj.delete()
            result = general_message(200, "success", "删除成功")
            return Response(result, status=200)
        except Exception as e:
            result = error_message(e)
            return Response(result, status=500)
