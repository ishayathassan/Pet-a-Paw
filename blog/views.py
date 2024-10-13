from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count
from .models import Blog, Comment, Tag
from django.db.models import Q


@login_required
def home(request):
    user = request.user
    search_input = request.GET.get('searchInput')

    if search_input:
        blogs = Blog.objects.select_related('user__userprofile').prefetch_related('liked_by').filter(
            Q(user__userprofile__name__icontains=search_input) |
            Q(content__icontains=search_input) |
            Q(tags__name__icontains=search_input)  # Search through tags as well
        ).distinct().order_by('-created_at')
    else:
        blogs = Blog.objects.select_related('user__userprofile').prefetch_related('liked_by').order_by(
            '-created_at').all()

    trending_tags = Tag.objects.annotate(num_blogs=Count('blog')).order_by('-num_blogs')[:5]
    liked_blogs = {blog.blog_id: user in blog.liked_by.all() for blog in blogs}
    context = {'blogs': blogs, 'liked_blogs': liked_blogs, 'trending_tags': trending_tags}
    return render(request, 'blog/blog_home.html', context)


@login_required
def create_blog(request):
    if request.method == 'POST':
        user = request.user
        content = request.POST.get('blog-content', '')

        # Extract tags from the content
        tags = [tag.strip('#') for tag in content.split() if tag.startswith('#')]

        # Remove tags from the content
        content = ' '.join(word for word in content.split() if not word.startswith('#'))

        # Create the blog post
        blog = Blog.objects.create(user=user, content=content)

        # Save tags associated with the blog
        if tags:
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                blog.tags.add(tag)

        return redirect('blog_home')  # Redirect to the blog home page after successful creation


@login_required
def like_blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    user = request.user

    if user in blog.liked_by.all():
        blog.liked_by.remove(user)
        blog.like_count -= 1
    else:
        blog.liked_by.add(user)
        blog.like_count += 1

    blog.save()

    return redirect(request.META.get('HTTP_REFERER', 'blog_home'))


@login_required
def unlike_blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    user = request.user

    if user in blog.liked_by.all():
        blog.liked_by.remove(user)
        blog.like_count -= 1
        blog.save()

    return redirect(request.META.get('HTTP_REFERER', 'blog_home'))


@login_required
def my_blogs(request, username):
    user = get_object_or_404(User, username=username)
    blogs = Blog.objects.filter(user=user).order_by('-created_at').all()
    context = {'blogs': blogs}
    return render(request, 'blog/my_blogs.html', context)


@login_required
def blog_profile(request, username):
    user = get_object_or_404(User, username=username)
    blogs = Blog.objects.filter(user=user).order_by('-created_at').all()
    context = {'blogs': blogs, 'user': user}
    return render(request, 'blog/blog_profile.html', context)


@login_required
def single_blog(request, blog_id):
    blog = get_object_or_404(Blog, blog_id=blog_id)
    comments = Comment.objects.filter(blog=blog).order_by('-created_at').all()
    context = {'blog': blog, 'comments': comments}
    return render(request, 'blog/single_blog.html', context)


@login_required
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


@login_required
def update_blog(request, blog_id):
    blog = get_object_or_404(Blog, blog_id=blog_id)
    if request.method == 'POST':
        new_content = request.POST.get('blog-content')
        if new_content:
            # Extract tags from the new content
            tags = [tag.strip('#') for tag in new_content.split() if tag.startswith('#')]
            # Remove tags from the content
            new_content = ' '.join(word for word in new_content.split() if not word.startswith('#'))
            # Update the blog content
            blog.content = new_content
            blog.save()
            # Clear existing tags associated with the blog
            blog.tags.clear()
            # Save new tags associated with the blog
            if tags:
                for tag_name in tags:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    blog.tags.add(tag)
            target_url = request.GET.get('next', reverse('my_blogs', kwargs={'username': request.user.username}))
            return redirect(target_url)  # Redirect to blog home page after successful update
    context = {'blog': blog}
    return render(request, 'blog/update_blog.html', context)


@login_required
def delete_blog(request, blog_id):
    # Fetch the blog post to delete
    blog = get_object_or_404(Blog, blog_id=blog_id)

    # Check if the request method is POST
    if request.method == 'POST':
        # Delete the blog post
        blog.delete()
        # Redirect to a specific URL after deletion
        return redirect('blog_home')  # Redirect to the blog home page after successful deletion

    # Render the delete confirmation template
    return render(request, 'blog/delete_blog.html', {'blog': blog})
