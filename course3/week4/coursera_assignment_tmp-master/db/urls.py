from django.conf.urls import url

from db.views import index

urlpatterns = [
    url(r'', index),
    url(r'^index/$', index)
]