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

    def forum_list_request(self, id, type='thing'):

        forum_list_url = (
                    f"forumlist?id={id}&type={type}"
        )

        root = pybgg_utils._make_request(forum_list_url)

        return json.dumps(pybgg_utils._generate_dict_from_element_tree(root))

    def forum_request(self, id, page=1):

        forum_url = (
                    f"forum?id={id}&page={page}"
        )

        root = pybgg_utils._make_request(forum_url)

        return json.dumps(pybgg_utils._generate_dict_from_element_tree(root))

    def thread_request(self, id, min_article_id=0, min_article_date='', count=-1, username=''):

        thread_url = (
                    f"thread?id={id}&minarticleid={min_article_id}&minarticledate={min_article_date}"
        )

        if count != -1:
            thread_url += f"&count={count}"

        root = pybgg_utils._make_request(thread_url)

    def user_request(self, name, buddies=0, guilds=0, hot=0, top=0, domain='boardgame', page=1):

        user_url = (
                  f"user?id={id}&buddies={buddies}&guilds={guilds}&hot={hot}&top={top}&domain={domain}&page={page}"
        )

        root = pybgg_utils._make_request(user_url)

        return json.dumps(pybgg_utils._generate_dict_from_element_tree(root))

