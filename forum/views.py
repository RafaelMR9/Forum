from django.shortcuts import render
from django.views.generic.base import View
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Topic
from taggit.models import Tag
from .forms import TopicModel2Form, UserModel2Form

# Create your views here.
class index(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse_lazy("forum:topics-list"))


class TopicListView(View):
    def get(self, request, *args, **kwargs):
        topics = Topic.objects.order_by('-date')
        tags = Tag.objects.all()
        context = { 'topics': topics, 'tags': tags }
        return render(request, 'forum/pages/topicsList.html', context)


class TopicDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        topic = Topic.objects.get(pk=pk)
        tags = Tag.objects.all()
        context = { 'topic': topic, 'tags':tags }
        return render(request, 'forum/pages/topicsDetail.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        topic = Topic.objects.get(pk=pk)
        topic.delete()
        return HttpResponseRedirect(reverse_lazy("forum:topics-list"))

class TopicUpdateView(View):
    def get(self, request, pk, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/login")
        topic = Topic.objects.get(pk=pk)
        tags = Tag.objects.all()
        form = TopicModel2Form(instance=topic)
        context = { 'form': form, 'tags':tags }
        return render(request, 'forum/pages/topicsUpdate.html', context)

    def post(self, request, pk, *args, **kwargs):
        user = request.user
        topic = Topic.objects.get(pk=pk)
        tags = Tag.objects.all()
        form = TopicModel2Form(request.POST, instance=topic)
        
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = user
            topic.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse_lazy("forum:topics-detail", kwargs={'pk':pk}))
        else:
            context = { 'form': form, 'tags':tags }
            return render(request, 'forum/pages/topicsUpdate.html', context)


class TopicCreateView(View):
    def get(self, request, *args, **kwargs):
        tags = Tag.objects.all()
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/login")
        context = { 'form': TopicModel2Form, 'tags': tags }
        return render(request, 'forum/pages/topicsCreate.html', context)

    def post(self, request, *args, **kwargs):
        user = request.user
        form = TopicModel2Form(request.POST)
        
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = user
            topic.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse_lazy("forum:topics-list"))


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        tags = Tag.objects.all()
        context = { 'form': UserModel2Form, 'tags':tags }
        return render(request, 'registration/signUp.html', context)

    def post(self, request, *args, **kwargs):
        form = UserModel2Form(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse_lazy("forum:topics-list"))