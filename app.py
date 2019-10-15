#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from models import create_app, Artist, Venue, Show
from sqlalchemy.exc import SQLAlchemyError
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
db = create_app(app)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#



#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

  city_and_state = ''
  data = []

  venue_query = Venue.query.group_by(Venue.id, Venue.city, Venue.state).all()

  for venue in venue_query:
    upcoming_shows = venue.shows.filter(Show.start_time > current_time).all()

    if city_and_state == venue.city + venue.state:
      data[len(data) - 1]["venues"].append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": len(upcoming_shows)
      })
      
    else:
      city_and_state = venue.city + venue.state
      data.append({
        "city": venue.city,
        "state": venue.state,
        "venues": [{
          "id": venue.id,
          "name": venue.name,
          "num_upcoming_shows": len(upcoming_shows)
        }]
      })
  
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    venue_query = Venue.query.filter(Venue.name.ilike('%' + request.form['search_term'] + '%'))
    for result in venue_query:
      # print(result.name)
      # print(result.id)
    
      venue_array = list(map(Venue.short, venue_query))
    
    
    response = {
      "count": len(venue_array),
      "data": venue_array
    }
    return render_template (
        'pages/search_venues.html',
        results=response,
        search_term=request.form.get('search_term', '')
    )

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    venue_query = Venue.query.get(venue_id)
      
    if venue_query:
      venue_details = Venue.details(venue_query)
      current_time = datetime.now().strftime('%Y-%m-%d')
      new_shows_query = Show.query.options(db.joinedload('Artist')).filter(Show.venue_id == venue_id).filter(Show.start_time > current_time).all()
      new_show = list(map(Show.details_artist, new_shows_query))
      venue_details["upcoming_shows"] = new_show
      venue_details["upcoming_shows_count"] = len(new_show)
      past_shows_query = Show.query.options(db.joinedload('Artist')).filter(Show.venue_id == venue_id).filter(Show.start_time <= current_time).all()
      past_shows = list(map(Show.details_artist, past_shows_query))
      venue_details["past_shows"] = past_shows
      venue_details["past_shows_count"] = len(past_shows)
      

    # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
      return render_template('pages/show_venue.html', venue=venue_details)
    else:
      return render_template('errors/404.html')
  

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashin

  data = request.form
  try:
    new_venue = Venue(
    genres=data.getlist("genres"),
    name=data.get("name"),
    address=data.get("address"),
    city=data.get("city"),
    state=data.get("state"),
    facebook_link=data.get("facebook_link"),
    phone=data.get("phone"),
    website=data.get("website_link"),
    image_link=data.get("image_link")
  )
    Venue.insert(new_venue)
    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  except SQLAlchemyError as e:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  venue_query = Venue.query.get(venue_id)
  
  if venue_query:
    Venue.delete(venue_query)
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  artist_query = Artist.query.all()
  artist_map = list(map(Artist.short, artist_query))

  return render_template('pages/artists.html', artists=artist_map)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  artist_query = Artist.query.filter(Artist.name.ilike('%' + request.form['search_term'] + '%'))

  artist_mapper = list(map(Artist.short, artist_query))




  response={
    "count": len(artist_mapper),
    "data": artist_mapper
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  artist_query = Artist.query.get(artist_id)
  if artist_query:
        artist_details = Artist.details(artist_query)
        current_time = datetime.now().strftime('%Y-%m-%d')
        upcoming_shows_query = Show.query.options(db.joinedload('Artist')).filter(Show.artist_id == artist_id).filter(Show.start_time >= current_time).all()
        for query in upcoming_shows_query:
          print(query.id)
          print(query.artist_id)
          print(query.venue_id)
          print(query.start_time)


        upcoming_shows_list = list(map(Show.details_venue, upcoming_shows_query))
        artist_details["upcoming_shows"] = upcoming_shows_list
        artist_details["upcoming_shows_count"] = len(upcoming_shows_list)
        past_shows_query = Show.query.options(db.joinedload('Artist')).filter(Show.artist_id == artist_id).filter(Show.start_time <= current_time).all()
        past_shows_list = list(map(Show.details_venue, past_shows_query))
        artist_details["past_shows"] = past_shows_list
        artist_details["past_shows_count"] = len(past_shows_list)
        return render_template('pages/show_artist.html', artist=artist_details)
  return render_template('errors/404.html')
  

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
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
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  form = ArtistForm()
  data = request.form
  try:
    seeking_venue = None
    if 'seeking_venue' in request.form:
      seeking_venue = request.form['seeking_venue'] == 'y'

    new_artist = Artist(
        name=data.get("name"),
        genres=data.getlist("genres"),
        city=data.get("city"),
        state=data.get("state"),
        phone=data.get("phone"),
        website=data.get("website_link"),
        seeking_venue= seeking_venue,
        facebook_link=data.get("facebook_link"),
        seeking_description=data.get("seeking_description"),
        image_link=data.get("image_link")
    )
    Artist.insert(new_artist)
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except SQLAlchemyError as e:
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  shows_query = Show.query.all()
  shows_mapper = list(map(Show.details, shows_query))
  data = shows_mapper

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm()
  data = request.form

  try:
    new_show = Show(
      venue_id=data.get('venue_id'),
      artist_id=data.get('artist_id'),
      start_time=data.get('start_time')
    )
    Show.insert(new_show)
    flash('Show was successfuly listed!')
  except SQLAlchemyError as e:
    flash('An error occured. Show could not be listed.')

  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
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

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
