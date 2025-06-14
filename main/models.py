from django.db import models
from django.contrib.auth.models import User  # 추가


# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE) 
    headline = models.CharField(max_length=100)                
    # nickname = models.CharField(max_length=20)  #삭제                
    mood = models.CharField(max_length=20, blank=True)         
    photo = models.ImageField(upload_to="post/", blank=True, null=True)  
    reflection = models.TextField()                           
    created_at = models.DateTimeField(auto_now_add=True)       
    is_shared = models.BooleanField(default=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    like=models.ManyToManyField(User, related_name='likes', blank=True)
    like_count=models.PositiveIntegerField(default=0)          

    def __str__(self):
        return f"[{self.headline}] by {self.author.username}"
    
    def summary(self):
        return self.reflection[:20]
    


class Comment(models.Model):
    content = models.TextField()
    pub_date = models.DateTimeField()
    writer = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post.headline} : {self.content[:20]} by {self.writer.username}"



