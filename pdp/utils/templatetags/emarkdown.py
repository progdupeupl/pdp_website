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

import markdown
import bleach

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(needs_autoescape=False)
def emarkdown(value, post_id=None):
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
        'abbr': ['title'],
    }

    text = markdown.markdown(value, extensions=[
                             'codehilite(linenums=True)',
                             'extra'])

    if post_id is not None:
        if not isinstance(post_id, str):
            post_id = str(post_id)

        # Adapt backlinks from footnotes to text
        text = text.replace('id="fnref:', 'id="fnref:{}_'.format(post_id))
        text = text.replace('href="#fnref:', 'href="#fnref:{}_'.format(
            post_id))

        # Adapt links from text to footnotes
        text = text.replace('id="fn:', 'id="fn:{}_'.format(post_id))
        text = text.replace('href="#fn:', 'href="#fn:{}_'.format(post_id))

    return mark_safe('<div class="markdown">{0}</div>'.format(
        bleach.clean(
            text,
            tags=allowed_tags,
            attributes=allowed_attrs
        )))
