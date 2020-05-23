import json
import datetime
import collections
import hashlib
import xml.etree.ElementTree as ElementTree
import pybgg_json.pybgg_utils as pybgg_utils
from pybgg_json.pybgg_cache import PyBggCache

MIN_DATE = datetime.date.min.strftime("%Y-%m-%d")
MAX_DATE = datetime.date.max.strftime("%Y-%m-%d")

class PyBggInterface(object):

    def __init__(self, cache=PyBggCache()):
        self.cache = cache
        
    def make_request(self, url):
        if self.cache is not None:
            results = self.cache.check_cache(url)
            if results is not None:
                return results
            else:
                root = pybgg_utils._make_request(url)
                results = pybgg_utils._generate_dict_from_element_tree(root)
                self.cache.cache_result(url, results)
                return results
        else:
            root = pybgg_utils._make_request(url)
            if root is not None:
                results = pybgg_utils._generate_dict_from_element_tree(root)
            else:
                return {}
            return results
            
            

    def thing_item_request(self, id, type='', versions=0, videos=0, stats=0, historical=0, 
                            marketplace=0, comments=0, ratingcomments=0, page=1, page_size=100, 
                            date_from=MIN_DATE, date_to=MAX_DATE):

        # Date from and date to are not currently supported by BoardGameGeek
        thing_items_url = (
                    f"thing?id={id}&type={type}&versions={versions}&videos={videos}&"
                    f"stats={stats}&historical={historical}&marketplace={marketplace}&comments={comments}&"
                    f"ratingcomments={ratingcomments}&page={page}&page_size={page_size}"
        )

        return self.make_request(thing_items_url)

    def family_item_request(self, id, type=''):

        family_items_url = (
                    f"family?id={id}&type={type}"
        )

        return self.make_request(family_items_url)

    def forum_list_request(self, id, type='thing'):

        forum_list_url = (
                    f"forumlist?id={id}&type={type}"
        )

        return self.make_request(forum_list_url)

    def forum_request(self, id, page=1):

        forum_url = (
                    f"forum?id={id}&page={page}"
        )

        return self.make_request(forum_url)

    def thread_request(self, id, min_article_id=0, min_article_date='', count=-1, username=''):

        thread_url = (
                    f"thread?id={id}&minarticleid={min_article_id}&minarticledate={min_article_date}"
        )

        if count != -1:
            thread_url += f"&count={count}"

        return self.make_request(thread_url)

    def user_request(self, name, buddies=0, guilds=0, hot=0, top=0, domain='boardgame', page=1):

        user_url = (
                  f"user?name={name}&buddies={buddies}&guilds={guilds}&hot={hot}&top={top}&"
                  f"domain={domain}&page={page}"
        )

        return self.make_request(user_url)

    def guild_request(self, id, members=0, sorttype='username', page=1):

        guild_url = (
                   f"guild?id={id}&members={members}&sort={sorttype}&page={page}"
        )

        return self.make_request(guild_url)
    
    # Must use either username or id AND type
    def plays_request(self, username=None, id=None, type=None, mindate=MIN_DATE, 
                      maxdate=MAX_DATE, subtype='boardgame', page=1):
        
        if username is None and (id is None or type is None):
            return {}
        else:
            if username is not None:
                identifier = f"username={username}"
            else:
                identifier = f"id={id}&type={type}"
                
        plays_url = (
                    f"plays?{identifier}&mindate={mindate}&maxdate={maxdate}&subtype={subtype}&"
                    f"page={page}"
        )

        return self.make_request(plays_url)
    
    def collection_request(self, username, subtype='boardgame', exclude_subtype=None, id=None,
                           brief=None, stats=None, own=None, rated=None, playerd=None, comment=None,
                           trade=None, want=None, wishlist=None, wishlist_priority=None, preordered=None,
                           wanttoplay=None, wanttobuy=None, prevowned=None, hasparts=None, wantparts=None,
                           minrating=None, rating=None, minbggrating=None, bggrating=None, minplays=None,
                           maxplays=None, showprivate=None, collid=None, modifiedsince=MIN_DATE):
        
        collection_url = (
                    f"collection?"
        )
        
        for arg, arg_val in locals().items():
            if arg_val is not None and arg is not 'self':
                collection_url += f"{arg}={arg_val}&"
        collection_url += f"modifiedsince={modifiedsince}"
        
        return self.make_request(collection_url)