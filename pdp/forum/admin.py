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

from django.contrib import admin
from .models import Category, Forum, Topic, Post, TopicRead, TopicFollowed

admin.site.register(Category)
admin.site.register(Forum)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(TopicRead)
admin.site.register(TopicFollowed)
