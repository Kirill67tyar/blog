from django.urls import path, include
from blog.views import post_list, post_retrieve, post_detail

app_name = 'blog'

urlpatterns = [
    path('', post_list, name='list'),
    # path('<int:year>/<int:month>/<int:day>/<str:post>/', post_retrieve, name='retrieve'),
    path('<int:year>/<int:month>/<int:day>/<str:slug>/', post_detail, name='retrieve'),

]