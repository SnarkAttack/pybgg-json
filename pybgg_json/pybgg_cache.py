import json
import hashlib
import os

class PyBggCache(object):

    cache_dir = "pybgg_cache/"
    
    def __init__(self, cache_dir=cache_dir):
        
        self.cache_dir = cache_dir
        
    def check_cache(self, file_name):
        
        full_path = os.path.join(self.cache_dir, file_name)
 
        if os.path.exists(full_path):
            try:
                results = None
                with open(full_path, 'r') as f:
                    results = json.load(f)
                return results
            except:
                return None
        else:
            return None
        
    def cache_result(self, file_name, result_data):
        
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        
        file_path = os.path.join(self.cache_dir, file_name)
        
        with open(file_path, 'w') as f:
            json.dump(result_data, f)
            
    
        
        
