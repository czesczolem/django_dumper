from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^end$', views.stop, name='stop'),
    url(r'^file_list$', views.file_list, name='file_list'),
    url(r'^(?P<file_id>\d+/)', views.download_file, name='download')
]
