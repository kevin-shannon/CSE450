import math

from graph import build_graph


def solve(V):
    while True:
        # Reset labels
        for key in V:
            if key != 'S' and key != 'T':
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
        edge = vertex.label
        while vertex != V['S']:
            if edge.dest == vertex:
                min_delta = min(min_delta, edge.capacity - edge.flow)
                vertex = edge.origin
            else:
                min_delta = min(min_delta, edge.flow)
                vertex = edge.dest
            edge = vertex.label
        # Update flows by delta
        vertex = V['T']
        edge = vertex.label
        while vertex != V['S']:
            if edge.dest == vertex:
                edge.flow += min_delta
                vertex = edge.origin
            else:
                edge.flow -= min_delta
                vertex = edge.dest
            edge = vertex.label

def dfs(v):
    for edge in v.edges:
        if labelable(v, edge):
            if v == edge.origin:
                edge.dest.label = edge
                if edge.dest == V['T']:
                    return True
                else:
                    p = dfs(edge.dest)
            else:
                edge.origin.label = edge
                if edge.origin == V['T']:
                    return True
                else:
                    p = dfs(edge.origin)
            if p:
                return p

def labelable(v, edge):
    if v == edge.origin:
        return True if edge.dest.label is None and edge.capacity > edge.flow else False
    else:
        return True if edge.origin.label is None and edge.flow > 0 else False


V = build_graph('../process/processed_data/itinerary.csv')
solve(V)
print(f"Maximum Flow: {sum([edge.flow for edge in V['T'].edges])}")
