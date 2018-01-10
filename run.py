#Tai-Hsien Ou Yang. Dec., 30, 2017.
from google.transit import gtfs_realtime_pb2
from datetime import datetime
import urllib.request
from time import time 
from time import sleep
import os

MAX_WAIT_MINUTE = 30 
STATION_NAME = "Columbia University"
STATION_ID_NORTH = "117N"
STATION_ID_SOUTH = "117S"
REFRESH_DURATION_SECOND = 60

API_URL_WITH_TOKEN = "http://datamine.mta.info/mta_esi.php?key=<MTA_KEY>"

feed = gtfs_realtime_pb2.FeedMessage()

while True:
  os.system('clear')
  with urllib.request.urlopen( API_URL_WITH_TOKEN ) as url:
    s = url.read()

  feed.ParseFromString(s)
  direction = "ERR"
  train_id = "ERR"

  current_time = int(time())
  
  print( "\n ===== NY Subway Arrivals =====\n" )
  print( "", STATION_NAME )
  
  for entity in feed.entity:
    if entity.HasField('trip_update'):
      train_id = entity.trip_update.trip.route_id
      for updateMessage in entity.trip_update.stop_time_update:
        stop_id = updateMessage.stop_id
        if ( stop_id == STATION_ID_NORTH ) or ( stop_id == STATION_ID_SOUTH ):
          time_arrival = updateMessage.arrival.time
          expected_duration = (time_arrival-current_time) // 60 % 60
          if( stop_id == STATION_ID_NORTH ):
            direction = " Northbound"
          if( stop_id == STATION_ID_SOUTH ):
            direction = " Southbound"
          if( expected_duration < MAX_WAIT_MINUTE ):
            print(direction, train_id, "train:", expected_duration, "minutes.")      
    if entity.HasField('alert'):
      print( "\n ======= Service Alert =======\n" )
      for alert in entity.alert.informed_entity:
        print( " DELAY: Train", alert.trip.route_id, ", trip:", alert.trip.trip_id )
  print( "\n Last updated:", datetime.fromtimestamp(current_time) )
  sleep( REFRESH_DURATION_SECOND )
