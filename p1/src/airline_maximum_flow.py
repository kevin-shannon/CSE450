from ford_fulkerson import solve
from graph import build_graph

V = build_graph('../process/processed_data/itinerary.csv')
solve(V)
print(f"Maximum Flow: {sum([edge.flow for edge in V['T'].edges])}")
