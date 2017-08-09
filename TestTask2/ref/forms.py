from django import forms


class AddSystemUserForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'required': True, 'maxlength': 30}),
                                 max_length=30)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'required': True, 'maxlength': 30}),
                                max_length=30)
    link = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}),
                                    required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'required': True}))



class ReferalNumberForm(forms.Form):
    referal_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}),
                                    required=True)


class EmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'required': True}))