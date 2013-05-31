# coding: utf-8
# Author: kaidee

from django import forms
from depot1.forms import *
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404

from django.template.loader import get_template
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.db import transaction
from rest_framework.views import View

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from depot1.models import *
from forms import *
import ImageFile
# from PIL import Image
import datetime

def store_view(request):
    cart = request.session.get("cart", None)
    products = Product.objects.all()
    paginator = Paginator(products ,5)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        products = paginator.page(page)
    except :
        products = paginator.page(paginator.num_pages)
    return render_to_response("store.html", {
        "products": products, "cart": cart
        }, context_instance=RequestContext(request)
        )
	
def create_product(request):
    form = ProductForm(request.POST or None)    
    if form.is_valid():
        form.save()
        form = ProductForm()
    return render_to_response("create_product.html", {
        "form": form,
        }, context_instance=RequestContext(request)
        )

def upload_image(request):
    form = ImagesForm(request.POST or None)    
    if form.is_valid():
        form.save()
        form = ImagesForm()
    return render_to_response("upload_image.html", {
        "form": form
        }, context_instance=RequestContext(request))
    
# @login_required
def list_product(request):
  
    list_items = Product.objects.all()
    paginator = Paginator(list_items ,5)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)
    return render_to_response("list_product.html", {
        "list_items": list_items,
        }, context_instance=RequestContext(request)
        )

def view_product(request, id):
    product_item = Product.objects.get(id = id)

    return render_to_response("view_product.html", {
        "product_item": product_item,
        }, context_instance=RequestContext(request)
        )

def edit_product(request, id):
    product_instance = Product.objects.get(id=id)
    form = ProductForm(request.POST or None, instance = product_instance)
    if form.is_valid():
        form.save()

    return render_to_response("edit_product.html", {
        "form": form,
        }, context_instance=RequestContext(request)
        )

def delete_product(request, id):
    product_item = Product.objects.get(id = id)
    try:
        Product.objects.get(id = id).delete()
    except:
        pass
    

    return render_to_response("delete_product.html", {
        "product_item": product_item,
        }, context_instance=RequestContext(request)
        )

def view_cart(request):
    cart = request.session.get("cart", None)
    if  not cart:
        cart = Cart()
        request.session["cart"] = cart

    return render_to_response("view_cart.html", {"cart": cart})

def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    cart = request.session.get("cart",None)
    if not cart:
      cart =Cart()
      request.session["cart"] = cart
    cart.add_product(product)
    request.session["cart"] = cart
    return HttpResponseRedirect('/cart/view/')

def clean_cart(request):
    request.session['cart'] = Cart()
    return HttpResponseRedirect("/store/")


@transaction.commit_on_success
def create_order(request):
    form = OrderForm(request.POST or None)
    if form.is_valid():
        order = form.save()
        # order = OrderForm()
        for item in request.session['cart'].items:
          # order = Order.objects.get(name=request.name)
                    # order = Order.objects.get(id=1)
          item.order = order
          item.save()
        clean_cart(request)
        return HttpResponseRedirect("/store/")
        # form = OrderForm()
    return render_to_response("create_order.html",{
        "form": form,
        },context_instance=RequestContext(request),
        )

def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    if username and password:
        user = authenticate(username=request.POST['username'],
            password=request.POST['password']
            )

        if user is not None:
            login(request, user)
            print request.user
            return HttpResponseRedirect("/list/")
    else:
        return HttpResponseRedirect("/store/")

def logout_view(request):
    logout(request)
    return store_view(request)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/store/")
    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html",{
        'form': form,
        },context_instance=RequestContext(request),
        )