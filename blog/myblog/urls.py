from django.urls import path

from myblog.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]