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

    def thing_items_request(self, id, thing_type='', versions=0, videos=0, stats=0, historical=0, 
                            marketplace=0, comments=0, ratingcomments=0, page=1, page_size=100, 
                            date_from=min_date, date_to=max_date):
        
        # Date from and date to are not currently supported by BoardGameGeek
        thing_items_url = (
                    f"thing?id={id}&thing_type={thing_type}&versions={versions}&videos={videos}&"
                    f"stats={stats}&historical={historical}&marketplace={marketplace}&comments={comments}&"
                    f"ratingcomments={ratingcomments}&page={page}&page_size={page_size}"
        )

        #test_dict = {'videos': {'total': '262', 'video': [{'id': '252015', 'title': 'Wingspan unboxing', 'category': 'unboxing', 'language': 'English', 'link': 'http://www.youtube.com/watch?v=wrNqy3DcVwE', 'username': 'cdholmes', 'userid': '1080017', 'postdate': '2020-02-18T12:52:18-06:00'}, {'id': '251705', 'title': 'Roc Reviews - Wingspan & European Expansion', 'category': 'review', 'language': 'English', 'link': 'http://www.youtube.com/watch?v=CIprVDwqHFI', 'username': 'AndrewJRager', 'userid': '1519609', 'postdate': '2020-02-16T12:03:27-06:00'}, {'id': '250994', 'title': 'Flügelschlag + Europa Erweiterung Review und Regelerklärung', 'category': 'review', 'language': 'German', 'link': 'http://www.youtube.com/watch?v=vaZFU9pcgwg', 'username': 'LosNossos', 'userid': '1231123', 'postdate': '2020-02-10T11:01:00-06:00'}, {'id': '250820', 'title': 'Solo Playthrough  - Wingspan', 'category': 'session', 'language': 'English', 'link': 'http://www.youtube.com/watch?v=MuwDGdsqSHg', 'username': 'Ludomania', 'userid': '134673', 'postdate': '2020-02-09T03:19:56-06:00'}, {'id': '250565', 'title': 'Wingspan | Shelfside Review', 'category': 'review', 'language': 'English', 'link': 'http://www.youtube.com/watch?v=gzzjF4qC8Og', 'username': 'Raynify', 'userid': '852250', 'postdate': '2020-02-07T15:38:29-06:00'}, {'id': '249880', 'title': 'WingSpawn Review', 'category': 'review', 'language': 'Japanese', 'link': 'http://www.youtube.com/watch?v=jhO_7vGEP-Q', 'username': 'akito0190', 'userid': '1665835', 'postdate': '2020-02-03T13:20:24-06:00'}, {'id': '249311', 'title': 'How to play Wingspan in 9 Minutes - Teach The Table', 'category': 'instructional', 'language': 'English', 'link': 'http://www.youtube.com/watch?v=PrA_iS-ukw4', 'username': 'turtlenate', 'userid': '313755', 'postdate': '2020-01-29T16:55:32-06:00'}, {'id': '248852', 'title': 'Tom Teaches Wingspan (Solo Setup and Gameplay)', 'category': 'session', 'language': 'English', 'link': 'http://www.youtube.com/watch?v=POoBQ1xgVA4', 'username': 'dahbuss', 'userid': '629774', 'postdate': '2020-01-26T15:27:11-06:00'}, {'id': '248540', 'title': 'Cómo jugar/How to play', 'category': 'instructional', 'language': 'Spanish', 'link': 'http://www.youtube.com/watch?v=tLjI8pNXmiA', 'username': 'JB el lobo', 'userid': '2002609', 'postdate': '2020-01-24T03:29:21-06:00'}, {'id': '247239', 'title': 'Wingspan Board Game Review / How to Play', 'category': 'review', 'language': 'English', 'link': 'http://www.youtube.com/watch?v=xhlJYKeo8kQ', 'username': 'zmikers', 'userid': '1481845', 'postdate': '2020-01-12T02:11:56-06:00'}, {'id': '247223', 'title': 'Abrindo: Wingspan', 'category': 'unboxing', 'language': 'Portuguese', 'link': 'http://www.youtube.com/watch?v=T5rzSscGVXY', 'username': 'Micaelsousa', 'userid': '790334', 'postdate': '2020-01-11T16:30:38-06:00'}, {'id': '245841', 'title': 'Wingspan with the European Expansion Playthrough - Full Session', 'category': 'session', 'language': 'English', 'link': 'http://www.youtube.com/watch?v=ksTKZjeVJec', 'username': 'Athex', 'userid': '20808', 'postdate': '2019-12-28T13:55:40-06:00'}, {'id': '245758', 'title': 'Cómo se juega exprés | Not in my Game', 'category': 'instructional', 'language': 'Spanish', 'link': 'http://www.youtube.com/watch?v=lR4vj6EkXo4', 'username': 'GatthePekerd', 'userid': '1303281', 'postdate': '2019-12-27T08:05:23-06:00'}, {'id': '245701', 'title': 'Wojennik TV # 302: Wingspan (Na Skrzydłach) (tryb solo) - recenzja', 'category': 'review', 'language': 'Polish', 'link': 'http://www.youtube.com/watch?v=bh0Ftytze00', 'username': 'Jean_Leviathan', 'userid': '234662', 'postdate': '2019-12-26T13:18:10-06:00'}, {'id': '245693', 'title': 'A Conversation With - Wingspan Designer Elizabeth Hargrave - (Quackalope Games)', 'category': 'interview', 'language': 'English', 'link': 'http://www.youtube.com/watch?v=zNZWUcIICPY', 'username': 'Quackalope', 'userid': '1996209', 'postdate': '2019-12-26T10:43:22-06:00'}]}}
        #test_dict = {'videos': {'total': '262', 'video': [{'id': '252015', 'title': 'Wingspan unboxing', 'category': 'unboxing', 'language': 'English', 'link': 'http://www.youtube.com/watch?v=wrNqy3DcVwE', 'username': 'cdholmes', 'userid': '1080017', 'postdate': '2020-02-18T12:52:18-06:00'}]}}
        #test_dict = {'list': ['1', '2', '3', '4']}
                    
        root = pybgg_utils._make_request(thing_items_url)
        #root = _open_xml_request_file('wingspan_mid.xml')
        
        # for neighbor in root.iter('link'):
        #     print(_generate_dict_from_element_tree(neighbor))
        
        #print(_personal_pretty_print(test_dict))
        #print(_generate_dict_from_element_tree(root))
        #print(pybgg_utils._personal_pretty_print(pybgg_utils._generate_dict_from_element_tree(root), 0))
        
        return json.dumps(pybgg_utils._generate_dict_from_element_tree(root))

if __name__ == "__main__":
    
    
    bgg_interface = PyBggInterface()
    
    bgg_interface.thing_items_request(id=266192, videos=1)