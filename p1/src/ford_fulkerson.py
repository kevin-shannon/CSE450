import math

from collections.abc import Iterable


def solve(V):
    while True:
        # Reset labels
        for key in V:
            if isinstance(V[key], Iterable):
                for v in V[key]:
                    v.label = None
            else:
                V[key].label = None
        V['S'].label = True
        # if no path exists then halt; maximum flow has been achieved
        if not dfs(V['S']):
            return
        # Augment
        min_delta = math.inf
        vertex = V['T']
        while vertex != V['S']:
            edge = vertex.label
            min_delta =  min(min_delta, edge.capacity - edge.flow) if edge.dest == vertex else min(min_delta, edge.flow)
            vertex = away(vertex, edge)
        # Update flows by delta
        vertex = V['T']
        while vertex != V['S']:
            edge = vertex.label
            edge.flow = edge.flow + min_delta if edge.dest == vertex else edge.flow - min_delta
            vertex = away(vertex, edge)

def dfs(u):
    for edge in u.edges:
        if labelable(u, edge):
            v = away(u, edge)
            v.label = edge
            if v.is_sink_vertex:
                return True
            else:
                p = dfs(v)
            if p:
                return p

def away(u, edge):
    if u == edge.origin:
        return edge.dest
    else:
        return edge.origin

def labelable(u, edge):
    if u == edge.origin:
        return True if edge.dest.label is None and edge.capacity > edge.flow else False
    else:
        return True if edge.origin.label is None and edge.flow > 0 else False
