#!/usr/bin/env python3
"""
List all docs in Python
"""


def list_all(mongo_collection):
    """
    a Python function that lists all documents in a collection
    """
    docs = [x for x in mongo_collection.find()]

    return docs
