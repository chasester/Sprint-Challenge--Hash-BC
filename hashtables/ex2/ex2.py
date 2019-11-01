#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


class Ticket:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination


def reconstruct_trip(tickets, length):
    ht = HashTable(length)
    for i in tickets:
        hash_table_insert(ht,i.source, i);#put all the sorces in the db

    last = hash_table_retrieve(ht,"NONE");
    trip = [last.destination];
    while last.destination != "NONE":
        last = hash_table_retrieve(ht,last.destination)
        trip.append(last.destination);
    """
    YOUR CODE HERE
    """
    return trip
