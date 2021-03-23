from django.contrib import admin
from blog.models import Post


class PostAdmin(admin.ModelAdmin):

    fields = ('id', 'title', 'slug', 'author', 'body', 'created', 'updated', 'publish', 'status',)
    readonly_fields = ('created', 'updated', 'publish', 'id',)
    list_display = ('id', 'title', 'slug',)
    list_filter = ('status', 'created', 'publish', 'author',)
    search_fields = ('title', 'body',)
    prepopulated_fields = {'slug': ('title',)}
    # raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish',)

    # comments:
    # prepopulated_fields формирует поле key по value автоматически но только в админке
    # формирует так, каким должен быть слаг (по правилам слага).


admin.site.register(Post, PostAdmin)
