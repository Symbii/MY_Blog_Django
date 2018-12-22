from pure_pagination import PageNotAnInteger, Paginator
from django.shortcuts import render
from django.views import View
from myblog.models import Blog
# Create your views here.

class IndexView(View):
    """
    首页,继承view，自动根据请求，调用对应的方法
    """
    def get(self, request):
        all_blog = Blog.objects.all().order_by('-id')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
    
        p = Paginator(all_blog, 1, request=request)

        all_page_blog = p.page(page)

        return render(request, 'index.html', {"blog": all_page_blog})

