from pybgg_json.pybgg_json import PyBggInterface
import json
import unittest

expected_keys_thing_items = {
    'items': ['termsofuse', 'item'],
    'item': ['type', 'id', 'thumbnail', 'image', 'name', 'description', 'yearpublished',
             'minplayers', 'maxplayers', 'poll', 'playingtime', 'minplaytime', 'maxplaytime',
             'minage', 'link'],
    'primary': ['sortindex', 'value'],
    'poll': ['name', 'title', 'totalvotes', 'results'],
    'boardgame': ['id', 'value'],
}

def check_all_element_data(elem, parent_key):
    if parent_key is None:
        return True
    
    if type(parent_key) != dict:
        return True
    
    return all(item in expected_keys_thing_items[key] for item in value.keys())

def check_elem(elem, parent_key):
    if type(elem) == dict:
        check_all_element_data(elem, parent_key)
        return all(check_elem(value, key) for key, value in elem.items())
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
    

        
    