from django.db.models import Q
from haystack import indexes

from pdp.tutorial.models import Extract


class ExtractIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    chapter = indexes.CharField(model_attr='chapter')
    txt = indexes.CharField(model_attr='text')

    def get_model(self):
        return Extract

    def index_queryset(self, using=None):
        '''Used when the entire index for model is updated.'''
        return self.get_model().objects\
            .filter(Q(chapter__tutorial__is_visible=True) |
                    Q(chapter__part__tutorial__is_visible=True))
