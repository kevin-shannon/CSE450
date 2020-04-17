import csv
import sys

from datetime import datetime
from datetime import timedelta

sys.path.insert(1, '../')
from utils.graph_utils import bisect_left
from utils.graph_utils import parse_departure_time
from utils.graph_utils import parse_arrival_time


class Vertex:
    def __init__(self, label=None, edges=None, is_source_vertex=False, is_sink_vertex=False):
        self.label = label
        self.edges = edges if edges is not None else []
        self.is_source_vertex = is_source_vertex
        self.is_sink_vertex = is_sink_vertex

    def __repr__(self):
        if self.is_source_vertex:
            return 'S'
        elif self.is_sink_vertex:
            return 'T'
        return str(id(self))


class FlightVertex(Vertex):
    def __init__(self, flight_info, label=None, edges=None, is_source_vertex=False, is_sink_vertex=False):
        super().__init__(label, edges, is_source_vertex, is_sink_vertex)
        self.flight_info = flight_info

    def __repr__(self):
        return f"{self.flight_info['Origin Airport']} -> {self.flight_info['Destination Airport']} ({self.flight_info['Scheduled departure time']} -> {self.flight_info['Arrival Time']}) {self.flight_info['capacity']} seats"


class Edge:
    def __init__(self, origin=None, dest=None, flow=0, capacity=0):
        self.origin = origin
        self.dest = dest
        self.flow = flow
        self.capacity = capacity
    def __repr__(self):
        return f"{self.origin} --{self.flow}/{self.capacity}--> {self.dest}"

class FlightEdge(Edge):
    def __repr__(self):
        if self.dest.is_sink_vertex:
            return f"{self.origin.flight_info['Origin Airport']}:{self.origin.flight_info['Destination Airport']} --{self.flow}/{self.capacity}--> {self.dest}"
        elif self.origin.is_source_vertex:
            return f"{self.origin} --{self.flow}/{self.capacity}--> {self.dest.flight_info['Origin Airport']}:{self.dest.flight_info['Destination Airport']}"
        return f"{self.origin.flight_info['Origin Airport']}:{self.origin.flight_info['Destination Airport']} --{self.flow}/{self.capacity}--> {self.dest.flight_info['Origin Airport']}:{self.dest.flight_info['Destination Airport']}"


def build_graph(processed_data):
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
