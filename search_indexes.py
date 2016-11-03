import datetime
from haystack import indexes
from models import Module


class ModuleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    slug = indexes.CharField(model_attr='slug')
    description = indexes.CharField(model_attr='description', default=None, )
    content_auto = indexes.EdgeNgramField(use_template=True)

    def get_model(self):
        return Module

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
