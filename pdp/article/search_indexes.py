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

from haystack import indexes
from pdp.article.models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    author = indexes.CharField(model_attr='author')
    description = indexes.CharField(model_attr='description')
    pubdate = indexes.DateTimeField(model_attr='pubdate')
    txt = indexes.CharField(model_attr='text')
    tags = indexes.MultiValueField()

    def get_model(self):
        return Article

    def prepare_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects\
            .filter(is_visible=True)
