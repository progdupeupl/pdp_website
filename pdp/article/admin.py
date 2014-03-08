# coding: utf-8

from django.contrib import admin
from .models import Article, ArticleCategory

admin.site.register(Article)
admin.site.register(ArticleCategory)
