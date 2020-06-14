from django import forms  
class StudentForm(forms.Form):  
    file      = forms.FileField() # for creating file input 