from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(default='Available', max_length = 30)
    image = models.ImageField(default='profile.png', upload_to='images')

    def __str__(self):
        return f'{self.user.username} Profile'

    @classmethod
    def get_profile(cls,user):
        profile=cls.objects.get(user=user)
        return profile