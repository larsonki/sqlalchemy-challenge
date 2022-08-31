import json
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)
year_ago = dt.date(2017, 8, 23) -  dt.timedelta(days=365)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def homepage():
    """List all available api routes."""
    return (
        f"Welcome to Honolulu, Hawaii Climate API!<br/>"
        f"<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f">>> Returns Precipitation in inches from 2016-08-23 \
            through 2017-08-23<br/>"
        f"-------------------<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f">>> Returns a list of all the stations on the island.<br/>"
        f"-------------------<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f">>> Returns the observed temperatures from the most active \
            station (USC00519281) <br/>from 2016-08-23 through 2017-08-23 <br/>"
        f"-------------------<br/>"
        f"<br/>"
        f"/api/v1.0/<start_date><br/>"
        f">>> Search by start and end dates (yyyy-mm-dd/yyyy-mm-dd) to determine \
            the minimum, <br/>average, and maximum temperatures for the \
            range. If end date not entered, range will go <br/>from start through \
            most recent date.<br/>"
        f"-------------------<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
# Convert the query results to a dictionary using date as the key and prcp as 
# the value.
    prcp = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_ago).all()
    session.close()
    prcp_results = dict(prcp)
# Return the JSON representation of your dictionary.
    return jsonify(prcp_results)

@app.route("/api/v1.0/stations")
def stations():
    station_results = session.query(Station.station).all()
    session.close()
    station = list(np.ravel(station_results))
# Return a JSON list of stations from the dataset.
    return jsonify(station=station)

@app.route("/api/v1.0/tobs")
def tobs():
# Query the dates and temperature observations of the most active station 
# for the previous year of data.
    most_active = session.query(Measurement.station,\
        func.count(Measurement.id)).group_by(Measurement.station).\
            order_by(func.count(Measurement.id).desc()).all()
    top_station = most_active[0][0]
    temp = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == top_station).\
            filter(Measurement.date >= year_ago).all()
    session.close()
    temp_obs = list(np.ravel(temp))
# Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(temp_obs=temp_obs)

# Return a JSON list of the minimum temperature, the average temperature, 
# and the maximum temperature for a given start or start-end range.
## Code adapted from Maria Carter (mcarter-00) @
## https://github.com/mcarter-00/Surfs-Up/blob/master/app.py
@app.route("/api/v1.0/<start_date>")
@app.route("/api/v1.0/<start_date>/<end_date>")
def stats(start_date=None, end_date=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs),\
        func.max(Measurement.tobs)]

# When given the start only, calculate TMIN, TAVG, and TMAX for all dates 
# greater than or equal to the start date.
    if not end_date:
        date_results = session.query(*sel).\
            filter(Measurement.date >= start_date).all()
        session.close()
        temp_stats = list(np.ravel(date_results))
        return jsonify(temp_stats)
    
# When given the start and the end date, calculate the TMIN, TAVG, and
# TMAX for dates from the start date through the end date (inclusive).
    date_results = session.query(*sel).\
        filter(Measurement.date >= start_date).\
            filter(Measurement.date <= end_date).all()
    session.close()
    temp_stats = list(np.ravel(date_results))
    return jsonify(temp_stats)

if __name__ == '__main__':
     app.run(debug=True)


