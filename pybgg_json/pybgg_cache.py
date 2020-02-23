import json
import hashlib

class PyBggCache(object):

    cache_dir = "pybgg-json/cache/"
    
    def __init__(self, cache_dir=cache_dir):
        
        self.cache_dir = cache_dir
        
