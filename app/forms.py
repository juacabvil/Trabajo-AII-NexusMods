#encoding:utf-8
from django import forms
   
class ModBusquedaForm(forms.Form):
    mod = forms.CharField(label="busqueda", widget=forms.TextInput, required=True)

class ColBusquedaForm(forms.Form):
    col = forms.CharField(label="busqueda", widget=forms.TextInput, required=True)
