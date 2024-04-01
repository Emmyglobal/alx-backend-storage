#!/usr/bin/env python3
"""
Change school topics
"""


def update_topics(mongo_collection, name, topics):
    """
    a Python function that changes all topics of a school document
    based on the name"""
    myquery = {"name": name}
    newval = {"$set": {"topics": topics}}
    return mongo_collection.update_many(myquery, newval)
