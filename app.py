#import modules
import pandas as pd 
import numpy as np 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#import flask to create our app and make a api
import flask 
from flask import Flask, jsonify

#Label the engine to be used for the data
engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect = True)

Measurement = Base.classes.measurement
Station = Base.classes.station
Session = Session(engine)

app= Flask(__name__)
#Create our routes welcome page and display our routes 
@app.route("/")
def welcome():
    return (f"Welcome newcomers <br/>"
            f"routes <br/>"
            f"/api/v1.0/preciptation <br/>"
            f"/api/v1.0/stations <br/>"
            f"/api/v1.0/tobs <br/>"
            f"/api/v1.0/<start>/<end>")



@app.route("/api/v1.0/preciptation")
#return the preciptation over the past year 
def precipitation():
    m_prcp = Session.query(Measurement.prcp, Measurement.date).\
    filter(Measurement.date > '2016-08-23').\
    order_by(Measurement.date).all()
    prdict = {date: x for date, x in m_prcp}
    return jsonify(prdict)

@app.route("/api/v1.0/stations")
#return our station data to our page
def station():
    result = Session.query(Station.station).all()
    st_list = list(np.ravel(result))
    return jsonify(st_list)

#attain our Tobs for our most active staion
@app.route("/api/v1.0/tobs")
    
def tobs():
    Tempobs = Session.query(Measurement.tobs).\
            filter(Measurement.station == 'USC00519281' ).\
            filter(Measurement.date >= '2017,8,23').all()
    tobs_list = list(np.ravel(Tempobs))
    return jsonify (tobs_list)

#end our route 
@app.route("/api/v1.0/<start>/<end>")

def temps(start,end):
    findings = Session.query(Measurement).filter(Measurement.date>= start).filter(Measurement.date<=end)
    found = []
    for row in findings:
        found.append(row.tobs)
    return(jsonify({"Min temp": min(found), "Max temp": max(found), "Avg temp": np.mean}))

if __name__ == "__Main__":
    app.run(debug=True)