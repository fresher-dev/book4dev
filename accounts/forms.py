from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    """
    User Profile Form
    fields:
        -> bio
        -> picture
    """

    class Meta:
        model = Profile
        fields = ["bio", "picture"]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

        self.fields["picture"].widget.attrs["accept"] = "image/*"
