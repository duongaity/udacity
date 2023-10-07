# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import dateutil.parser
import babel
import json
from datetime import datetime
from flask import (Flask, render_template, request,
                   flash, redirect, url_for)
from flask_moment import Moment
from flask_migrate import Migrate
from forms import VenueForm, ArtistForm, ShowForm
from config import Config
from models import (db, Venue, Artist, Show)
# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)


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


@app.route('/venues')
def venues():
    areas = []
    data = Venue.query.order_by('city', 'state', 'name').all()
    for venue in data:
        area_item = {}
        pos_area = -1
        if len(areas) == 0 and len(data) > 1:
            pos_area = 0
            area_item = {
                "city": venue.city,
                "state": venue.state,
                "venues": []
            }
            areas.append(area_item)
        else:
            for i, area in enumerate(areas):
                if area['city'] == venue.city and area['state'] == venue.state:
                    pos_area = i
                    break
            if pos_area < 0:
                area_item = {
                    "city": venue.city,
                    "state": venue.state,
                    "venues": []
                }
                areas.append(area_item)
                pos_area = len(areas) - 1
            else:
                area_item = areas[pos_area]
        v = {
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": 4
        }
        area_item['venues'].append(v)
        areas[pos_area] = area_item
    return render_template('pages/venues.html', areas=areas)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    name_venues = request.form.get('search_term')
    response = Venue.query.filter(Venue.name.ilike('%' + name_venues + '%'))
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    data = Venue.query.filter_by(id=venue_id).first()
    print(data.genres)

    upcoming_shows = []
    past_shows = []
    for show in data.shows:
        if show.start_time > datetime.now():
            upcoming_shows.append(show)
        else:
            past_shows.append(show)
    data.upcoming_shows = upcoming_shows
    data.past_shows = past_shows
    return render_template('pages/show_venue.html', venue=data)


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm()
    venue = Venue(name=form.name.data, city=form.city.data,
                  state=form.state.data, phone=form.phone.data,
                  address=form.address.data,
                  genres=form.genres.data, facebook_link=form.facebook_link.data,
                  image_link=form.image_link.data, website=form.website.data)
    # Clear The Form
    form.name.data = ''
    form.city.data = ''
    form.state.data = ''
    form.address.data = ''
    form.phone.data = ''
    form.image_link.data = ''
    form.facebook_link.data = ''
    # Add post data to database
    db.session.add(venue)
    db.session.commit()

    return redirect(url_for('venues'))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    data = Venue.query.filter_by(id=venue_id).first()
    form = VenueForm()
    return render_template('forms/edit_venue.html', form=form, venue=data)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    venue = Venue.query.get(venue_id)

    venue.name = request.form.get('name')
    venue.phone = request.form.get('phone')
    venue.facebook_link = request.form.get('facebook_link')
    venue.image_link = request.form.get('image_link')
    venue.city = request.form.get('city')
    venue.state = request.form.get('state')
    venue.address = request.form.get('address')

    db.session.add(venue)
    db.session.commit()
    return redirect(url_for('show_venue', venue_id=venue_id))


@app.route('/venues/<int:venue_id>/delete', methods=['GET'])
def delete_venue(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm()
    return render_template('forms/delete_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/delete', methods=['POST'])
def delete_venue_submission(venue_id):
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/artists')
def artists():
    return render_template('pages/artists.html', artists=Artist.query.all())


@app.route('/artists/search', methods=['POST'])
def search_artists():
    name_artist = request.form.get('search_artist')
    response = Artist.query.filter(name=name_artist)
    return render_template('pages/search_artist.html', results=response, search_artist=request.form.get('search_artist', ''))


@app.route('/artists/<int:artists_id>')
def show_artists(artists_id):
    response = Artist.query.get(artists_id)
    return render_template('pages/show_artist.html', artist=response)


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm()
    artist = Artist(name=form.name.data, city=form.city.data, state=form.state.data,
                    genres=form.genres.data, phone=form.phone.data, image_link=form.image_link.data,
                    facebook_link=form.facebook_link.data, website=form.website.data)
    # Clear The Form
    form.name.data = ''
    form.city.data = ''
    form.state.data = ''
    form.genres.data = ''
    form.phone.data = ''
    form.image_link.data = ''
    form.facebook_link.data = ''
    form.website.data = ''
    # Add post data to database
    db.session.add(artist)
    db.session.commit()

    # Return a Message
    flash("Create Venue Submitted Successfully!")
    return redirect(url_for('artists'))


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    artist = Artist.query.get(artist_id)

    artist.name = request.form.get('name')
    artist.phone = request.form.get('phone')
    artist.facebook_link = request.form.get('facebook_link')
    artist.image_link = request.form.get('image_link')
    artist.city = request.form.get('city')
    artist.state = request.form.get('state')
    artist.address = request.form.get('address')

    db.session.add(artist)
    db.session.commit()
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/artists/<int:artist_id>/delete', methods=['GET'])
def delete_artist(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm()
    return render_template('forms/delete_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/delete', methods=['POST'])
def delete_artist_submission(artist_id):
    Artist.query.filter_by(id=artist_id).delete()
    db.session.commit()
    return redirect(url_for('index'))

#  Shows
#  ----------------------------------------------------------------


@app.route('/shows')
def shows():
    return render_template('pages/shows.html', shows=Show.query.all())


@app.route('/shows/create', methods=['GET'])
def create_show_form():
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    form = ShowForm()
    show = Show(venue_id=form.venue_id.data,
                artist_id=form.artist_id.data, start_time=form.start_time.data)
    # Clear The Form
    form.venue_id.data = ''
    form.artist_id.data = ''
    form.start_time.data = ''
    # Add post data to database
    db.session.add(show)
    db.session.commit()

    # Return a Message
    flash("Create Venue Submitted Successfully!")
    return redirect(url_for('shows'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)
