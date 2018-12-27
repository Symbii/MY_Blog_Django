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
        finally:
            count_nums.save()
        #博客分类数目统计
        #obj_category = obj.category
        #category_number = obj_category.blog_set.count()
        #obj_category.number = category_number
        #obj_category.save()
        #博客标签数目统计
        #obj_tag_list = obj.tag.all()
        #for obj_tag in obj_tag_list:
        #    tag_number = obj_tag.blog_set.count()
        #    obj_tag.number = tag_number
        #    obj_tag.save()

    def delete_model(self, request, obj):
        # 统计博客数目
        blog_nums = Blog.objects.count()
        count_nums = Counts.objects.get()
        count_nums.blog_nums = blog_nums - 1
        count_nums.save()
        # 博客分类数目统计
        #obj_category = obj.category
        #category_number = obj_category.blog_set.count()
        #obj_category.number = category_number - 1
        #obj_category.save()
        # 博客标签数目统计
        #obj_tag_list = obj.tag.all()
        #for obj_tag in obj_tag_list:
        #    tag_number = obj_tag.blog_set.count()
        #    obj_tag.number = tag_number - 1
        #    obj_tag.save()
        obj.delete()

class CountsAdmin(admin.ModelAdmin):
    list_display = ['blog_nums', 'category_nums', 'tag_nums', 'visit_nums']

# Register your models here.
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment)
admin.site.register(Counts, CountsAdmin)