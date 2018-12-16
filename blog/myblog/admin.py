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