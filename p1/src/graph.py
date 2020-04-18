'''
File name :   graph.py
Author :      Kevin Shannon
Date :        04/18/2020
Description : Vertex and Edge data structures to represent a graph in a maximum
              network flow problem.
'''

class Vertex:
    '''
    Parameters
    ----------
    label : bool or Edge
        Label of the edge that labeled this vertex.
    edges : list
        All edges connected to this vertex.
    is_source_vertex : bool
        True if this is the source vertex.
    is_sink_vertex : bool
        True if this is the sink vertex.
    '''
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
    '''
    flight_info : dict
        Dictionary of csv values assosiated with a single flight.
    '''
    def __init__(self, flight_info, label=None, edges=None, is_source_vertex=False, is_sink_vertex=False):
        super().__init__(label, edges, is_source_vertex, is_sink_vertex)
        self.flight_info = flight_info

    def __repr__(self):
        return f"{self.flight_info['Origin Airport']} -> {self.flight_info['Destination Airport']} ({self.flight_info['Scheduled departure time']} -> {self.flight_info['Arrival Time']}) {self.flight_info['capacity']} seats"


class Edge:
    '''
    origin : Vertex
        Tail end of the edge.
    dest : Vertex
        Head of the edge.
    flow : int
        The flow going through the edge.
    capacity : int
        The capacity of flow through the edge.
    '''
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
