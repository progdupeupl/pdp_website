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

from django import template

register = template.Library()


@register.filter()
def upfirstletter(value):
    # This function uses value[0] instead of value[1] because value[0] seems
    # to be empty when used with the humane_date tag.
    first = value[1] if len(value) > 1 else ''
    remaining = value[2:] if len(value) > 2 else ''
    return first.upper() + remaining
