from django.contrib import admin
from blog.models import Post, Comment, Tag


class PostAdmin(admin.ModelAdmin):

    fields = ('id', 'title', 'slug', 'author', 'body', 'created', 'updated', 'publish', 'status',)
    readonly_fields = ('created', 'updated', 'id',)
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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'name', 'created', 'active',)
    list_filter = ('active', 'created', 'updated',)
    search_fields = ('post', 'email', 'body',)\


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ('name', 'slug', 'posts',)
    list_display = ('name', 'slug',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name',)
    search_fields = ('name', 'slug', 'posts',)


