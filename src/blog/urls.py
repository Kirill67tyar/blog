from django.urls import path, include
from blog.views import post_list, post_retrieve, post_share, PostListView, experiments

app_name = 'blog'

urlpatterns = [
    # path('', post_list, name='list'),
    path('', PostListView.as_view(), name='list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', post_retrieve, name='retrieve'),
    path('<int:post_id>/share/', post_share, name='share'),

    # experiment--------------------------------------------
    path('experiments/', experiments, name='experiments'),

]