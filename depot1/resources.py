from django.core.urlresolvers import reverse
from rest_framework.views import View
from rest_framework.resources import ModelResource
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from models import *

class LineItemResource(ModelResource):
	# class Meta:
    	model = LineItem
    	fields = ('product', 'unit_price', 'quantity')
    	def product(self, instance):
    		return instance.product.title