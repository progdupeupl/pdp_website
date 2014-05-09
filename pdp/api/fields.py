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

from rest_framework import serializers


class TutorialSizeField(serializers.Field):
    def to_native(self, obj):
        if obj == 'S':
            return 'small'
        elif obj == 'M':
            return 'medium'
        elif obj == 'B':
            return 'big'
        else:
            raise NotImplementedError


class ChapterField(serializers.Field):
    def to_native(self, obj):
        return obj.pk
