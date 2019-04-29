# 1. Import Flask
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import create_engine, inspect
from datetime import datetime as dt
import datetime

# 2. Create an app
#################################################
# Database Setup
#################################################
dbPath = r"C:\Users\kapali_s\Documents\SMU\Homeworks\Assignment_10\hawaii.sqlite"
engine = create_engine("sqlite:///" + dbPath)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# 3. Define static routes
@app.route("/")
def index():
    #List all routes
    return (
        f"Welcome to the Climate App!<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"//api/v1.0/start/end<br/>")


@app.route("/api/v1.0/precipitation/")
#retun json representatin of all prcp after 2010-01-01
def precipitation():
    session = Session(engine)
    date_prcp = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > "2010-01-01").\
    order_by(Measurement.date).all()
    prcp_dict = dict(date_prcp)
    print("Precipitation")
    return jsonify(prcp_dict)   


@app.route("/api/v1.0/stations")
#return json list of stations
def stations():
    session = Session(engine)
    station_names = session.query(Station.station).all()
    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tobs(): 
#     #query dates and temp from last data point 2017-08-23   
#     #first date
      session = Session(engine)
#     last 12 months of tobs data
#     retrieve tobs scores
      date_tobs = session.query(Measurement.date, Measurement.tobs).\
      filter(Measurement.date.between('2016-8-23','2017-8-23')).all()
      return jsonify(date_tobs)
 
@app.route("/api/v1.0/start")
def tmin_tmax_tavg():

#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
        session = Session(engine)
        start_date_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= datetime.datetime(2017,8,16)).all()

        start_temp_list = {'min':start_date_temp[0][0],
                           'avg': start_date_temp[0][1],
                           'max':start_date_temp[0][2] }

        return jsonify(start_temp_list)

@app.route("/api/v1.0/start/end")
def tmin_tmax_tavg1():


# calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
        session = Session(engine)
        between_date_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date.between('2016-8-23','2017-8-23')).all()   
        
        between_list = {'min':between_date_temp[0][0],
                        'avg': between_date_temp[0][1],
                        'max':between_date_temp[0][2] }

        return jsonify(between_list)

if __name__ == "__main__":
     app.run(debug=True)
