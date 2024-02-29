#myapp/forms.py
from django import forms

class ReclasificadorForm(forms.Form):
    #campo de los elementos de la izquierda para poder seleccionar varios
    elementos_izquierda= forms.MultipleChoiceField(widget=forms.SelectMultiple, required=False)

    #campo de los elementos de la izquierda para poder seleccionar varios 
    elementos_derecha = forms.MultipleChoiceField(widget=forms.SelectMultiple, required=False)