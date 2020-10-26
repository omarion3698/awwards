from .models import *
from django import forms

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['poster', 'timestamp', 'reviews', 'usability', 'content', 'design', 'rating']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude=['poster','project', 'upload_date']

class RateForm(forms.ModelForm):
    class Meta:
        model=Rating
        exclude=['poster', 'project', 'average']

class RatingForm(forms.ModelForm):
    class Meta:
        model = ProjectVote
        fields = ['design', 'usability', 'content']