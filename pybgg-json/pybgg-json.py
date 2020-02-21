import requests
import datetime
import collections
import xml.etree.ElementTree as ElementTree
import pprint

base_api_url = "https://www.boardgamegeek.com/xmlapi2/"

min_date = datetime.date.min.strftime("%Y-%m-%d")
max_date = datetime.date.max.strftime("%Y-%m-%d")

# Returns root of ElementTree
def _make_request(request_url):
     full_url = base_api_url + request_url
     print(full_url)
     r = requests.get(full_url)
     
     return ElementTree.fromstring(r.text)
     
def _generate_dict_from_element_tree(root):
    root_dict = root.attrib
    for child in root:
        child_dict = _generate_dict_from_element_tree(child)
        if root_dict.get(child.tag, None) is not None:
            if type(root_dict[child.tag]) == list:
                root_dict[child.tag].append(child_dict)
            else:
                root_dict[child.tag] = [root_dict[child.tag], child_dict]
        else:
            root_dict[child.tag] = child_dict
    return root_dict

def thing_items_request(id, thing_type='', versions=0, videos=0, stats=0, historical=0, 
                        marketplace=0, comments=0, ratingcomments=0, page=1, page_size=100, 
                        date_from=min_date, date_to=max_date):
    
    # Date from and date to are not currently supported by BoardGameGeek
    thing_items_url = (
                f"thing?id={id}&thing_type={thing_type}&versions={versions}&videos={videos}&"
                f"stats={stats}&historical={historical}&marketplace={marketplace}&comments={comments}&"
                f"ratingcomments={ratingcomments}&page={page}&page_size={page_size}"
    )
                        
    thing_root = _make_request(thing_items_url)
    
    nodes = collections.deque([thing_root])
    
    ret_dict = {}
    
    pp = pprint.PrettyPrinter(indent=4)
 
    pp.pprint(_generate_dict_from_element_tree(thing_root))
    
thing_items_request(id=266192)