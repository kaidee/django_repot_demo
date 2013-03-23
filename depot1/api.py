from tastypie.resources import ModelResource
from depot1.models import LineItem
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization


class LineItemResource(ModelResource):
	class Meta:
		queryset = LineItem.objects.all()
		# resource_name = 'l'
		authorization = DjangoAuthorization()