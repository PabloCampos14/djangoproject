#myapp/forms.py
from django import forms
#
class ProvForm(forms.Form):
    id_proveedor = forms.IntegerField()
    num_proveedor = forms.CharField(max_length=20)
    nombre_proveedor = forms.CharField(max_length=100)
    no_clabe = forms.CharField(max_length=20, required=False)
    descripcion = forms.CharField(max_length=255)

class EditarFechaForm(forms.Form):
    fecha_liquidacion = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control datepicker', 'placeholder': 'YYYY-MM-DD'})
    )