from django.urls import path, re_path

from myblog.views import IndexView, ArchiveView, BlogDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('archive/', ArchiveView.as_view(), name='archive'),
    re_path(r'blog/(?P<blog_id>\d+)$', BlogDetailView.as_view(), name='blog_id'),
]