from django import forms  
class StudentForm(forms.Form):  
    file      = forms.FileField(attrs={'class' : 'files'}) # for creating file input 