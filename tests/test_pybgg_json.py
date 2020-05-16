from pybgg_json.pybgg_json import PyBggInterface
import json
import unittest

expected_keys = {
    'items': ['termsofuse', 'item'],
    # There are actually multiple fields that use item as a keyword, so this combines all seen
    'item': ['type', 'id', 'thumbnail', 'image', 'name', 'description', 'yearpublished',
             'minplayers', 'maxplayers', 'poll', 'playingtime', 'productcode', 'minplaytime', 'maxplaytime',
             'minage', 'link', 'width', 'length', 'depth', 'weight', 'versions', 'videos',
             'comments', 'ratingcomments', 'statistics', 'marketplacelistings', 'rank', 'objecttype',
             'objectid', 'subtypes'],
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
    'boardgamefamily': ['id', 'value', 'inbound'],
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
    'forums': ['type', 'id', 'termsofuse', 'forum'],
    'forum': ['id', 'title', 'numthreads', 'numposts', 'lastpostdate', 'noposting', 'termsofuse', 'threads', 'groupid', 'description'],
    'threads': ['thread'],
    'thread': ['id', 'subject', 'author', 'numarticles', 'postdate', 'lastpostdate', 'termsofuse', 'articles', 'link'],
    'articles': ['article'],
    # TODO: Check if article date field gets based off of postdate or editdate
    'article': ['id', 'username', 'link', 'postdate', 'editdate', 'numedits', 'subject', 'body'],
    'user': ['id', 'name', 'termsofuse', 'firstname', 'lastname', 'avatarlink', 'yearregistered', 'lastlogin',
                'stateorprovince', 'country', 'webaddress', 'xboxaccount', 'wiiaccount', 'psnaccount', 'battlenetaccount',
                'steamaccount', 'traderating', 'marketrating', 'buddies', 'guilds', 'hot', 'top'],
    'buddies': ['total', 'page', 'buddy'],
    'buddy': ['id', 'name'],
    'guilds': ['total', 'page', 'guild'],
    'guild': ['id', 'name'],
    'hot': ['domain', 'item'],
    'top': ['domain', 'item'],
    'guild': ['id', 'name', 'created', 'termsofuse', 'category', 'website', 'manager', 'description',
                'location', 'members'],
    'location': ['addr1', 'addr2', 'city', 'stateorprovince', 'postalcode', 'country'],
    'members': ['count', 'page', 'member'],
    'member': ['name', 'date'],
    'plays': ['username', 'userid', 'total', 'page', 'termsofuse', 'play'],
    'play': ['id', 'date', 'quantity', 'length', 'incomplete', 'nowinstats', 'location', 'item', 'players'],
    'subtypes': ['subtype'],
    'players': ['player'],
    'player': ['username', 'userid', 'name', 'startposition', 'color', 'score', 'new', 'rating', 'win'],
}


def check_all_element_data(elem, parent_key):
    if parent_key is None:
        return True

    if type(elem) != dict:
        return True

    # print(parent_key)
    # print(elem.keys())
    # print(expected_keys.get(parent_key, {}))

    return all(item in expected_keys.get(parent_key, {}) for item in elem.keys())

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
    assert check_json(bgg_int.thing_item_request(id=266192)) == True

def test_thing_items_request_all():
    bgg_int = PyBggInterface()
    assert check_json(bgg_int.thing_item_request(id=237182, versions=1, videos=1, stats=1, historical=0, marketplace=1, comments=1, ratingcomments=1)) == True

def test_family_items_request_basic():
    bgg_int = PyBggInterface()
    assert check_json(bgg_int.family_item_request(id=55566)) == True

def test_forum_list_basic():
    bgg_int = PyBggInterface()
    assert check_json(bgg_int.forum_list_request(id=194182)) == True

def test_forum_list_thing():
    bgg_int = PyBggInterface()

    assert check_json(bgg_int.forum_list_request(id=224517, type='thing')) == True

def test_forum_list_family():
    bgg_int = PyBggInterface()
    assert check_json(bgg_int.forum_list_request(id=46915, type='family')) == True

def test_forum_request_basic():
    bgg_int = PyBggInterface()
    assert check_json(bgg_int.forum_request(id=19)) == True

def test_forum_request_all():
    bgg_int = PyBggInterface()
    assert check_json(bgg_int.forum_request(id=974655, page=18)) == True

def test_thread_request_basic():
    bgg_int = PyBggInterface()
    assert check_json(bgg_int.thread_request(id=2375680)) == True

def test_thread_request_min_article_id():
    bgg_int = PyBggInterface()

    min_article_id_request = bgg_int.thread_request(id=2352640, min_article_id=33837087)
    assert check_json(min_article_id_request) == True

    full_thread_request = bgg_int.thread_request(id=2352640)

    assert (len(json.loads(full_thread_request)['thread']['articles']['article']) - len(json.loads(min_article_id_request)['thread']['articles']['article'])) == 4

def test_thread_request_min_article_date_no_hms():
    bgg_int = PyBggInterface()

    min_article_date_request = bgg_int.thread_request(id=2343582, min_article_date='2020-01-07')
    assert check_json(min_article_date_request) == True

    full_thread_request = bgg_int.thread_request(id=2343582)

    assert (len(json.loads(full_thread_request)['thread']['articles']['article']) - len(json.loads(min_article_date_request)['thread']['articles']['article'])) == 6

def test_thread_request_min_article_date_hms():
    bgg_int = PyBggInterface()

    min_article_date_request = bgg_int.thread_request(id=2343582, min_article_date='2020-01-07%2006:07:08')
    assert check_json(min_article_date_request) == True

    full_thread_request = bgg_int.thread_request(id=2343582)

    assert (len(json.loads(full_thread_request)['thread']['articles']['article']) - len(json.loads(min_article_date_request)['thread']['articles']['article'])) == 7

def test_thread_request_count():
    bgg_int = PyBggInterface()

    count_request = bgg_int.thread_request(id=2330040, count=2)
    assert check_json(count_request) == True
    assert len(json.loads(count_request)['thread']['articles']['article']) == 2

def test_user_request_basic():
    bgg_int = PyBggInterface()
    assert check_json(bgg_int.user_request(name='mcpat0226')) == True

def test_user_request_buddies():
    bgg_int = PyBggInterface()
    assert check_json(bgg_int.user_request(name='DrFlanagan', buddies=1)) == True

def test_user_request_guilds():
    bgg_int = PyBggInterface()

    assert check_json(bgg_int.user_request(name='mcpat0226', guilds=1)) == True

def test_user_request_hot():
    bgg_int = PyBggInterface()

    assert check_json(bgg_int.user_request(name='DrFlanagan', hot=1)) == True

def test_user_request_top():
    bgg_int = PyBggInterface()
    assert check_json(bgg_int.user_request(name='mcpat0226', top=1)) == True

def test_user_request_page():
    bgg_int = PyBggInterface()
    assert check_json(bgg_int.user_request(name='mcpat0226', page=2)) == True

def test_guild_request_basic():
    bgg_int = PyBggInterface()
    assert check_json(bgg_int.guild_request(id=1622)) == True

def test_guild_request_members():
    bgg_int = PyBggInterface()
    assert check_json(bgg_int.guild_request(id=1622, members=1)) == True
    
def test_plays_basic_request():
    bgg_int = PyBggInterface()
    assert check_json(bgg_int.plays_request(username='mcpat0226')) == True
