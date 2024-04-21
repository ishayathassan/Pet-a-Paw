from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Blog, Like, Comment
from home.models import UserProfile


# Create your views here.
@login_required
def home(request):
    user = request.user
    blogs = Blog.objects.select_related('user__userprofile').order_by('-created_at').all()
    liked_blogs = {}
    for blog in blogs:
        liked_blogs[blog.blog_id] = Like.objects.filter(blog=blog, user=user).exists()
    # Debug output
    print(liked_blogs)
    context = {'blogs': blogs, 'liked_blogs': liked_blogs}
    return render(request, 'blog/blog_home.html', context)


def create_blog(request):
    if request.method == 'POST':
        content = request.POST.get('blog-content')
        user = request.user
        if content:
            Blog.objects.create(content=content, user=user)
            return redirect('blog_home')  # Redirect to blog home page after successful post
    return redirect('blog_home')  # Redirect to blog home page if form submission fails


@login_required
def like_blog(request, blog_id):
    blog = get_object_or_404(Blog, blog_id=blog_id)

    # Create the Like object or retrieve existing one
    like, created = Like.objects.get_or_create(user=request.user, blog=blog)

    # If the Like object was created (i.e., it didn't exist before), increment the like count
    if created:
        blog.like_count += 1
        blog.save()

    return redirect('blog_home')


@login_required
def unlike_blog(request, blog_id):
    blog = Blog.objects.get(blog_id=blog_id)
    try:
        like = Like.objects.get(user=request.user, blog=blog)
        like.delete()
        blog.like_count -= 1
        blog.save()
    except Like.DoesNotExist:
        print("Does not exist")
    return redirect('blog_home')


def my_blogs(request, username):
    user = get_object_or_404(User, username=username)
    blogs = Blog.objects.filter(user=user).order_by('-created_at').all()
    context = {'blogs': blogs}
    return render(request, 'blog/my_blogs.html', context)


def single_blog(request, blog_id):
    blog = get_object_or_404(Blog, blog_id=blog_id)
    comments = Comment.objects.filter(blog=blog).order_by('-created_at').all()
    context = {'blog': blog, 'comments': comments}
    return render(request, 'blog/single_blog.html', context)


def post_comment(request, blog_id):
    blog = get_object_or_404(Blog, blog_id=blog_id)
    if request.method == 'POST':
        user = request.user
        content = request.POST.get('comment')
        if content:
            Comment.objects.create(content=content, blog=blog, user=user)
            blog.comment_count += 1
            blog.save()
            messages.success(request, 'Your comment has been posted successfully!')
    return redirect('single_blog', blog_id=blog_id)
