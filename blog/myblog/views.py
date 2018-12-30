from pure_pagination import PageNotAnInteger, Paginator
from django.shortcuts import render
from django.views import View
from myblog.models import Blog, Counts
import markdown

# Create your views here.

class IndexView(View):
    """
    首页,继承view，自动根据请求，调用对应的方法
    """
    def get(self, request):
        all_blog = Blog.objects.all().order_by('-id')

        #all_blog加markdown样式
        for blog in all_blog:
            blog.content = markdown.markdown(blog.content)
            
        # 博客、标签、分类数目统计
        count_nums = Counts.objects.get()
        blog_nums = count_nums.blog_nums
        cate_nums = count_nums.category_nums
        tag_nums = count_nums.tag_nums

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
    
        p = Paginator(all_blog, 1, request=request)
        all_page_blog = p.page(page)

        return render(request, 'index.html', {
            "blog":all_page_blog,
            "blog_nums":blog_nums,
        })

class ArchiveView(View):
    """
    归档
    """
    def get(self, request):
        #按照时间归档
        Archive = Blog.objects.all().order_by("-create_time")

        # 博客、标签、分类数目统计
        count_nums = Counts.objects.get()
        blog_nums = count_nums.blog_nums
        cate_nums = count_nums.category_nums
        tag_nums = count_nums.tag_nums

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page=1
        
        p = Paginator(Archive, 5, request=request)
        all_page_archive = p.page(page)

        return render(request, "archive.html", {
            "all_archive":all_page_archive,
            "blog_nums" : blog_nums
        })

class BlogDetailView(View):
    """
    博客详情页
    """
    def get(self, request, blog_id):
        blog = Blog.objects.get(id=blog_id)
        blog.content = markdown.markdown(blog.content)
        return render(request, 'blog-detail.html', {
            'blog': blog,
        })

def page_not_found(request):
    return render(request, '404.html')

def page_errors(request):
    return render(request, '500.html')