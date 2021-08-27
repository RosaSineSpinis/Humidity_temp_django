from django import forms
from .models import Document


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes',
    )


'''I think it is for many fiels'''
class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


'''I think it is for the whole directory'''
class DirectoryFieldForm(forms.Form):
    directory = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'multiple': True, 'webkitdirectory': True, 'directory': True, 'class': 'form-control'}))

# '''changed css class in form'''
# class DocumentForm(forms.ModelForm):
#     class Meta:
#         model = Document
#         fields = ('docfile')
#         widget = {
#             'docfile': forms.FileField(attrs={'class': 'form_control'})
#         }