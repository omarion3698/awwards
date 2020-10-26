from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import generic
from django.db.models import F
from users.models import Profile
from . models import Project, ProjectVote
from django.contrib.auth.models import User
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProfileSerializer, ProjectSerializer
from rest_framework import status
from .permissions import IsAdminOrReadOnly

def welcome(request):
    one_entry = Project.objects.filter(id=1)
    two_entry = Project.objects.filter(pk=2)
    three_entry = Project.objects.filter(id=3)
    four_entry = Project.objects.filter(id=4)
    five_entry = Project.objects.filter(id=3)

    return render(request, 'awwards/welcome.html', {"one_entry":one_entry, "two_entry":two_entry, "three_entry":three_entry, "four_entry":four_entry, "five_entry":five_entry})

def home(request):
    current_user = request.user
    projects = Project.objects.all()
    users = Profile.objects.all()

    form = ReviewForm()

    return render(request, 'awwards/home.html', {'projects':projects,'current_user':current_user,'users':users,'form':form})


def profile(request):
    title = request.user.username
    try:
        current_user=request.user
        projects=Project.objects.filter(poster=current_user).all()
        profile=Profile.get_profile(current_user)

        if request.method == 'POST':
            form = ProjectForm(request.POST, request.FILES)
            if form.is_valid():
                project = form.save(commit=False)
                user_profile = Profile.get_profile(current_user)
                project.poster = current_user
                project.save()
            return redirect('profile')
        else:
            form = ProjectForm()

    except Exception as e:
        raise Http404()

    return render(request,"awwards/profile.html",{'profile':profile, "title":title, "projects":projects,"form":form})


@login_required(login_url='/login/')
def review(request,project_id):
    try:
        project=Project.objects.get(id=project_id)
    except Exception as e:
        raise  Http404()

    if request.method=='POST':
        current_user=request.user
        form=ReviewForm(request.POST)
        if form.is_valid:
            reviews=form.save(commit=False)
            reviews.poster=current_user
            reviews.project= project_id
            reviews.save()
    else:
        form=ReviewForm()

    ratings = Rating.objects.filter(project = project_id).all()

    total = 0
    number = len(ratings)

    for rating in ratings:
        total += rating.average
        rate = total/number
        project.rating = rate

    reviews = Review.objects.filter(project = project_id).all()
    return render(request,"awwards/review.html",{"project":project,'form':form,"reviews":reviews, "ratings":ratings})

@login_required(login_url='/login/')
def rate(request, project_id):
    try:
        project=Project.objects.get(id=project_id)
    except Exception as e:
        raise  Http404()

    if request.method=='POST':
        current_user=request.user
        check = Rating.objects.filter(poster = current_user, project = project_id).all()
        form=RateForm(request.POST)
        if form.is_valid:
            if len(check) < 1:
                ratings=form.save(commit=False)
                if ratings.usability < 11 or ratings.content < 11 or ratings.design < 11:
                    ratings.poster=current_user
                    ratings.project= project_id
                    ratings.average = (ratings.usability + ratings.content + ratings.design)/3
                    ratings.save()
                else:
                    message = 'Rating failed! One of the values is not within the defined range'
                    return redirect('rate', {"message":message})
            else:
                Rating.objects.filter(poster = current_user, project = project_id).delete()
                ratings=form.save(commit=False)
                if ratings.usability < 11 or ratings.content < 11 or ratings.design < 11:
                    ratings.poster=current_user
                    ratings.project= project_id
                    ratings.average = (ratings.usability + ratings.content + ratings.design)/3
                    ratings.save()
                else:
                    message = 'Rating failed! One of the values is not within the defined range'
                    return redirect('rate', {"message":message})

            return redirect('review', project_id)

    else:
        form=RateForm()

    return render(request,"awwards/rate.html",{"project":project,'form':form})

class ProjectListView(ListView):
    model = Project
    ordering = ['-timestamp']

class UserProjectListView(ListView):
    model = Project
    context_object_name = 'object'
    template_name = 'awwards/user_projects.html'
    ordering = ['-timestamp']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Project.objects.filter(poster=user).order_by('-timestamp')

class ProjectDetailView(DetailView):
    model = Project

class ProjectCreateView(CreateView):
    model = Project
    fields = ['img','title','description','link']

    def form_valid(self, form):
        # we override the create validation to tell it this is the author of the post. Otherwise we'll get an integrity error
        form.instance.poster = self.request.user
        return super().form_valid(form)

@login_required(login_url='/login/')
def search_results(request):

    if 'project' in request.GET and request.GET["project"]:
        search_term = request.GET.get("project")
        searched_projects = Project.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'awwards/search.html',{"message":message,"projects": searched_projects})
    else:
        message = "You haven't searched for any term"
        return render(request, 'awwards/search.html',{"message":message})

@login_required(login_url='/login/')
def rating(request, pk):
    project = get_object_or_404(Project, pk=pk)
    rating = ProjectVote.objects.all()
    if request.method == 'POST':
        form = RatingForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            rating=form.save(commit=False)
            rating.voter = request.user.id
            rating.voted = project.id
            rating.save()
            usability = form.cleaned_data.get('usability')
            content = form.cleaned_data.get('content')
            design = form.cleaned_data.get('design')
            
            messages.success(request, f'You have rated this project usability: {usability}, design: {design}, content: {content}')
            return redirect('awwards-home')
    else:
        form = RatingForm()
    return render(request, 'awwards/rating.html', {'form': form, "project":project})

class ProjectsList(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get(self, request, format=None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects, many=True)

        return Response(serializers.data)

    def post(self, request, format = None):
        serializers = ProjectSerializer(data = request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status = status.HTTP_201_CREATED)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfilesList(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get(self, request, format=None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles, many=True)

        return Response(serializers.data)

    def post(self, request, format = None):
        serializers = ProfileSerializer(data = request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status = status.HTTP_201_CREATED)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get_profile(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        profile = self.get_profile(pk)
        serializers = ProfileSerializer(profile)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        profile = self.get_profile(pk)
        serializers = ProfileSerializer(profile, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        profile = self.get_profile(pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get_project(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        project = self.get_project(pk)
        serializers = ProjectSerializer(project)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        project = self.get_project(pk)
        serializers = ProjectSerializer(project, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        project = self.get_project(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def about(request):
    return render(request, 'awwards/about.html')