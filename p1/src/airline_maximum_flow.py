'''
File name :   airline_maximum_flow.py
Author :      Kevin Shannon
Date :        04/18/2020
Description : Builds problem specific topology of graph and solves the maximum
              flow through it.
'''

import csv
import sys

from datetime import datetime
from datetime import timedelta
from ford_fulkerson import solve
from graph import Edge, Vertex
from graph import FlightEdge, FlightVertex

sys.path.insert(1, '../')
from utils.graph_utils import bisect_left
from utils.graph_utils import parse_departure_time
from utils.graph_utils import parse_arrival_time


def build_graph(processed_data):
    '''
    Function to build the topology of an itinerary.

    Parameters
    ----------
    processed_data : str
        Location of itinerary file.

    Returns
    -------
    vertices : dict
        Dictionary containg vertices of the graph.
    '''
    airports = ['LAX', 'SFO', 'SEA', 'PHX', 'DEN', 'ORD', 'ATL', 'BOS', 'IAD']
    itinerary = []
    vertices = {}

    # Read in the flight itinerary data
    with open(processed_data) as f:
        reader = csv.DictReader(f)
        for row in reader:
            itinerary.append(dict(row))

    # Build vertices for each flight
    for airport in airports:
        flights = [flight for flight in itinerary if flight['Origin Airport'] == airport]
        flights.sort(key=lambda x: x['Scheduled departure time'])
        vertices[airport] = [FlightVertex(flight) for flight in flights]
    # Build Special S and T vertices
    vertices['S'] = Vertex(is_source_vertex=True)
    vertices['T'] = Vertex(is_sink_vertex=True)

    # Build initial edges for S
    for flight in vertices['LAX']:
        edge = FlightEdge(origin=vertices['S'], dest=flight, flow=0, capacity=int(flight.flight_info['capacity']))
        vertices['S'].edges.append(edge)
        flight.edges.append(edge)

    # Build edges for each flight
    for airport in airports:
        for flight in vertices[airport]:
            if flight.flight_info['Destination Airport'] != 'JFK':
                # Flights are sorted by departure time, do a binary search to find first flight that takes off from destination airport after current flight has arrived
                first_available_flight = bisect_left(vertices[flight.flight_info['Destination Airport']], parse_arrival_time(flight.flight_info), key=lambda x: parse_departure_time(x.flight_info))
                available_flights = vertices[flight.flight_info['Destination Airport']][first_available_flight:]

                # Add edges for all possible next flights passenger could catch
                for next_flight in available_flights:
                    edge = FlightEdge(origin=flight, dest=next_flight, flow=0, capacity=int(flight.flight_info['capacity']))
                    flight.edges.append(edge)
                    next_flight.edges.append(edge)
            else:
                # Build edges for T
                edge = FlightEdge(origin=flight, dest=vertices['T'], flow=0, capacity=int(flight.flight_info['capacity']))
                flight.edges.append(edge)
                vertices['T'].edges.append(edge)
    return vertices

V = build_graph('../process/processed_data/itinerary.csv')
solve(V)
print(f"Maximum Flow: {sum([edge.flow for edge in V['T'].edges])}")
