from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^end$', views.stop, name='stop'),
    url(r'^file_list$', views.file_list, name='file_list'),
    url(r'^download/(?P<file_id>)', views.download_file, name='download'),
    url(r'^server_state$', views.server_state, name='server_state'),
    url(r'^dump_timeout$', views.dump_timeout, name='dump_timeout'),

]
