import csv
import sys

from datetime import datetime
from datetime import timedelta

sys.path.insert(1, '../')
from utils.graph_utils import bisect_left
from utils.graph_utils import parse_departure_time
from utils.graph_utils import parse_arrival_time


class Vertex:
    def __init__(self, label=None, forward_edges=None, backward_edges=None, is_start_vertex=False, is_dest_vertex=False):
        self.label = label
        self.forward_edges = forward_edges if forward_edges is not None else []
        self.backward_edges = backward_edges if backward_edges is not None else []
        self.is_start_vertex = is_start_vertex
        self.is_dest_vertex = is_dest_vertex


class FlightVertex(Vertex):
    def __init__(self, flight_info, label=None, forward_edges=None, backward_edges=None, is_start_vertex=False, is_dest_vertex=False):
        super().__init__(label, forward_edges, backward_edges, is_start_vertex, is_dest_vertex)
        self.flight_info = flight_info
    def __repr__(self):
        return f"{self.flight_info['Origin Airport']} -> {self.flight_info['Destination Airport']} ({self.flight_info['Scheduled departure time']} -> {self.flight_info['Arrival Time']}) {self.flight_info['capacity']} seats"


class Edge:
    def __init__(self, vertex=None, flow=0, capacity=0):
        self.vertex = vertex
        self.flow = flow
        self.capacity = capacity
    def __repr__(self):
        if self.vertex.is_dest_vertex:
            return f"--{self.flow}/{self.capacity}--> T"
        elif self.vertex.is_start_vertex:
            return f"--{self.flow}/{self.capacity}--> S"
        else:
            return f"--{self.flow}/{self.capacity}--> {self.vertex}"

class FlightEdge(Edge):
    def __repr__(self):
        if self.vertex.is_dest_vertex:
            return f"--{self.flow}/{self.capacity}--> T"
        elif self.vertex.is_start_vertex:
            return f"--{self.flow}/{self.capacity}--> S"
        else:
            return f"--{self.flow}/{self.capacity}--> {self.vertex.flight_info['Origin Airport']}"


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
    vertices['S'] = Vertex(is_start_vertex=True)
    vertices['T'] = Vertex(is_dest_vertex=True)
    # Build initial edges for S
    for flight in vertices['LAX']:
        vertices['S'].forward_edges.append(FlightEdge(vertex=flight, flow=0, capacity=int(flight.flight_info['capacity'])))
        flight.backward_edges.append(FlightEdge(vertex=vertices['S'], flow=0, capacity=int(flight.flight_info['capacity'])))
    # Build edges for each flight
    for airport in airports:
        for flight in vertices[airport]:
            if flight.flight_info['Destination Airport'] != 'JFK':
                first_available_flight = bisect_left(vertices[flight.flight_info['Destination Airport']], parse_arrival_time(flight.flight_info), key=lambda x: parse_departure_time(x.flight_info))
                available_flights = vertices[flight.flight_info['Destination Airport']][first_available_flight:]
                flight.forward_edges = [FlightEdge(vertex=next_flight, flow=0, capacity=int(flight.flight_info['capacity'])) for next_flight in available_flights]
                for next_flight in available_flights:
                    next_flight.backward_edges.append(FlightEdge(vertex=flight, flow=0, capacity=int(flight.flight_info['capacity'])))
            else:
                flight.forward_edges = [Edge(vertex=vertices['T'], flow=0, capacity=int(flight.flight_info['capacity']))]
                vertices['T'].backward_edges.append(FlightEdge(vertex=flight, flow=0, capacity=int(flight.flight_info['capacity'])))
    return vertices
