from graph import build_graph


def solve(V):
    V['S'].label = True
    path = dfs(V['S'], [])
    augment(path)

def dfs(v, path):
    for edge in v.forward_edges:
        if forward_labelable(edge):
            if edge.vertex == V['T']:
                return path + [(edge, 'forward')]
            else:
                edge.delta = edge.capacity - edge.flow
                edge.vertex.label = edge
                p = dfs(edge.vertex, path + [(edge, 'forward')])
                if p:
                    return p
    for edge in v.backward_edges:
        if backward_labelable(edge):
            if edge.vertex == V['T']:
                return path + [(edge, 'backward')]
            else:
                edge.delta = edge.flow
                edge.vertex.label = edge
                p = dfs(edge.vertex, path + [(edge, 'backward')])
                if p:
                    return p


def augment(path):
    delta = min(path, key=lambda x: x[0].delta)
    for edge in path:
        if edge[1] == 'forward':
            edge[0].flow += delta
        elif edge[1] == 'backward':
            edge[0].flow -= delta

def forward_labelable(edge):
    return True if edge.vertex.label is None and edge.capacity > edge.flow else False

def backward_labelable(edge):
    return True if edge.vertex.label is None and edge.flow > 0 else False


V = build_graph('../process/processed_data/itinerary.csv')
solve(V)
