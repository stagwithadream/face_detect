from django import forms

class detect_image_form(forms.Form):
        img=forms.FileField(required=True)
