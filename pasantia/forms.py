from django import forms
from .models import PostPasantias, Entidad

class PasantiaPostForm(forms.ModelForm):
    body = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': '52/2022'
            }),
        required=True)
    fecha_limite = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}),required=True)
    created_on = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}),required=True)
    file = forms.FileField(widget=forms.FileInput(attrs={'accept':'.pdf'}),
        required=True
        )
    
    
    class Meta:
        model = PostPasantias
        fields = ['body', 'fecha_limite', 'created_on', 'file']
        

class EntidadRegisterForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(), required=True)
    image = forms.ImageField(label='Profile Picture', required=True, widget=forms.FileInput)
    
    class Meta:
        model = Entidad
        fields = ['name', 'image']