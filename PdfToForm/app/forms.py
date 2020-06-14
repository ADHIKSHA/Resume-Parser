from django import forms  
class StudentForm(forms.Form):  
    file      = forms.FileField(label='') # for creating file input 