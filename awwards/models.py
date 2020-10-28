from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator 

class Project(models.Model):
    # img = models.ImageField(default='default.png', upload_to='images')
    img = models.ImageField(upload_to='images',null=True)
    title = models.CharField(default='My Project', max_length = 30)
    description = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    reviews = models.CharField(max_length = 30, blank = True, default = 0)
    link = models.CharField(default='No link', max_length = 120)
    av_usability = models.CharField(max_length = 30, default = 0)
    av_design = models.CharField(max_length = 30, default = 0)
    av_content = models.CharField(max_length = 30, default = 0)
    rating = models.CharField(max_length = 30, default = 0)

    def __str__(self):
        return self.title

    @classmethod
    def search_by_title(cls,search_term):
        projectis = cls.objects.filter(title__icontains=search_term)
        return projectis

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})


    def get_project_by_id(project_id):
        project = Project.objects.get(pk = project_id)
        return project

class Rating(models.Model):
    project = models.CharField(max_length = 30, default = '')
    poster = models.ForeignKey(User,on_delete=models.CASCADE)
    usability = models.IntegerField(choices=((1, 1),(2, 2),(3, 3),(4, 4),(5, 5),(6, 6), (7, 7),(8, 8), (9, 9), (10, 10)), blank=True)
    content = models.IntegerField(choices=((1, 1),(2, 2),(3, 3),(4, 4),(5, 5),(6, 6), (7, 7),(8, 8), (9, 9), (10, 10)), blank=True)
    design = models.IntegerField(choices=((1, 1),(2, 2),(3, 3),(4, 4),(5, 5),(6, 6), (7, 7),(8, 8), (9, 9), (10, 10)), blank=True)

    def __str__(self):
        return self.poster
    average = models.IntegerField(blank = True, default=0)

class Review(models.Model):
    project = models.CharField(max_length = 30, default = '')
    review = models.TextField(max_length = 30)
    poster = models.ForeignKey(User,on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.review

class ProjectVote(models.Model):
    voter = models.CharField(default='My Project', max_length = 80)
    voted = models.CharField(default='My Project', max_length = 80)
    published_date = models.DateField(auto_now_add=True, null=True)
    design = models.PositiveIntegerField(default=1, choices=((1, 1),(2, 2),(3, 3),(4, 4),(5, 5),(6, 6), (7, 7),(8, 8), (9, 9), (10, 10)))
    usability = models.PositiveIntegerField(default=1, choices=((1, 1),(2, 2),(3, 3),(4, 4),(5, 5),(6, 6), (7, 7),(8, 8), (9, 9), (10, 10)))
    content = models.PositiveIntegerField(default=1, choices=((1, 1),(2, 2),(3, 3),(4, 4),(5, 5),(6, 6), (7, 7),(8, 8), (9, 9), (10, 10)))

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return f'{self.design} marks'