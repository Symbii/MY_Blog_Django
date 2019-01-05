from django.contrib import admin
from myblog.models import Category, Tag, Blog, Comment, Counts

class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'create_time', 'click_nums', 'category']

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

        #博客分类数目统计
        obj_category = obj.category
        category_number = obj_category.blog_set.count()
        obj_category.number = category_number
        obj_category.save()
        
        #counts表刷新，分类数据
        category_nums = Category.objects.count()
        count_nums.category_nums = category_nums

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

        count_nums.save()

    def delete_model(self, request, obj):
        # 统计博客数目
        blog_nums = Blog.objects.count()
        count_nums = Counts.objects.get()
        count_nums.blog_nums = blog_nums - 1
        
        # 博客分类数目统计
        obj_category = obj.category
        category_number = obj_category.blog_set.count()
        obj_category.number = category_number - 1
        obj_category.save()
        
        #counts表刷新，分类数据
        category_nums = Category.objects.count()
        count_nums.category_nums = category_nums

        # 博客标签数目统计
        obj_tag_list = obj.tag.all()
        for obj_tag in obj_tag_list:
            tag_number = obj_tag.blog_set.count()
            obj_tag.number = tag_number - 1
            obj_tag.save()

        #counts表刷新，标签数据
        tag_nums = Tag.objects.count()
        count_nums.tag_nums = tag_nums

        count_nums.save()
        obj.delete()

class CountsAdmin(admin.ModelAdmin):
    list_display = ['blog_nums', 'category_nums', 'tag_nums', 'visit_nums']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'number']

    def save_model(self, request, obj, form, change):
        obj.save()
        category_nums = Category.objects.count()
        count_nums = Counts.objects.get()
        count_nums.category_nums = category_nums
        count_nums.save()

    def delete_model(self, request, obj):
        obj.delete()
        category_nums = Category.objects.count()
        count_nums = Counts.objects.get()
        count_nums.category_nums = category_nums
        count_nums.save()

class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'number']

    def save_model(self, request, obj, form, change):
        obj.save()
        tag_nums = Tag.objects.count()
        count_nums = Counts.objects.get()
        count_nums.tag_nums = tag_nums
        count_nums.save()

    def delete_model(self, request, obj):
        obj.delete()
        tag_nums = Tag.objects.count()
        count_nums = Counts.objects.get()
        count_nums.tag_nums = tag_nums
        count_nums.save()


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment)
admin.site.register(Counts, CountsAdmin)