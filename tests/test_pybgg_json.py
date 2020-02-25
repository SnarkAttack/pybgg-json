from pybgg_json.pybgg_json import PyBggInterface
import json
import unittest

expected_keys_thing_items = {
    'items': ['termsofuse', 'item'],
    # There are actually multiple fields that use item as a keyword, so this combines all seen
    'item': ['type', 'id', 'thumbnail', 'image', 'name', 'description', 'yearpublished',
             'minplayers', 'maxplayers', 'poll', 'playingtime', 'productcode', 'minplaytime', 'maxplaytime',
             'minage', 'link', 'width', 'length', 'depth', 'weight', 'versions', 'videos',
             'comments', 'ratingcomments', 'statistics', 'marketplacelistings'],
    'name': ['primary', 'alternate'],
    'primary': ['sortindex', 'value'],
    'alternate': ['sortindex', 'value'],
    'poll': ['name', 'title', 'totalvotes', 'results'],
    'boardgame': ['id', 'value'],
    'results': ['numplayers', 'result'],
    'result': ['value', 'numvotes'],
    # This one gets a bit messy as well
    'link': ['boardgamecategory', 'boardgamemechanic', 'boardgamefamily', 'boardgameexpansion', 
             'boardgamedesigner', 'boardgameartist', 'boardgamepublisher', 'boardgameversion', 'language',
             'href', 'title'],
    'boardgamecategory': ['id', 'value'],
    'boardgamemechanic': ['id', 'value'],
    'boardgamefamily': ['id', 'value'],
    'boardgameexpansion': ['id', 'value'],
    'boardgamedesigner': ['id', 'value'],
    'boardgameartist': ['id', 'value'],
    'boardgamepublisher': ['id', 'value'],
    'boardgameversion': ['id', 'value', 'inbound'],
    'language': ['id', 'value'],
    'videos': ['total', 'video'],
    'video': ['id', 'title', 'category', 'language', 'link', 'username', 'userid', 'postdate'],
    'versions': ['item'],
    'comments': ['page', 'totalitems', 'comment'],
    'comment': ['username', 'rating', 'value'],
    'marketplacelistings': ['listing'],
    'listing': ['listdate', 'price', 'condition', 'notes', 'link'],
    'price': ['currency', 'value'],
    'statistics': ['page', 'ratings'],
    'ratings': ['usersrated', 'average', 'bayesaverage', 'ranks', 'stddev', 'median', 'owned', 'trading', 'wanting',
               'wishing', 'numcomments', 'numweights', 'averageweight'],
    'ranks': ['rank'],
    'rank': ['subtype'],
    'subtype': ['id', 'name', 'friendlyname', 'value', 'bayesaverage'],
    'family': ['id', 'name', 'friendlyname', 'value', 'bayesaverage'],
}

def check_all_element_data(elem, parent_key):

    if parent_key is None:
        return True

    if type(elem) != dict:
        return True

    return all(item in expected_keys_thing_items.get(parent_key, {}) for item in elem.keys())

# All we can do with these tests (because different games will have different fields and values and many can change
# over time) is to check that we expect every key value that comes back for a dictionary
def check_elem(elem, parent_key):
    if type(elem) == dict:
        return check_all_element_data(elem, parent_key) and all(check_elem(value, key) for key, value in elem.items())
    elif type(elem) == list:
        for item in elem:
            return check_elem(item, parent_key)
    else:
        return True
    
def check_json(json_str):
    bgg_dict = json.loads(json_str)
    return check_elem(bgg_dict, None)

def test_thing_items_request_basic():
    bgg_int = PyBggInterface()
    assert check_json(bgg_int.thing_items_request(id=266192)) == True

def test_thing_items_request_all():
    bgg_int = PyBggInterface()
    assert check_json(bgg_int.thing_items_request(id=266192, versions=1, videos=1, stats=1, historical=0, marketplace=1, comments=1, ratingcomments=1)) == True
