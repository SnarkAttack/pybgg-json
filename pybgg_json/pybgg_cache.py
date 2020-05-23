import json
import hashlib
import os
import time
from .pybgg_utils import get_type_of_request

HOUR_IN_SEC = 60*60
DAY_IN_SEC = HOUR_IN_SEC*24

class PyBggCache(object):
    
    refresh_times = {
        'collection': DAY_IN_SEC,
        'thing': 7*DAY_IN_SEC
    }

    cache_dir = "pybgg_cache/"
    
    def __init__(self, cache_dir=cache_dir):
        
        self.cache_dir = cache_dir
        
    def check_cache(self, url):
        
        file_name = hashlib.md5(url.encode()).hexdigest()
        file_path = os.path.join(self.cache_dir, file_name)
        
        if time.time() - os.path.getmtime(file_path) > self.refresh_times[get_type_of_request(url)]:
            return None
 
        if os.path.exists(file_path):
            try:
                results = None
                with open(file_path, 'r') as f:
                    results = json.load(f)
                return results
            except:
                return None
        else:
            return None
        
    def cache_result(self, url, result_data):
        
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        
        file_name = hashlib.md5(url.encode()).hexdigest()
        file_path = os.path.join(self.cache_dir, file_name)
        
        with open(file_path, 'w') as f:
            json.dump(result_data, f)
            
    
        
        
