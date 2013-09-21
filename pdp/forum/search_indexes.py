import datetime
from haystack import indexes
from pdp.forum.models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='author')
    topic = indexes.CharField(model_attr='topic')
    pubdate = indexes.DateTimeField(model_attr='pubdate')
    txt = indexes.CharField(model_attr='text')

    def get_model(self):
        return Post