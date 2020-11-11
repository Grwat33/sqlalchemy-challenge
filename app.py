import numpy as np
import pandas as pd 
import datetime as dt
from datetime import datetime
from datetime import timedelta
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

base = automap_base()
base.prepare(engine, reflect=True)

measurement = base.classes.measurement
station = base.classes.station
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    last = session.query(measurement.date).order_by(measurement.date.desc()).first()
    last = last[0]
    clean_date = datetime.strptime(last, '%Y-%m-%d')
    oneyearago = clean_date - dt.timedelta(days=366)
    pasttwelvemonths = session.query(measurement.prcp, measurement.date).\
        filter(measurement.date>=oneyearago, measurement.date<=clean_date).all()
    return jsonify(pasttwelvemonths)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    uniquestations = session.query(measurement.station).group_by(measurement.station).all()
    return jsonify(uniquestations)

@app.route("/api/v1.0/tobs")
def temperature():
        session = Session(engine)
        last = session.query(measurement.date).order_by(measurement.date.desc()).first()
        last = last[0]
        clean_date = datetime.strptime(last, '%Y-%m-%d')
        oneyearago = clean_date - dt.timedelta(days=366)
        stationtemp = session.query(station.station, station.name, func.count(measurement.tobs)).\
            filter(measurement.station == station.station).\
            group_by(measurement.station).\
            order_by(func.count(measurement.station).desc()).all()
        pasttwelvemonthstemp = session.query(measurement.tobs, measurement.date).\
            filter(measurement.station=='USC00519281',measurement.date>=oneyearago, measurement.date<=clean_date).all()
        return jsonify(pasttwelvemonthstemp)

@app.route("/api/v1.0/augustfirst/augustfourteenth")
def end():
    session = Session(engine)
    startdate = '2017-08-01'
    enddate = '2017-08-14'
    cleanstartdate = datetime.strptime(startdate, '%Y-%m-%d')
    cleanenddate = datetime.strptime(enddate, '%Y-%m-%d')
    betweenvacationtemp = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.date>=startdate, measurement.date<=enddate).all()
    return jsonify(betweenvacationtemp)

@app.route("/api/v1.0/augustfirst")
def start():
    session = Session(engine)
    startdate = '2017-08-01'
    cleanstartdate = datetime.strptime(startdate, '%Y-%m-%d')
    aftervacationtemp = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.date>=startdate).all()
    return jsonify(aftervacationtemp)

@app.route("/")
def Home_Page():
        return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/augustfirst<br/>"
        f"/api/v1.0/augustfirst/augustfourteenth<br/>"
    )

if __name__ == "__main__":
    app.run(debug=True)
