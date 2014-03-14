# coding: utf-8
#
# This file is part of Progdupeupl.
#
# Progdupeupl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Progdupeupl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Progdupeupl. If not, see <http://www.gnu.org/licenses/>.

from django.contrib.auth.models import User
from rest_framework import serializers
from pdp.forum.models import Category, Forum, Topic, Post
from pdp.forum.models import TopicRead, TopicFollowed
from pdp.article.models import Article
from pdp.tutorial.models import Tutorial, Part, Chapter, Extract


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.Field()

    class Meta:
        model = Category
        fields = ('id', 'title', 'position', 'slug')


class ForumSerializer(serializers.ModelSerializer):
    slug = serializers.Field()

    class Meta:
        model = Forum
        fields = ('id', 'title', 'subtitle',
                  'category', 'position_in_category', 'slug')


class TopicReadSerializer(serializers.ModelSerializer):
    user = serializers.Field(source='user.username')

    class Meta:
        model = TopicRead
        fields = ('id', 'topic', 'post', 'user')


class TopicFollowedSerializer(serializers.ModelSerializer):
    user = serializers.Field(source='user.username')

    class Meta:
        model = TopicFollowed
        fields = ('id', 'topic', 'user')


class TopicSerializer(serializers.ModelSerializer):
    author = serializers.Field(source='author.username')
    is_locked = serializers.Field()
    is_solved = serializers.Field()
    is_sticky = serializers.Field()
    last_message = serializers.Field()

    class Meta:
        model = Topic
        fields = ('id', 'title', 'subtitle', 'forum', 'author',
                  'last_message', 'pubdate', 'is_solved', 'is_locked',
                  'is_sticky')


class PostSerializer(serializers.ModelSerializer):
    author = serializers.Field(source='author.username')
    update = serializers.Field()
    position_in_topic = serializers.Field()

    class Meta:
        model = Post
        fields = ('id', 'text', 'topic', 'author',
                  'pubdate', 'update', 'position_in_topic')


class UserSerializer(serializers.ModelSerializer):
    topics = serializers.PrimaryKeyRelatedField(many=True, read_only='true')
    articles = serializers.PrimaryKeyRelatedField(many=True, read_only='true')
    topics_read = serializers.PrimaryKeyRelatedField(
        many=True, read_only='true')
    topics_followed = serializers.PrimaryKeyRelatedField(
        many=True, read_only='true')
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only='true')

    class Meta:
        model = User
        fields = ('id', 'username', 'topics', 'posts',
                  'topics_read', 'topics_followed', 'articles')


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.Field(source='author.username')

    class Meta:
        model = Article
        fields = ('id', 'title', 'description',
                  'text', 'author', 'pubdate', 'is_visible')


class TutorialSerializer(serializers.ModelSerializer):
    is_visible = serializers.Field()
    is_pending = serializers.Field()
    pubdate = serializers.Field()
    slug = serializers.Field()
    authors = serializers.Field()

    class Meta:
        model = Tutorial
        fields = ('id', 'title', 'description', 'authors', 'introduction',
                  'conclusion', 'slug', 'pubdate',
                  'is_mini', 'is_visible', 'is_pending')


class PartSerializer(serializers.ModelSerializer):
    slug = serializers.Field()

    class Meta:
        model = Part
        fields = ('id', 'tutorial', 'position_in_tutorial',
                  'title', 'introduction', 'conclusion', 'slug')


class ChapterSerializer(serializers.ModelSerializer):
    slug = serializers.Field()

    class Meta:
        model = Chapter
        fields = ('id', 'part', 'position_in_part', 'tutorial',
                  'position_in_tutorial', 'title',
                  'introduction', 'conclusion', 'slug')


class ExtractSerializer(serializers.ModelSerializer):

    class Meta:
        model = Extract
        fields = ('id', 'chapter', 'title', 'position_in_chapter', 'text')
