from datetime import datetime

from django.shortcuts import redirect, get_object_or_404

from django.http import Http404
from django.http import HttpResponse

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from pdp.utils import render_template, slugify
from pdp.utils.paginator import paginator_range

from pdp.forum.models import Category, Forum, Topic, Post, TopicRead, TopicFollowed, POSTS_PER_PAGE, TOPICS_PER_PAGE
from pdp.article.models import Article
from pdp.tutorial.models import Tutorial, Part, Chapter, Extract

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins, generics, permissions, status

from serializers import CategorySerializer, ForumSerializer, TopicSerializer, TopicFollowedSerializer, TopicReadSerializer, PostSerializer, UserSerializer, ArticleSerializer, TutorialSerializer, ChapterSerializer, PartSerializer, ExtractSerializer  
from permissions import IsOwnerOrReadOnly

import django_filters

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CategoryList(generics.ListCreateAPIView):
    """
    List all category, or create a new category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a Category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ForumFilter(django_filters.FilterSet):
    class Meta:
        model = Forum
        fields = ['category']

class ForumList(generics.ListCreateAPIView):
    """
    List all forum, or create a new forum.
    """
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    filter_class = ForumFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ForumDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a Forum.
    """
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class TopicReadFilter(django_filters.FilterSet):
    class Meta:
        model = TopicRead
        fields = ['user']

class TopicReadList(generics.ListCreateAPIView):
    """
    List all Topic read, or create a new topic read.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = TopicRead.objects.all()
    serializer_class = TopicReadSerializer
    filter_class = TopicReadFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def pre_save(self, obj):
        obj.user = self.request.user

class TopicReadDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a Topic read.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    queryset = TopicRead.objects.all()
    serializer_class = TopicReadSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def pre_save(self, obj):
        obj.user = self.request.user

class TopicFollowedFilter(django_filters.FilterSet):
    class Meta:
        model = TopicFollowed
        fields = ['user']

class TopicFollowedList(generics.ListCreateAPIView):
    """
    List all Topic followed, or create a new topic followed.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = TopicRead.objects.all()
    serializer_class = TopicFollowedSerializer
    filter_class = TopicFollowedFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def pre_save(self, obj):
        obj.user = self.request.user

class TopicFollowedDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a Topic followed.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    queryset = TopicRead.objects.all()
    serializer_class = TopicFollowedSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def pre_save(self, obj):
        obj.user = self.request.user

class TopicFilter(django_filters.FilterSet):
    is_solved = django_filters.BooleanFilter()
    is_locked = django_filters.BooleanFilter()
    is_sticky = django_filters.BooleanFilter()
    class Meta:
        model = Topic
        fields = ['author', 'forum', 'is_solved', 'is_locked', 'is_sticky']

class TopicList(generics.ListCreateAPIView):
    """
    List all Topic, or create a new topic.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    filter_class = TopicFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def pre_save(self, obj):
        obj.author = self.request.user

class TopicDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a Topic.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def pre_save(self, obj):
        obj.author = self.request.user

class PostList(generics.ListCreateAPIView):
    """
    List all Post, or create a new post.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def pre_save(self, obj):
        obj.author = self.request.user

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a Post.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def pre_save(self, obj):
        obj.author = self.request.user# Create your views here.

class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = ['author']

class ArticleList(generics.ListCreateAPIView):
    """
    List all article, or create a new article.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_class = ArticleFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a Article.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def pre_save(self, obj):
        obj.author = self.request.user

class TutorialFilter(django_filters.FilterSet):
    is_visible = django_filters.BooleanFilter()
    is_pending = django_filters.BooleanFilter()
    class Meta:
        model = Tutorial
        fields = ['is_visible', 'is_pending']

class TutorialList(generics.ListCreateAPIView):
    """
    List all tutorial, or create a new tutorial.
    """
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer
    filter_class = TutorialFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class TutorialDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a Tutorial.
    """
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class PartFilter(django_filters.FilterSet):
    class Meta:
        model = Part
        fields = ['tutorial']

class PartList(generics.ListCreateAPIView):
    """
    List all part, or create a new part.
    """
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    filter_class = PartFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class PartDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a Part.
    """
    queryset = Part.objects.all()
    serializer_class = PartSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ChapterFilter(django_filters.FilterSet):
    class Meta:
        model = Chapter
        fields = ['part']

class ChapterList(generics.ListCreateAPIView):
    """
    List all chapter, or create a new chapter.
    """
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    filter_class = ChapterFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ChapterDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a Chapter.
    """
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ExtractFilter(django_filters.FilterSet):
    class Meta:
        model = Extract
        fields = ['chapter']

class ExtractList(generics.ListCreateAPIView):
    """
    List all extract, or create a new extract.
    """
    queryset = Extract.objects.all()
    serializer_class = ExtractSerializer
    filter_class = ExtractFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ExtractDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a Extract.
    """
    queryset = Extract.objects.all()
    serializer_class = ExtractSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
