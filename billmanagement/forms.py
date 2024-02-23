from django import forms
from django.forms import ModelForm
from billmanagement.models import *




class InvoiceItemForm(ModelForm):
    class Meta:
        model = InvoiceItem
        # fields = ['uploaded_images', 'invoice', 'name', 'description', 'cost', 'qty', 'date', ]
        fields = '__all__'

class FileUploadForm(ModelForm):
    class Meta:
        main_img = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
        model = FileUpload
        fields = ['main_img']
