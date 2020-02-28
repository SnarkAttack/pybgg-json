import json
import datetime
import collections
import xml.etree.ElementTree as ElementTree
import pybgg_json.pybgg_utils as pybgg_utils
from pybgg_json.pybgg_cache import PyBggCache

min_date = datetime.date.min.strftime("%Y-%m-%d")
max_date = datetime.date.max.strftime("%Y-%m-%d")

class PyBggInterface(object):
    
    def __init__(self, cache=PyBggCache()):
        self.cache = cache

    def thing_item_request(self, id, thing_type='', versions=0, videos=0, stats=0, historical=0, 
                            marketplace=0, comments=0, ratingcomments=0, page=1, page_size=100, 
                            date_from=min_date, date_to=max_date):
        
        # Date from and date to are not currently supported by BoardGameGeek
        thing_items_url = (
                    f"thing?id={id}&thing_type={thing_type}&versions={versions}&videos={videos}&"
                    f"stats={stats}&historical={historical}&marketplace={marketplace}&comments={comments}&"
                    f"ratingcomments={ratingcomments}&page={page}&page_size={page_size}"
        )

        root = pybgg_utils._make_request(thing_items_url)

        return json.dumps(pybgg_utils._generate_dict_from_element_tree(root))

    def family_item_request(self, id, family_type=''):

        family_items_url = (
                    f"family?id={id}&type={family_type}"
        )

        root = pybgg_utils._make_request(family_items_url)

        return json.dumps(pybgg_utils._generate_dict_from_element_tree(root))

    def forum_list_request(self, id, page=1):

        forum_list_url = (
                    f"forum?id={id}&page={page}"
        )

        root = pybgg_utils._make_request(forum_list_url)

        return json.dumps(pybgg_utils._generate_dict_from_element_tree(root))

if __name__ == "__main__":
    
    
    bgg_interface = PyBggInterface()
    
    #bgg_interface.thing_items_request(id=266192, versions=1, videos=1, stats=1, historical=1, marketplace=1, comments=1, ratingcomments=1)
    bgg_interface.family_items_request(id=266192)
