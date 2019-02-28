from django.conf.urls import patterns, url

from backends.views.user import UserView, QueryHistoryView
from backends.views.historys import AllHistorysView
from backends.views.station import StationManageView


urlpatterns = patterns(
    url(r'^user$', UserView.as_view()),
    url(r'^history$', QueryHistoryView.as_view()),
    url(r'^all_history$', AllHistorysView.as_view()),
    url(r'^station', StationManageView.as_view()),
)
