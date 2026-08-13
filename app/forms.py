"""
app/forms.py — WTForms Architecture.

Field names match exactly what the frozen page templates render via the form
macros (name='name', 'company', ...). The CSRF token and the <form> element are
emitted by the page templates; the honeypot ('website') is a template macro and
is validated in the route, not here.

SelectField.choices are used ONLY for server-side validation (the templates
render <option>s themselves). Optional selects allow an empty value.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional, AnyOf


CONSENT_MESSAGE = "Please confirm you agree to be contacted."


class _BaseContact(FlaskForm):
    name = StringField(validators=[DataRequired(), Length(max=200)])
    company = StringField(validators=[Optional(), Length(max=200)])
    email = StringField(validators=[DataRequired(), Email(), Length(max=320)])
    phone = StringField(validators=[Optional(), Length(max=64)])
    country = StringField(validators=[Optional(), Length(max=120)])
    message = TextAreaField(validators=[Optional(), Length(max=5000)])
    consent = BooleanField(validators=[DataRequired(message=CONSENT_MESSAGE)])


class ContactForm(_BaseContact):
    country = StringField(validators=[Optional(), Length(max=120)])
    enquiry_type = SelectField(
        choices=[("general", "General inquiry"), ("consultation", "Consultation request"),
                 ("documents", "Documents / compliance"), ("other", "Other")],
        validators=[DataRequired()],
    )
    message = TextAreaField(validators=[DataRequired(), Length(max=5000)])


class ExportInquiryForm(_BaseContact):
    company = StringField(validators=[DataRequired(), Length(max=200)])
    country = StringField(validators=[DataRequired(), Length(max=120)])
    # product choices are set per-request from the product registry (see routes).
    product = SelectField(choices=[], validators=[DataRequired()], validate_choice=False)
    quantity = StringField(validators=[Optional(), Length(max=120)])
    message = TextAreaField(validators=[DataRequired(), Length(max=5000)])
    consultation = BooleanField(validators=[Optional()])


class PartnershipForm(_BaseContact):
    company = StringField(validators=[DataRequired(), Length(max=200)])
    country = StringField(validators=[DataRequired(), Length(max=120)])
    product_lines = StringField(validators=[DataRequired(), Length(max=300)])
    volume = StringField(validators=[Optional(), Length(max=120)])
    frequency = SelectField(
        choices=[("", ""), ("one-time", "One-time"), ("occasional", "Occasional"),
                 ("regular", "Regular / ongoing")],
        validators=[Optional()],
    )
    target_market = StringField(validators=[Optional(), Length(max=200)])
