from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL, Regexp, Optional

states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY',
          'LA', 'ME', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'MD', 'MA', 'MI', 'MN',
          'MS', 'MO', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

genres_choices = ['Alternative', 'Blues', 'Classical', 'Country', 'Electronic', 'Folk', 'Funk', 'Hip-Hop',
                  'Heavy Metal', 'Instrumental', 'Jazz', 'Musical Theatre', 'Pop', 'Punk', 'R&B', 'Reggae',
                  'Rock n Roll', 'Soul', 'Other']


def make_choices(array):
    return [(x, x) for x in array]


class ShowForm(FlaskForm):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default=datetime.today()
    )


class VenueForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired(), AnyOf(states)],
        choices=make_choices(states)
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone', validators=[Regexp('\d{3}\-?\d{3}\-?\d{4}'), DataRequired()]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=make_choices(genres_choices)
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL(), Optional()]
    )
    website = StringField(
        'website', validators=[URL(), Optional()]
    )
    seeking_talent = BooleanField(
        'seeking_talent'
    )
    seeking_description = StringField(
        'seeking_description'
    )


class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired(), AnyOf(states)],
        choices=make_choices(states)
    )
    phone = StringField(
        'phone', validators=[Regexp('\d{3}\-?\d{3}\-?\d{4}'), DataRequired()]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=make_choices(genres_choices)
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL(), Optional()]
    )
    website = StringField(
        'website', validators=[URL(), Optional()]
    )
    seeking_venue = BooleanField(
        'seeking_venue'
    )
    seeking_description = StringField(
        'seeking_description'
    )
