from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='blog_home'),
    path('create/', views.create_blog, name='create_blog'),
    path('like/<int:blog_id>/', views.like_blog, name='like_blog'),
    path('unlike/<int:blog_id>/', views.unlike_blog, name='unlike_blog'),
    path('my_blog/<slug:username>/', views.my_blogs, name='my_blogs'),
    path('blogs/<int:blog_id>', views.single_blog, name='single_blog'),
    path('post-comment/<int:blog_id>/', views.post_comment, name='post_comment'),
    path('update-blog/<int:blog_id>/', views.update_blog, name='update_blog'),
    path('delete-blog/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    path('profile/<slug:username>/', views.blog_profile, name='blog_profile'),

]
