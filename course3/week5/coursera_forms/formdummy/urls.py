from django.urls import path

from . import views

urlpatterns = [
    path('', views.FormDummyView.as_view()),
]
