#!/usr/bin/python3
import time
import sys
import datetime
from influxdb import InfluxDBClient



def report(iso, kind):
  f=open("/home/pi/pygrafanadht/src/motion.log", "a+")
  # print(f"time: {actualtime}")
  f.write(f"Motion insert {kind} at: {iso} \n")
  # f.write("hello")
  f.close()


def main():
  # Configure InfluxDB connection variables
  host = "192.168.1.226"  # My Ubuntu NUC
  port = 8086  # default port
  user = "rpi-3"  # the user/password created for the pi, with write access
  password = "rpi-3"
  dbname = "motion_data"  # the database we created earlier

  # Create the InfluxDB client object
  client = InfluxDBClient(host, port, user, password, dbname)


  # think of measurement as a SQL table, it's not...but...
  measurement = "rpi-motion"
  # location will be used as a grouping tag later
  location = "babymonitor"

  try:
    iso = time.time_ns()
    # Print for debugging, uncomment the below line
    print(f"motion detected at {iso}")
    # Create the JSON data structure
    data=[
      {
          "measurement": measurement,
          "tags": {
              "location": location,
          },
          "time": iso,
          "fields": {
              "motion": 1,
          }
      }
    ]
    # Send the JSON data to InfluxDB
    client.write_points(data)
    report(iso,"succeed")
  except:
    report(iso,"failed")
  
if __name__== "__main__":
  main()