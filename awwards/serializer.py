from rest_framework import serializers
from .models import *
from users.models import *

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'user', 'bio', 'image')

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'img', 'title', 'poster', 'description', 'timestamp', 'reviews', 'av_usability', 'av_content', 'av_design')