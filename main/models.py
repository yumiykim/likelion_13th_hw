from django.db import models

# Create your models here.


class Post(models.Model):
    headline = models.CharField(max_length=100)                
    nickname = models.CharField(max_length=20)                 
    mood = models.CharField(max_length=20, blank=True)         
    photo = models.ImageField(upload_to="post/", blank=True, null=True)  
    reflection = models.TextField()                           
    created_at = models.DateTimeField(auto_now_add=True)       
    is_shared = models.BooleanField(default=True)              

    def __str__(self):
        return f"[{self.headline}] by {self.nickname}"
    
    def summary(self):
        return self.reflection[:20]
