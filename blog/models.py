from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    email = models.EmailField(null=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=45, null=True)
    city = models.CharField(max_length=40, null=True)
    country = models.CharField(max_length=40, null=True)
    address = models.CharField(max_length=100, null=True)
    postal = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.user} profile'


class Post(models.Model):
    title = models.CharField(max_length=80)
    text = models.TextField()
    author = models.CharField(max_length=50)
    photo = models.ImageField(default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment by {}, {}'.format(self.name, self.body)
