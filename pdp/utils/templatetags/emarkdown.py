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

from pdp.utils.templatetags import cssstyles
import markdown
import bleach

from django import template
from django.utils.safestring import mark_safe

md_cssstyle = cssstyles.StyleExtension()

register = template.Library()


@register.filter(needs_autoescape=False)
def emarkdown(value):
    # Allowed output tags from user raw HTML input and markdown generation
    allowed_tags = ['div', 'span', 'p', 'pre', 'hr', 'img', 'br',
                    'strong', 'em', 'i', 'b', 'code', 'sub', 'sup', 'del',
                    'a', 'abbr', 'blockquote',
                    'ul', 'ol', 'li',
                    'table', 'thead', 'tbody', 'tr', 'td', 'th']

    # Add h1…h6 titles, have a more beautiful way to do it?
    [allowed_tags.append('h{}'.format(i + 1)) for i in range(6)]

    allowed_attrs = {
        '*': ['class', 'id'],
        'a': ['href', 'title'],
        'img': ['src', 'alt'],
    }

    return mark_safe('<div class="markdown">{0}</div>'.format(
        bleach.clean(
            markdown.markdown(value, extensions=[
                              md_cssstyle,
                              'codehilite(force_linenos=True)',
                              'extra']),
            tags=allowed_tags,
            attributes=allowed_attrs)
        .encode('utf-8')))
