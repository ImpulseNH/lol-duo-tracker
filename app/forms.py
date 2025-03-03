from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired, ValidationError
import re

def validate_summoner_format(form, field):
    # Check if the summoner name is in the correct format
    if not re.match(r'^[^#]+#[^#]+$', field.data):
        raise ValidationError('Invalid format. Use Gamename#TAG format.')
    
    # Split the summoner name into parts
    parts = field.data.split('#')
    if len(parts) == 2 and len(parts[1]) < 3:
        raise ValidationError('TAG must contain at least 3 characters.')

class MyForm(FlaskForm):
    option = SelectField('Select region', choices=[
        ('AMERICAS', 'AMERICAS (NA, LAN, LAS, BR)'),
        ('ASIA', 'ASIA (KR, JP)'),
        ('EUROPE', 'EUROPE (EUW, EUNE, TR, RU)'),
        ('SEA', 'SEA (OCE, PH, SG, TH, TW, VN)'),
    ], validators=[DataRequired()])

    summoner1 = StringField(label="Summoner 1", validators=[DataRequired(), validate_summoner_format])
    summoner2 = StringField(label="Summoner 2", validators=[DataRequired(), validate_summoner_format])
    summoner1_puuid = HiddenField('Summoner 1 PUUID')
    summoner2_puuid = HiddenField('Summoner 2 PUUID')
    submit = SubmitField('Search')