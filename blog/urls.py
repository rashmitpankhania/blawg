from django.conf.urls import url
from . import views

app_name = 'blog'

urlpatterns = [
    url(r'list/$', views.home, name='list'),
    url(r'tag/(?P<tag_slug>[-\w]+)/$', views.home, name='list_by_tag'),
    url(r'(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$', views.detail, name='detail'),
    url(r'(?P<post_id>[0-9]+)/share/$', views.share, name='share'),
]