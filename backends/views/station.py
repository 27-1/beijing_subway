import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection

from backends.result import *
from sub.models.models import Station


# 站点管理
class StationManageView(APIView):
    # 查询站点信息
    def get(self, request, *args, **kwargs):
        try:
            page = int(request.GET.get("page_num", 1))
            page_size = int(request.GET.get("page_size", 10))
            station_name = request.GET.get("station_name", None)
            station_list = []
            if station_name:
                cursor = connection.cursor()
                cursor.execute(
                    "select count(*) from station where  station_name like '%{0}%';".format(station_name))
                station_count = cursor.fetchall()
                total = station_count[0][0]
                start = (page - 1) * page_size
                remaining_num = total - (page - 1) * page_size
                end = page_size
                if remaining_num < page_size:
                    end = remaining_num
                cursor = connection.cursor()
                cursor.execute(
                    "select ID, station_name, line, update_time from station where station_name like '%{0}%' order by update_time desc LIMIT {1},{2};".format(station_name, start, end))
                station_tuples = cursor.fetchall()
                if len(station_tuples) > 0:
                    for station_tuple in station_tuples:
                        station_dict = dict()
                        station_dict["ID"] = station_tuple[0]
                        station_dict["station_name"] = station_tuple[1]
                        station_dict["line"] = station_tuple[2]
                        station_dict["update_time"] = station_tuple[3]
                        station_list.append(station_dict)
                bean = {"total": total}

            else:
                cursor = connection.cursor()
                cursor.execute(
                    "select count(*) from station;".format(station_name))
                station_count = cursor.fetchall()
                total = station_count[0][0]
                start = (page - 1) * page_size
                remaining_num = total - (page - 1) * page_size
                end = page_size
                if remaining_num < page_size:
                    end = remaining_num
                cursor = connection.cursor()
                cursor.execute(
                    "select ID, station_name, line, update_time from station order by update_time desc LIMIT {0},{1};".format(
                        start, end))
                station_tuples = cursor.fetchall()
                if len(station_tuples) > 0:
                    for station_tuple in station_tuples:
                        station_dict = dict()
                        station_dict["ID"] = station_tuple[0]
                        station_dict["station_name"] = station_tuple[1]
                        station_dict["line"] = station_tuple[2]
                        station_dict["update_time"] = station_tuple[3]
                        station_list.append(station_dict)
                bean = {"total": total}
            result = general_message(200, "success", "查询成功", bean=bean, list=station_list)
            return Response(result, status=200)
        except Exception as e:
            result = error_message(e)
            return Response(result, status=500)

    # 添加站点信息
    def post(self, request, *args, **kwargs):
        try:
            station_name = request.data.get("station_name", None)
            line = request.data.get("line", None)
            if not station_name or not line:
                return Response(general_message(400, "params error", "参数异常"), status=400)
            station_repo = Station.objects.filter(station_name=station_name).first()
            if station_repo:
                return Response(general_message(400, "station_name is exist", "站点名已存在"), status=400)
            update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            station_info = dict()
            station_info["station_name"] = station_name
            station_info["line"] = line
            station_info["update_time"] = update_time
            Station.objects.create(**station_info)
            result = general_message(200, "success", "添加成功")
            return Response(result, status=200)
        except Exception as e:
            result = error_message(e)
            return Response(result, status=500)

    # 修改站点信息
    def put(self, request, *args, **kwargs):
        try:
            old_station_name = request.data.get("old_station_name", None)
            new_station_name = request.data.get("new_station_name", None)
            line = request.data.get("line", None)
            if not old_station_name:
                return Response(general_message(400, "params error", "参数异常"), status=400)
            if not new_station_name and not line:
                return Response(general_message(400, "params error", "参数异常"), status=400)

            station_repo = Station.objects.filter(station_name=new_station_name).first()
            if station_repo:
                return Response(general_message(400, "station_name is exist", "站点名已存在"), status=400)

            old_station_repo = Station.objects.filter(station_name=old_station_name).first()

            if new_station_name:
                old_station_repo.station_name = new_station_name
            if line:
                old_station_repo.line = line
            update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            old_station_repo.update_time = update_time

            old_station_repo.save()
            result = general_message(200, "success", "修改成功")
            return Response(result, status=200)
        except Exception as e:
            result = error_message(e)
            return Response(result, status=500)