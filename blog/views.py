from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .forms import Email, CommentForm
from .models import Post
from taggit.models import Tag
import smtplib


def home(request, tag_slug=None):
    object_list = Post.rash.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tag__in=[tag])
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts': posts,
        'tag': tag,
        'page': page,
    }
    return render(request, 'list.html', context)


class BlogList(ListView):
    queryset = Post.rash.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'list.html'


def share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='draft')
    sent = False
    form = Email()
    if request.method == 'POST':
        form = Email(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{}({}) recommends you to read "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read {} at {} of "{}" having comments:{}'.format(post.title, post_url, cd['name'],
                                                                        cd['comments'])
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.starttls()
            mail.ehlo()
            mail.login('rashmitpankhania@gmail.com', 'Putpak23#')
            mail.sendmail(cd['email'], [cd['to']], message, mail_options=[subject],)
            mail.close()
            sent = True
        else:
            form = Email()

    context = {
        'post': post,
        'form': form,
        'sent': sent,
    }
    return render(request, 'share.html', context)


def detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='draft',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    post_tag_ids = post.tag.values_list('id', flat=True)
    similar_posts = Post.rash.filter(tag__in=post_tag_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tag')).order_by('-same_tags', '-publish')[:4]
    context = {
        'post': post,
        'comment_form': comment_form,
        'comments': comments,
        'similar_posts': similar_posts
    }
    return render(request, 'detail.html', context)
