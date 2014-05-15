# coding: utf-8
#
# This file is part of Progdupeupl.
#
# Progdupeupl is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Progdupeupl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Progdupeupl. If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime

from django.db.models import Q

from django.contrib.auth.models import User

from pdp.utils import slugify

from pdp.forum.models import Category, Forum, Topic, Post
from pdp.forum.models import TopicRead, TopicFollowed
from pdp.tutorial.models import Tutorial, Part, Chapter, Extract

from rest_framework import generics, permissions

from .serializers import (CategorySerializer, ForumSerializer, TopicSerializer,
                          TopicFollowedSerializer, TopicReadSerializer,
                          PostSerializer, UserSerializer,
                          TutorialSerializer, ChapterSerializer,
                          PartSerializer, ExtractSerializer)

from .permissions import IsOwnerOrReadOnly

import django_filters


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryList(generics.ListAPIView):

    """
    List all category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CategoryDetail(generics.RetrieveAPIView):

    """
    Retrieve a Category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ForumFilter(django_filters.FilterSet):

    class Meta:
        model = Forum
        fields = ['category']


class ForumList(generics.ListAPIView):

    """
    List all forum.
    """
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    filter_class = ForumFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ForumDetail(generics.RetrieveAPIView):

    """
    Retrieve a Forum.
    """
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


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
    queryset = TopicFollowed.objects.all()
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
        lst = Post.objects.all().filter(topic=obj).order_by('-pubdate')
        if len(lst) > 0:
            obj.last_message = lst[0]

    def post_save(self, obj, created=True):
        # if i create a topic, i follow it
        tf = TopicFollowed(topic=obj, user=self.request.user)
        tf.save()


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
        lst = Post.objects.all().filter(topic=obj).order_by('-pubdate')
        if len(lst) > 0:
            obj.last_message = lst[0]

    def post_save(self, obj, created=True):
        # if i create a topic, i follow it
        tf = TopicFollowed(topic=obj, user=self.request.user)
        tf.save()


class PostFilter(django_filters.FilterSet):
    position_in_topic = django_filters.NumberFilter()

    class Meta:
        model = Post
        fields = ['author', 'topic', 'position_in_topic']


class PostList(generics.ListCreateAPIView):

    """
    List all Post, or create a new post.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_class = PostFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def pre_save(self, obj):
        obj.author = self.request.user
        if not obj.position_in_topic:
            obj.position_in_topic = obj.topic.get_post_count() + 1
        else:
            obj.update = datetime.now()

    # update the last message after post
    def post_save(self, obj, created=True):
        if not obj.update:
            tp = Topic.objects.all().get(pk=obj.topic.pk)
            tp.last_message = obj
            tp.save()


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
        obj.author = self.request.user
        if not obj.position_in_topic:
            obj.position_in_topic = obj.topic.get_post_count() + 1

        else:
            obj.update = datetime.now()

    # update the last message after post
    def post_save(self, obj, created=True):
        if not obj.update:
            tp = Topic.objects.all().get(pk=obj.topic.pk)
            tp.last_message = obj
            tp.save()


class TutorialFilter(django_filters.FilterSet):
    is_mini = django_filters.BooleanFilter()

    class Meta:
        model = Tutorial
        fields = ['is_mini']


class TutorialList(generics.ListCreateAPIView):

    """
    List all tutorial, or create a new tutorial.
    """
    queryset = Tutorial.objects.all().filter(is_visible=True)
    serializer_class = TutorialSerializer
    filter_class = TutorialFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def pre_save(self, obj):
        if not obj.pubdate:
            obj.pubdate = datetime.now()
            obj.slug = slugify(obj.title)

    def post_save(self, obj, created=True):
        obj.authors.add(self.request.user)


class TutorialDetail(generics.RetrieveUpdateDestroyAPIView):

    """
    Retrieve, update or delete a Tutorial.
    """
    queryset = Tutorial.objects.all().filter(is_visible=True)
    serializer_class = TutorialSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def pre_save(self, obj):
        if not obj.pubdate:
            obj.pubdate = datetime.now()
            obj.slug = slugify(obj.title)

    def post_save(self, obj, created=True):
        obj.authors.add(self.request.user)


class PartFilter(django_filters.FilterSet):
    position_in_tutorial = django_filters.NumberFilter()

    class Meta:
        model = Part
        fields = ['tutorial', 'position_in_tutorial']


class PartList(generics.ListCreateAPIView):

    """
    List all part, or create a new part.
    """
    queryset = Part.objects.all().filter(tutorial__is_visible=True)
    serializer_class = PartSerializer
    filter_class = PartFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def pre_save(self, obj):
        obj.slug = slugify(obj.title)


class PartDetail(generics.RetrieveUpdateDestroyAPIView):

    """
    Retrieve, update or delete a Part.
    """
    queryset = Part.objects.all().filter(tutorial__is_visible=True)
    serializer_class = PartSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def pre_save(self, obj):
        obj.slug = slugify(obj.title)


class ChapterFilter(django_filters.FilterSet):
    position_in_part = django_filters.NumberFilter()
    position_in_tutorial = django_filters.NumberFilter()

    class Meta:
        model = Chapter
        fields = ['part', 'tutorial',
                  'position_in_tutorial', 'position_in_part']


class ChapterList(generics.ListCreateAPIView):

    """
    List all chapter, or create a new chapter.
    """
    queryset = Chapter.objects.all().filter(Q(
        part__tutorial__is_visible=True) | Q(tutorial__is_visible=True))
    serializer_class = ChapterSerializer
    filter_class = ChapterFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def pre_save(self, obj):
        obj.slug = slugify(obj.title)


class ChapterDetail(generics.RetrieveUpdateDestroyAPIView):

    """
    Retrieve, update or delete a Chapter.
    """
    queryset = Chapter.objects.all().filter(Q(
        part__tutorial__is_visible=True) | Q(tutorial__is_visible=True))
    serializer_class = ChapterSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def pre_save(self, obj):
        obj.slug = slugify(obj.title)


class ExtractFilter(django_filters.FilterSet):
    position_in_chapter = django_filters.NumberFilter()

    class Meta:
        model = Extract
        fields = ['chapter', 'position_in_chapter']


class ExtractList(generics.ListCreateAPIView):

    """
    List all extract, or create a new extract.
    """
    queryset = Extract.objects.all()\
        .filter(Q(chapter__part__tutorial__is_visible=True) |
                Q(chapter__tutorial__is_visible=True))
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
    queryset = Extract.objects.all()\
        .filter(Q(chapter__part__tutorial__is_visible=True) |
                Q(chapter__tutorial__is_visible=True))
    serializer_class = ExtractSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
