from django import template
from django.utils.safestring import mark_safe
from blog.models import Post
import markdown

register = template.Library()

@register.simple_tag()
def total_posts():
    return Post.rash.count()


@register.inclusion_tag('latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.rash.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))