from django import forms


class BroadcastForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
