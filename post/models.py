from django.db import models
from user_app.models import Account

class Post(models.Model):
    author = models.ForeignKey(Account,related_name='posts',on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=4000)
    post_image=models.FileField(upload_to="post_image",null=True,blank=True)
    post_date=models.DateField(auto_now_add=True)
    liked_by= models.ManyToManyField(Account,blank=True,related_name='liked_by')
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    created=models.DateTimeField(auto_now_add=True)
    body=models.TextField(blank=False,null=False)
    owner=models.ForeignKey(Account,related_name='comments',on_delete=models.CASCADE)
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
 
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return self.body