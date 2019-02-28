from django.conf.urls import patterns, url

from console.views.jwt_token_view import UserLoginView, UserRegisterView
from console.views.historical_record import HistoryRecordView


urlpatterns = patterns(
    url(r'^user/login$', UserLoginView.as_view()),
    url(r'^user/register$', UserRegisterView.as_view()),
    url(r'^history/record$', HistoryRecordView.as_view()),

)
