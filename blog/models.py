from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Blog(models.Model):
    blog_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Blog {self.blog_id} by {self.user.username}"


class Like(models.Model):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} likes {self.blog.title}'


class Comment(models.Model):
    created_at = models.DateTimeField(primary_key=True, auto_now_add=True)
    content = models.TextField()
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.blog.title}"
