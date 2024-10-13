from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Blog(models.Model):
    blog_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name='liked_blogs', blank=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"Blog {self.blog_id} by {self.user.username}"


class Comment(models.Model):
    created_at = models.DateTimeField(primary_key=True, auto_now_add=True)
    content = models.TextField()
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.blog.blog_id}"
