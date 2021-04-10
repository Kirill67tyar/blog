from django.urls import path, include
from blog.views import post_list, post_retrieve, post_share, PostListView, experiments
from blog.feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    path('', post_list, name='list'),
    path('tag/<slug:tag_slug>/', post_list, name='list_by_tag'),
    # path('', PostListView.as_view(), name='list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', post_retrieve, name='retrieve'),
    path('<int:post_id>/share/', post_share, name='share'),
    path('feed/', LatestPostsFeed(), name='post_feed'),

    # experiment--------------------------------------------
    path('experiments/', experiments, name='experiments'),

]