from django import forms

    class detect_image(forms.Form):
        img=forms.ImageField(required=True)

        def clean_img(self):
            data=sef.cleaned_data['img']

            return data
