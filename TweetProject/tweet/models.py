from django.db import models
from django.contrib.auth.models import User


class Tweet(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)# means if a user is deleted than the data of it inside the tweet model will also gets deleted
    text=models.TextField(max_length=300)
    photo=models.ImageField(upload_to='photos/',blank=True,null=True)
    video=models.FileField(upload_to='video',blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.username}-{self.text[:10]}'# it is used to tell how the twweet obj will look in py string

# Create your models here.
