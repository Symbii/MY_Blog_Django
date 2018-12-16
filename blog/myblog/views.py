from django.shortcuts import render
from django.views import View
from myblog.models import Blog
# Create your views here.

class IndexView(View):
    """
    首页
    """
    def get(self, request):
        all_blog = Blog.objects.all().order_by('-id')
        return render(request, 'index.html', {"blog": all_blog})

