from django import template
from django.utils.safestring import mark_safe
from django.db.models import Count
from blog.models import Post
import markdown


register = template.Library()

# ------------------------------------- Simple tags
@register.simple_tag
def total_posts():
    return Post.published.count()

@register.simple_tag
def show_most_comment_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]




# ------------------------------------- Inclusion tags
@register.inclusion_tag(filename='../templates/template_tags/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts, 'count': count}




# ------------------------------------- Filters
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))





# this is a post formatted with markdown
# --------------------------------------
# *This is emphasized* and **This is emphasized**
# Here is a list:
# * One
# * Two
# * Three