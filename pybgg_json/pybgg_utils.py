import requests
import xml.etree.ElementTree as ElementTree

base_api_url = "https://www.boardgamegeek.com/xmlapi2/"


pivot_list = ['type']
no_mod_list = ['item']
condense_lists_tags = ['item', 'results']
prevent_condense_tags = ['poll', 'result']


def _personal_pretty_print(elem, indent=0):
        rec_str = ""
        if type(elem) == dict:
            rec_str += "{\n"
            for key, value in elem.items():
                rec_str += " "*(indent+4)+f"{key}: {_personal_pretty_print(value, indent+4)}\n"
            rec_str += " "*indent+"},"
        elif type(elem) == list:
            rec_str += "[\n"
            for list_elem in elem:
                rec_str += " "*(indent+4)+f"{_personal_pretty_print(list_elem, indent+4)}\n"
            rec_str += " "*(indent)+"],"
        else:
            rec_str += elem
            
        return rec_str

# BGG results return a lot of xml in repeating tags (like <link>). To ease usage (and because python dicts
# obviously only allow each key once) if we find duplicate keys we will convert the value mapped by the key
# into a list and append to that
def _update_and_merge_dict(dict1, dict2):
    keys1 = dict1.keys()
    keys2 = dict2.keys()
    
    for key in keys2:
        if key in keys1:
            if type(dict1[key]) == list:
                dict1[key].append(dict2[key])
            else:
                dict1[key] = [dict1[key], dict2[key]]
        else:
            dict1[key] = dict2[key]

def _dict_w_ele_rem(dic, ele):
    dic = dic.copy()
    dic.pop(ele)
    return dic

# Returns root of ElementTree
def _make_request(request_url):
    full_url = base_api_url + request_url
    print(full_url)
    r = requests.get(full_url)
    
    f = open('wingspan_mid.xml', 'w')
    f.write(r.text)
    f.close()
    
    return ElementTree.fromstring(r.text)

def _open_xml_request_file(file_path):
    
    return ElementTree.parse(file_path).getroot()
    
def _generate_dict_from_element_tree(root):
    # Make copy so we aren't actually modifying element tree data
    root_dict = root.attrib.copy()
    
    if root.text is not None and len(root.text.strip(" \n\t\r")) > 0:
        return {root.tag: root.text}
    
    if len(root.attrib) == 1 and root.attrib.get('value') is not None:
        return {root.tag: root.attrib['value']}
    
    for key in root.attrib.keys():
        if key in pivot_list and root.tag not in no_mod_list:
            return {root.tag: {root.attrib[key]: _dict_w_ele_rem(root.attrib, key)}}
    
    for child in root:    
        # Move recursively throughout tree 
        child_result = _generate_dict_from_element_tree(child)
        _update_and_merge_dict(root_dict, child_result)
        
    # See if there's a better way to do this
    for key, value in root_dict.items():
        # If the given tag in list, we're not really looking to condense them
        if root.tag in condense_lists_tags and key not in prevent_condense_tags and type(value) == list:
            new_dict = {}
            for elem in value:
                inner_key = list(elem.keys())[0]
                if new_dict.get(inner_key) is None:
                    new_dict[inner_key] = []
                new_dict[inner_key].append(elem[inner_key])
            root_dict[key] = new_dict
        
            
    return {root.tag: root_dict}