from django import forms
from main_app.models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    name = forms.CharField(label='Name', widget=forms.TextInput);
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('name', 'username', 'email', 'password1', 'password2',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2
       
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['name'];
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    
