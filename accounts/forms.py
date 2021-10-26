from django import forms
from .models import *

class ProductForm(forms.ModelForm):

	class Meta:
		model = Product
		fields = ['image','name','category','price','description','quantity','is_published','created_at']