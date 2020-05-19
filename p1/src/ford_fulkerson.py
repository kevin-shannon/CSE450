'''
File name :   ford_fulkerson.py
Author :      Kevin Shannon
Date :        04/18/2020
Description : General implementation of the Ford-Fulkerson algorithm using
              depth-first search.
'''

import math

from collections.abc import Iterable


def solve(V):
    '''
    The heart of Ford-Fulkerson algorithm, V must be a dictionary with 'S' as
    the source and 'T' as the sink. The values of the dictionary may be individual
    values or iterables.

    Parameters
    ----------
    V : dict
        Data structure containg vertices of the graph to be solved.
    '''
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
            min_delta =  min(min_delta, edge.capacity - edge.flow if edge.dest == vertex else edge.flow)
            vertex = away(vertex, edge)
        # Update flows by delta
        vertex = V['T']
        while vertex != V['S']:
            edge = vertex.label
            edge.flow = edge.flow + min_delta if edge.dest == vertex else edge.flow - min_delta
            vertex = away(vertex, edge)

def dfs(u):
    '''
    Recursive depth-first-searh algorithm that looks for labelable vertices.

    Parameters
    ----------
    u : Vertex
        Current vertex being evaluated.

    Returns
    -------
    p : bool or None
        True only if a path to the sink was found.
    '''
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
    '''
    Parameters
    ----------
    u : Vertex
        Current vertex being evaluated.
    edge : Edge
        Edge associated with u.

    Returns
    -------
    Vertex
        Vertex that is on the other side of the edge from u.
    '''
    if u == edge.origin:
        return edge.dest
    else:
        return edge.origin

def labelable(u, edge):
    '''
    Parameters
    ----------
    u : Vertex
        Current vertex being evaluated.
    edge : Edge
        Edge associated with u.

    Returns
    -------
    bool
        True if the vertex away from u is eligible for labeling.
    '''
    if u == edge.origin:
        return True if edge.dest.label is None and edge.capacity > edge.flow else False
    else:
        return True if edge.origin.label is None and edge.flow > 0 else False
