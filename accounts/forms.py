from cProfile import Profile
from accounts.models import Profile
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class EditProfileForm(forms.ModelForm):
    celular = forms.CharField(widget=forms.TextInput(attrs={'maxlength':'8'}))
    
    class Meta:
        model = Profile
        fields = ('celular',)
        
class DocumentUploadForm(forms.ModelForm):
    ci_doc = forms.FileField(required=False, widget=forms.FileInput(attrs={'accept':'.pdf'}))
    hoja_vida_doc = forms.FileField(required=False, widget=forms.FileInput(attrs={'accept':'.pdf'}))
    record_doc = forms.FileField(required=False, widget=forms.FileInput(attrs={'accept':'.pdf'}))
    bol_insc_doc = forms.FileField(required=False, widget=forms.FileInput(attrs={'accept':'.pdf'}))
    conc_est_doc = forms.FileField(required=False, widget=forms.FileInput(attrs={'accept':'.pdf'}))
    
    class Meta:
        model = Profile
        fields = ('ci_doc', 'hoja_vida_doc', 'record_doc', 'bol_insc_doc', 'conc_est_doc',)