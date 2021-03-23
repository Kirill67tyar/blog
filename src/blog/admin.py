from django.contrib import admin
from blog.models import Post


class PostAdmin(admin.ModelAdmin):

    fields = 'id', 'title', 'slug', 'author', 'body', 'created', 'updated', 'publish', 'status',
    readonly_fields = 'created', 'updated', 'publish', 'id',
    list_display = 'id', 'title', 'slug',


admin.site.register(Post, PostAdmin)
