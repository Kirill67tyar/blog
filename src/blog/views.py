from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.core.mail import send_mail
from blog.models import Post
from blog.forms import EmailPostForm


def experiments(request):
    obj = get_object_or_404(Post, id=1)
    post_url = request.build_absolute_uri(obj.get_absolute_url())
    # # 1 ----------------------------------------------------------------
    # print(f'\n\n--------------------------------------------\n'
    #       f'request.build_absolute_uri(obj.get_absolute_url() = {post_url}\n'
    #       f'obj.get_absolute_url() = {obj.get_absolute_url()}\n'
    #       f'path = {request.path}\n'
    #       f'path_info = {request.path_info}\n'
    #       f'get_host = {request.get_host()}\n'
    #       f'get_full_path_info = {request.get_full_path_info()}\n'
    #       f'get_full_path = {request.get_full_path()}\n'
    #       f'---------------------------------------------\n\n')
    # #  ----------------------------------------------------------------
    # # 2 ----------------------------------------------------------------
    # print('\n\n--------------------------------------------\n',
    #       *dir(request),
    #       '---------------------------------------------\n\n',sep='\n')
    # # ----------------------------------------------------------------
    return HttpResponse('Check console')


def concat_and_send_message(request, post, data):
    """
        Функция ответственна за конкатенацию и отправку сообщения
        возвращает True
        принимает 3 аргумента где:
            request - HTTP request с методом post
            post - экземпляр модели Post
            data - cleaned_data
    """
    post_url = request.build_absolute_uri(post.get_absolute_url())
    title = f'{data["name"]} ({data["email"]}) recommends you reading {post.title}'
    body = f'Read {post.title} at {post_url} \n\n {data["name"]}\'s comments:\n {data["comments"]}'
    send_mail(title, body, settings.EMAIL_HOST_USER, [data['to']])
    sent = True
    return sent



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

# send_mail('check',
# "I'm checking sending messages from kirillbogomolov.ric@gmail.com",
# 'kirillbogomolov.ric@gmail.com',
# ['kirillbogomolov.ric@gmail.com', 'kirillbogomolov.ric@yandex.ru',],
# fail_silently=False)

    # если мы введем некорректные данные (не число) в get параметр ?page= то
    # пагинатор перейдет на первую страницы
    # если мы примем в get параметр (query string) число большее, чем страниц у нас есть -
    # то попадем на последнюю страницу
    # все это благодаря тому, что мы используем метод get_page()
    # но можно использовать метод page() и нам придется вручную отлавливать PageNotAnInteger и EmptyPage


def post_share(request, post_id):
    """
        обратоботчик принимающий post и get запросы для отправки
        вызывает функцию concat_and_send_message(request, post, data)
        где post - экземпляр модели Post
        data - cleaned_data
    """

    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            sent = concat_and_send_message(request=request, post=post, data=data)


    # elif request.method == 'GET':
    else:
        form = EmailPostForm()
    context = {
        'form': form,
        'sent': sent,
        'post': post,
    }
    return render(request, 'blog/share.html', context=context)




class PostListView(ListView):

    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/list.html'