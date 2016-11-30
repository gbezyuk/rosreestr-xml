from django import forms


class CadastralBlockFileUploadForm(forms.Form):
    file = forms.FileField()