from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField, DecimalRangeField, SelectField, SelectMultipleField, widgets)

from wtforms.validators import InputRequired, Length
import sys
import config.VARS as VARS




import re
import pandas as pd

r = re.compile("ageRange.*")
ages = list(filter(r.match, VARS.USER_CHARS.columns))




last_age_index = [i for i, v in enumerate(VARS.USER_CHARS.columns) if re.match('ageRange_65\+', v)]

styles = sorted(VARS.USER_CHARS.columns[(last_age_index[0]+1):])

cities = sorted(VARS.CITY_REVIEWS.columns)




class BigFiveForm(FlaskForm):
    
    open = DecimalRangeField(label = "Openness to experience")
    cons = DecimalRangeField(label = "Conscientiousness")
    extra = DecimalRangeField(label = "Extraversion")
    agree = DecimalRangeField(label = "Agreeableness")
    neuro = DecimalRangeField(label = "Neuroticisim")
    age = SelectField(label = "Age Group", choices = ages)


class TravelStyles(FlaskForm):
    
    style = SelectMultipleField(label = "", choices = styles, validators=[InputRequired()])


class MultiCheckboxField(SelectMultipleField):
     widget = widgets.ListWidget(prefix_label=False)
     option_widget = widgets.CheckboxInput()


class CityRater(FlaskForm):
    
    goodcity = SelectMultipleField(label = "", choices = cities, validators=[InputRequired()])
    badcity = SelectMultipleField(label = "", choices = cities)
