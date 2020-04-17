import csv
import glob
import pickle

from datetime import datetime
from datetime import timedelta

files = glob.glob('data/*')
allowed_airports = ['LAX', 'JFK', 'SFO', 'PHX', 'SEA', 'DEN', 'ATL', 'ORD', 'BOS', 'IAD']
itinerary = []

for file in files:
    origin_airport = file.split('/')[-1][:3]
    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Destination Airport'] in allowed_airports:
                itinerary.append( {**row, **{'Origin Airport': origin_airport}})

aa_flights = [flight for flight in itinerary if flight['Carrier Code'] == 'AA']
dl_flights = [flight for flight in itinerary if flight['Carrier Code'] == 'DL']
ua_flights = [flight for flight in itinerary if flight['Carrier Code'] == 'UA']

aa_capacity = {'737-800': 160, '737-823': 160, 'A321-231': 181, 'A320-232': 150, 'A319-132': 128, 'A321-211': 181, 'A319-115': 128, 'A320-214': 150, 'A319-112': 128}
dl_capacity = {'757-231': 168, '737-900ER': 180, '757-26D': 168, 'BD-500-1A10': 109, '757-2Q8': 168, '777-232LR': 288, '757-232': 168, 'MD-88': 149, '737-932ER': 180,
               '767-332': 208, '737-832': 160, 'A320-211': 157, '737-732': 124, '757-351': 234, '757-251': 168, 'A319-114': 132, 'A320-212': 157, 'MD-90-30': 158,
               'A321-211': 191, '717-200': 110}
ua_capacity = {'757-222': 169, '757-224': 169, 'A319-131': 126, 'A320-232': 150, '737-900ER': 179, '777-222': 364, '787-8': 219, '737-800': 166, 'A319-132': 126,
               '737-824': 166, '737-724': 126, '737-924ER': 179, '757-324': 234, '757-33N': 234}

with open('plane_lookup', 'rb') as f:
    plane_lookup = pickle.load(f)

[flight.update({'capacity': aa_capacity[plane_lookup[flight['Tail Number']]['Model']]}) for flight in aa_flights]
[flight.update({'capacity': dl_capacity[plane_lookup[flight['Tail Number']]['Model']]}) for flight in dl_flights]
[flight.update({'capacity': ua_capacity[plane_lookup[flight['Tail Number']]['Model']]}) for flight in ua_flights]

with open('time_shift', 'rb') as f:
    time_shift = pickle.load(f)

for flight in itinerary:
    takeoff_time = datetime.strptime(flight['Date (MM/DD/YYYY)']+'|'+flight['Scheduled departure time'], '%m/%d/%Y|%H:%M')
    air_time = int(flight['Actual elapsed time (Minutes)'])
    time_zone_difference = time_shift[flight['Origin Airport']][flight['Destination Airport']] * 60
    arrival_time = takeoff_time + timedelta(minutes=air_time+time_zone_difference)
    flight['Arrival Time'] = arrival_time.strftime('%H:%M')

itinerary = [flight for flight in itinerary if (datetime.strptime(flight['Date (MM/DD/YYYY)']+'|'+flight['Scheduled departure time'], '%m/%d/%Y|%H:%M') \
+ timedelta(minutes=int(flight['Actual elapsed time (Minutes)'])+time_shift[flight['Origin Airport']][flight['Destination Airport']]*60)).day == \
datetime.strptime(flight['Date (MM/DD/YYYY)']+'|'+flight['Scheduled departure time'], '%m/%d/%Y|%H:%M').day]

with open('processed_data/itinerary.csv', 'w') as f:
    fieldnames = itinerary[0].keys()
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for flight in itinerary:
        writer.writerow(flight)
