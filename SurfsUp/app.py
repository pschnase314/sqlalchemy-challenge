#import dependencies
from flask import Flask, jsonify
import pandas as pd
import datetime as dt
from statistics import mean

#import data
measurements_df=pd.read_csv("Resources/hawaii_measurements.csv")
stations_df=pd.read_csv("Resources/hawaii_stations.csv")

#define app
app = Flask(__name__)

#make homepage showing what the options are for retrieving data
@app.route("/")
def home():
    return("/api/v1.0/precipitation <br>\
    /api/v1.0/stations<br>\
    /api/v1.0/tobs<br>\
    /api/v1.0/start<br>\
    /api/v1.0/start/end")

#return all the precipitation data
#note that I was getting errors when I ran this in firefox, but not in chrome I did not have time to figure out why
@app.route("/api/v1.0/precipitation")
def precipitation():
    prcps=[]
    for line in measurements_df.iterrows():
        prcps.append({line[1]["date"]: line[1]["prcp"]})

    return(jsonify(prcps))

#return all information for all stations
@app.route("/api/v1.0/stations")
def stations():
    stns = []
    for line in stations_df.iterrows():
        stns.append([line[1]["station"],line[1]["name"],line[1]["latitude"],line[1]["longitude"],line[1]["elevation"]])
    return(jsonify(stns))

#return temperature data for final year at most active station
@app.route("/api/v1.0/tobs")
def tobs():
    temps=[]
    for line in measurements_df.iterrows():
        if (line[1]["station"]=="USC00519281") and (dt.date.fromisoformat(line[1]["date"]) > dt.date.fromisoformat("2016-08-23")):
            temps.append({line[1]["date"]: line[1]["tobs"]})

    return(jsonify(temps))

#return lowest, average, and highest temperatures from most active station starting on given date
#date format:  yyyy-mm-dd
@app.route("/api/v1.0/<start>")
def tobs2(start):
    temps=[]
    for line in measurements_df.iterrows():
        if (line[1]["station"]=="USC00519281") and (dt.date.fromisoformat(line[1]["date"]) >= dt.date.fromisoformat(start)):
            temps.append(line[1]["tobs"])
    low = min(temps)
    high = max(temps)
    avg = mean(temps)
    return({"TMIN":low, "TAVG": avg, "TMAX": high})

#return lowest, average, and highest temperatures from most active station starting on given date and ending before given date
#date format:  yyyy-mm-dd
@app.route("/api/v1.0/<start>/<end>")
def tobs3(start,end):
    temps=[]
    for line in measurements_df.iterrows():
        if (line[1]["station"]=="USC00519281") and (dt.date.fromisoformat(line[1]["date"]) >= dt.date.fromisoformat(start)) and (dt.date.fromisoformat(line[1]["date"]) < dt.date.fromisoformat(end)):
            temps.append(line[1]["tobs"])
    low = min(temps)
    high = max(temps)
    avg = mean(temps)
    return({"TMIN":low, "TAVG": avg, "TMAX": high})

#run the app
if __name__ == "__main__":
    app.run(debug=False)
