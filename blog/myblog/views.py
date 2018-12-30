from pure_pagination import PageNotAnInteger, Paginator
from django.shortcuts import render
from django.views import View
from myblog.models import Blog, Counts, Tag
from django.http import HttpResponse
from django.db import connection
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
            "cate_nums" : cate_nums,
            "tag_nums"  : tag_nums,
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
            "blog_nums" : blog_nums,
            "cate_nums" : cate_nums,
            "tag_nums"  : tag_nums,
        })

class BlogDetailView(View):
    """
    博客详情页
    """
    def get(self, request, blog_id):
        blog = Blog.objects.get(id=blog_id)

        # 博客、标签、分类数目统计
        count_nums = Counts.objects.get()
        blog_nums = count_nums.blog_nums
        cate_nums = count_nums.category_nums
        tag_nums = count_nums.tag_nums
        tag_names = []
        cursor = connection.cursor()

        #获取标签名字，采用sql语句获取 ，也可以直接blog.tag.all
        sql_cmd = "select tag_id from myblog_blog_tag where blog_id = {0};".format(blog_id)
        cursor.execute(sql_cmd)
        row_tag_id = cursor.fetchall()
        for row_each_tag in row_tag_id: 
            sql_cmd = "select name from myblog_tag where id = {0};".format(row_each_tag[0])
            cursor.execute(sql_cmd)
            row_each_name = cursor.fetchone()
            tag_names.append(row_each_name[0])

        # 实现博客上一篇与下一篇功能
        has_prev = False
        has_next = False
        id_prev = id_next = int(blog_id)
        blog_id_max = Blog.objects.all().order_by('-id').first()
        id_max = blog_id_max.id
        while not has_prev and id_prev >= 1:
            blog_prev = Blog.objects.filter(id=id_prev - 1).first()
            if not blog_prev:
                id_prev -= 1
            else:
                has_prev = True
        while not has_next and id_next <= id_max:
            blog_next = Blog.objects.filter(id=id_next + 1).first()
            if not blog_next:
                id_next += 1
            else:
                has_next = True;


        blog.content = markdown.markdown(blog.content)
        return render(request, 'blog-detail.html', {
            'blog': blog,
            "blog_nums" : blog_nums,
            "cate_nums" : cate_nums,
            "tag_nums"  : tag_nums,
            "tag_names" : tag_names,
            'blog_prev': blog_prev,
            'blog_next': blog_next,
            'has_prev': has_prev,
            'has_next': has_next,
        })


class TagView(View):
    """
    博客标签综述
    """
    def get(self, request):
        all_tags = Tag.objects.all()

        # 博客、标签、分类数目统计
        count_nums = Counts.objects.get()
        blog_nums = count_nums.blog_nums
        cate_nums = count_nums.category_nums
        tag_nums = count_nums.tag_nums

        return render(request, 'tags.html', {
            'tags': all_tags,
            'tag_nums': tag_nums,
            'blog_nums': blog_nums,
            "cate_nums" : cate_nums,    
        })

class TagDetailView(View):
    """
    博客标签下所包含的博客文章
    """
    def get(self, request, tag_name):
        return HttpResponse("功能没想好做成什么样，待想一想，看看同类产品")

def page_not_found(request):
    return render(request, '404.html')

def page_errors(request):
    return render(request, '500.html')