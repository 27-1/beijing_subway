from django.db import models


class User(models.Model):
    class Meta:
        db_table = 'user_info'

    user_name = models.CharField(max_length=128, help_text='用户名')
    password = models.CharField(max_length=128, help_text='密码')
    create_time = models.DateTimeField(help_text='创建时间', null=True)
    update_time = models.DateTimeField(help_text='更新时间', null=True)
    note = models.TextField(help_text='备注', null=True, blank=True)


class History(models.Model):
    class Meta:
        db_table = 'history'

    user_id = models.IntegerField(help_text='用户id')
    prediction_id = models.IntegerField(help_text='预测id')
    create_time = models.DateTimeField(help_text='创建时间', null=True)


class Prediction(models.Model):
    class Meta:
        db_table = 'prediction'

    station_name = models.CharField(max_length=128, help_text='站点名')
    prediction_time = models.DateTimeField(help_text='预测时间', null=True)
    prediction_index = models.IntegerField(help_text='拥堵指数', default=0)
    update_time = models.DateTimeField(help_text='更新时间', null=True)


class Station(models.Model):
    class Meta:
        db_table = 'station'

    station_name = models.CharField(max_length=128, help_text='站点名')
    line = models.TextField(help_text='地铁线路', null=True, blank=True)
    update_time = models.DateTimeField(help_text='更新时间', null=True)




