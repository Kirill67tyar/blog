from django.shortcuts import render
from django.shortcuts import get_object_or_404
from blog.models import Post


def post_list(request):
    obj_list = Post.published.all()
    return render(request, 'blog/list.html', context={'obj_list': obj_list,})


def post_detail(request, year, month, day, slug):
    kwargs = {
        'publish__year': year,
        'publish__month': month,
        'publish__day': day,
        'slug': slug,
    }
    obj = get_object_or_404(Post, **kwargs)
    return render(request, 'blog/retrieve.html', context={'obj': obj,})


def post_retrieve(request, **kwargs):
    obj = get_object_or_404(Post, **kwargs)
    return render(request, 'blog/retrieve.html', context={'obj': obj,})
