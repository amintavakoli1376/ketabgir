from django.contrib import admin
from .models import Article, Category ,IPAddress

#Admin header change
admin.site.site_header = "مدیریت وبلاگ"

# Register your models here.

def make_published(modeladmin, request, queryset):
    rows_update = queryset.update(status='published')
    if rows_update == 1:
        message_bit = "منتشر شد."
    else:
        message_bit = "منتشر شدند."
    modeladmin.message_user(request,"{} مقاله {}".format(rows_update,message_bit))
make_published.short_description = "انتشار مقالات انتخاب شده"

def make_draft(modeladmin, request, queryset):
    rows_update = queryset.update(status='draft')
    if rows_update == 1:
        message_bit = "پیش نویس شد."
    else:
        message_bit = "پیش نویس شدند."
    modeladmin.message_user(request,"{} مقاله {}".format(rows_update,message_bit))
make_draft.short_description = "پیش نویس شدن مقالات انتخاب شده"

def make_active(modeladmin, request, queryset):
    rows_update = queryset.update(status=True)
    if rows_update == 1:
        message_bit = "فعال شد."
    else:
        message_bit = "فعال شدند."
    modeladmin.message_user(request,"{} دسته بندی {}".format(rows_update,message_bit))
make_active.short_description = "فعال شدن دسته بندی های انتخاب شده"

def make_deactive(modeladmin, request, queryset):
    rows_update = queryset.update(status=False)
    if rows_update == 1:
        message_bit = "غیرفعال شد."
    else:
        message_bit = "غیرفعال شدند."
    modeladmin.message_user(request,"{} دسته بندی {}".format(rows_update,message_bit))
make_deactive.short_description = "غیرفعال شدن دسته بندی های انتخاب شده"

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position','title','slug','parent','status')
    list_filter = ('status',)
    search_fields = ('title','slug')
    prepopulated_fields = {'slug': ('title',)}
    actions = [make_active,make_deactive]

admin.site.register(Category,CategoryAdmin)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','thumbnail_tag','slug','author','jpublish','is_special','status','category_to_str')
    list_filter = ('publish','status','author')
    search_fields = ('title','description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['status','publish']
    actions = [make_published,make_draft]
    


admin.site.register(Article,ArticleAdmin)
admin.site.register(IPAddress)
