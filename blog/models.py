from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField


class Post(models.Model):
    title = RichTextField()
    content = RichTextField()
    excerpt = models.TextField()
    likes = models.ManyToManyField(User, blank=True, related_name='liked_posts')
    featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    featured_image = models.ImageField(upload_to='posts/images/', null=True, blank=True)
    video = models.FileField(upload_to='posts/videos/', null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"
    
    
# Create your models here.
