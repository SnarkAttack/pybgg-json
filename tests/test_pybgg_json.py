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

def check_elem(elem):
    print(elem)
    if type(elem) == dict:
        for key, value in elem.items():
            if type(value) == dict:
                print(expected_keys_thing_items[key])
                for x in value.keys():
                    print(x in expected_keys_thing_items[key])
                print(value.keys())
                return all(item in expected_keys_thing_items[key] for item in value.keys()) and all(check_elem(item) for item in value.values())
            elif type(value) == list:
                return all(check_elem(item) for item in value)
            else:
                return True
    elif type(elem) == list:
        for item in elem:
            return check_elem(item)
    else:
        return True
    
def check_json(json_str):
    bgg_dict = json.loads(json_str)
    return check_elem(bgg_dict)

def test_thing_items_request_basic():
    bgg_int = PyBggInterface()
    assert check_json(bgg_int.thing_items_request(id=266192)) == True
        
    