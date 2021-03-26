from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView

from blog.models import Post
from blog.forms import EmailPostForm

def post_list(request):
    qs = Post.published.all()
    paginator = Paginator(qs, 2)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/list.html', context={'page_obj': page_obj,})


def post_retrieve(request, year, month, day, slug):
    kwargs = {
        'publish__year': year,
        'publish__month': month,
        'publish__day': day,
        'slug': slug,
    }
    obj = get_object_or_404(Post, **kwargs)
    return render(request, 'blog/retrieve.html', context={'obj': obj,})



    # если мы введем некорректные данные (не число) в get параметр ?page= то
    # пагинатор перейдет на первую страницы
    # если мы примем в get параметр (query string) число большее, чем страниц у нас есть -
    # то попадем на последнюю страницу
    # все это благодаря тому, что мы используем метод get_page()
    # но можно использовать метод page() и нам придется вручную отлавливать PageNotAnInteger и EmptyPage


def post_share(request, post_id):

    post = get_object_or_404(Post, id=post_id, status='published')
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
    elif request.method == 'GET':
        form = EmailPostForm()
    return render(request, 'blog/share.html', context={'form': form})




class PostListView(ListView):

    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/list.html'