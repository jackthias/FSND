# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import sys

import dateutil.parser
import babel
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_migrate import Migrate
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from forms import *

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#
from starter_code.models import Venue, Artist, Show, db

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------
def format_venue_for_list(venue):
    data = venue.__dict__
    data['num_upcoming_shows'] = len(venue.shows)
    return data


@app.route('/venues')
def venues():
    return render_template('pages/venues.html', areas=[{
        "city": region.city,
        "state": region.state,
        "venues": [format_venue_for_list(venue) for venue in
                   Venue.query.filter_by(city=region.city, state=region.state).all()]
    } for region in Venue.query.distinct(Venue.city, Venue.state).all()])


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    results = Venue.query.filter(Venue.name.ilike('%{}%'.format(request.form.get('search_term', '')))).all()
    return render_template('pages/search_venues.html', results={"count": len(results), "data": results},
                           search_term=request.form.get('search_term', ''))


def format_show(show, venue=True):
    result = show.__dict__
    result["start_time"] = str(show.start_time)
    if venue:
        result["artist_image_link"] = show.artist.image_link
        result["artist_name"] = show.artist.name
    else:
        result["venue_image_link"] = show.venue.image_link
        result["venue_name"] = show.venue.name
    return result


def get_child_shows(element, venue=True):
    data = element.__dict__
    if venue:
        past_shows = Show.query.join(Venue).filter(Show.venue_id == element.id, Show.start_time <= db.func.now()).all()
        upcoming_shows = Show.query.join(Venue).filter(Show.venue_id == element.id,
                                                       Show.start_time >= db.func.now()).all()
    else:
        past_shows = Show.query.join(Artist).filter(Show.artist_id == element.id, Show.start_time <= db.func.now()).all()
        upcoming_shows = Show.query.join(Artist).filter(Show.artist_id == element.id, Show.start_time > db.func.now()).all()
    data['past_shows'] = [format_show(show, venue=venue) for show in past_shows]
    data['past_shows_count'] = len(past_shows)
    data['upcoming_shows'] = [format_show(show, venue=venue) for show in upcoming_shows]
    data['upcoming_shows_count'] = len(upcoming_shows)
    return data


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    venue = Venue.query.get(venue_id)
    data = get_child_shows(venue)
    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    error = False
    form = VenueForm()
    try:
        if form.validate_on_submit():
            venue = Venue(name=request.form.get('name', ''),
                          city=request.form.get('city', ''),
                          state=request.form.get('state', ''),
                          address=request.form.get('address', ''),
                          phone=request.form.get('phone', ''),
                          image_link=request.form.get('image_link'),
                          facebook_link=request.form.get('facebook_link', ''),
                          genres=request.form.getlist('genres'),
                          website=request.form.get('website', ''),
                          seeking_talent=request.form.get('seeking_talent', '') == 'y',
                          seeking_description=request.form.get('seeking_description', ''))
            db.session.add(venue)
            db.session.commit()
        else:
            flash('Validation for ' + request.form.get('name', '') + ' failed! ' + str(form.errors))
            return redirect(url_for('create_venue_form'))
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    if not error:
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
        return render_template('pages/home.html')
    else:
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
        return redirect(url_for('create_venue_form'))


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    return render_template('pages/artists.html', artists=Artist.query.all())


@app.route('/artists/search', methods=['POST'])
def search_artists():
    results = Artist.query.filter(Artist.name.ilike('%{}%'.format(request.form.get('search_term', '')))).all()
    return render_template('pages/search_artists.html', results={"count": len(results), "data": results},
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    artist = Artist.query.get(artist_id)
    data = get_child_shows(artist, venue=False)
    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    error = False
    form = ArtistForm()
    name = None
    try:
        if form.validate_on_submit():
            artist = Artist(name=request.form.get('name', ''),
                            city=request.form.get('city', ''),
                            state=request.form.get('state', ''),
                            phone=request.form.get('phone', ''),
                            genres=request.form.getlist('genres'),
                            image_link=request.form.get('image_link', ''),
                            facebook_link=request.form.get('facebook_link', ''),
                            website=request.form.get('website', ''),
                            seeking_venue=request.form.get('seeking_venue', '') == 'y',
                            seeking_description=request.form.get('seeking_description', ''))
            db.session.add(artist)
            db.session.commit()
            name = artist.name
        else:
            flash('Validation for ' + request.form.get('name', '') + ' failed! ' + str(form.errors))
            return redirect(url_for('create_artist_form'))
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    # on successful db insert, flash success
    if not error:
        flash('Artist ' + name + ' was successfully listed!')
    else:
        flash('An error occurred. Artist ' + request.form.get('name', '') + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    data = [{
        "venue_id": show.venue_id,
        "venue_name": show.venue.name,
        "artist_id": show.artist_id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": str(show.start_time)
    } for show in Show.query.all()]
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    error = False
    try:
        show = Show(
            start_time=request.form.get('start_time', ''),
            artist_id=request.form.get('artist_id', ''),
            venue_id=request.form.get('venue_id', '')
        )
        db.session.add(show)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.rollback()

    # on successful db insert, flash success
    if not error:
        flash('Show was successfully listed!')
    else:
        flash('An error occurred. Show could not be listed.')
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''