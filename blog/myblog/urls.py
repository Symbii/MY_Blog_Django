from django.urls import path, re_path

from myblog.views import IndexView, ArchiveView, BlogDetailView, TagView, TagDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('archive/', ArchiveView.as_view(), name='archive'),
    re_path(r'blog/(?P<blog_id>\d+)$', BlogDetailView.as_view(), name='blog_id'),
    path('tags/', TagView.as_view(), name='tags'),
    re_path(r'tags/(?P<tag_name>\w+)$', TagDetailView.as_view(), name='tag_name'),
]