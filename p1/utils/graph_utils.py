from datetime import datetime
from datetime import timedelta

def bisect_left(a, x, lo=0, hi=None, key=lambda x: x):
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if key(a[mid]) <= x: lo = mid+1
        else: hi = mid
    return lo

def parse_departure_time(flight):
    return datetime.strptime(flight['Date (MM/DD/YYYY)']+'|'+flight['Scheduled departure time'], '%m/%d/%Y|%H:%M')

def parse_arrival_time(flight):
    return datetime.strptime(flight['Date (MM/DD/YYYY)']+'|'+flight['Arrival Time'], '%m/%d/%Y|%H:%M')
