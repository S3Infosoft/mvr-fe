from django import forms


class ReportEmailForm(forms.Form):
    subject = forms.CharField(max_length=250)
    message = forms.CharField(widget=forms.Textarea())
    to = forms.EmailField()


class ReportForm(forms.Form):
    ENQUIRIES = (
        ("OTA", "OTA"),
        ("PARTNER", "Partner"),
        ("REVIEW", "Review"),
    )

    start_date = forms.DateTimeField(widget=forms.SelectDateWidget())
    end_date = forms.DateTimeField(widget=forms.SelectDateWidget())
    enquiry_type = forms.ChoiceField(choices=ENQUIRIES)
