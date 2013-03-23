# coding: utf-8
# Author: kaidee

from django import forms
from models import *
import itertools

def anyTrue(predicate, sequence):
    return True in itertools.imap(predicate, sequence)
def endsWith(s, *endings):
    return anyTrue(s.endswith, endings)

class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product    

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

    def clean_price(self):
        price = self.cleaned_data['price']
        if price<=0:
            raise forms.ValidationError("价格必须大于零")
        return price

# class PictureForm(forms.Form):
#     imagefile = forms.ImageField() 

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

class ImagesForm(forms.ModelForm):
    """docstring for ImagesForm"""
    class Meta:
        model = Images
    def __init__(self, arg):
        super(ImagesForm, self).__init__()
