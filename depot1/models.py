# coding: utf-8
# Author: kaidee

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
	title = models.CharField(max_length=100, unique=True)
	description = models.TextField(blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	brandname = models.CharField(max_length=40, blank=True, null=True)
	color = models.CharField(max_length=20, blank=True, null=True)

	class Meta:
		ordering = ('-timestamp',)
        # verbose_name_plural = _('Categories')

	def __unicode__(self):
		return self.title

class Images(models.Model):
	title = models.CharField(max_length=50, blank=True, null=True)
	photo = models.ImageField(upload_to='static/img/%Y/%m', blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-timestamp',)

	def __unicode__(self):
		return self.title

class Product(models.Model):
	title = models.CharField(max_length=100,unique=True)
	category = models.ManyToManyField(Category)
	price = models.DecimalField(max_digits=18, decimal_places=2)
	description = models.TextField(blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	images = models.ForeignKey(Images, blank=True, null=True)
	# orders = models.ManyToManyField(order, through='LineItem')

	class Meta:
		ordering = ('-timestamp',)

	def __unicode__(self):
		return self.title

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    nickname = models.CharField(max_length=30)
    address = models.TextField(blank=True, null=True)

    # def save(self):
    #     if not self.nickname:
    #         self.nickname = self.user.username
    #     super(Profile, self).save()

    # def __unicode__(self):
    #     return self.nickname 

class Order(models.Model):
	name = models.CharField(max_length=50)
	address = models.TextField(blank=True, null=True)
	email = models.EmailField(blank=True, null=True)

	def __unicode__(self):
		return self.name

class LineItem(models.Model):
	product = models.ForeignKey(Product)
	order = models.ForeignKey(Order)
	unit_price = models.DecimalField(max_digits=8,decimal_places=2)
	quantity = models.IntegerField()

class Cart(object):
	"""docstring for Cart"""
	def __init__(self, *args, **kwargs):
		self.items = []
		self.total_price = 0
	def add_product(self, product):
		self.total_price += product.price
		for item in self.items:
			if item.product.id == product.id:
				item.quantity += 1
				return
		return self.items.append(LineItem(product=product, unit_price=product.price, quantity=1))