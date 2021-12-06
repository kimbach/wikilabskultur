# smkapi
#
# Functions for SMK API
#
# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = empty_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, Optional, List, TypeVar, Type, Callable, cast
from enum import Enum
from datetime import datetime
import dateutil.parser
import json
import requests
import pathlib
import smkitem

def get_smk_object(object_number):
    # url = 'https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bobject_number%3D'+object_number+'%5D'
    url = 'https://api.smk.dk/api/v1/art/?object_number='+object_number
    data = json.loads(requests.get(url).text)
    return(data)
    #items=data['items'].get()
    #print(items[0].image_native)
    
    # Map to obejct model
    #smk_items = smkitem.empty_from_dict(data)

    #return smk_items

    # Iterate over Items
    #for item in smk_items.items:
    #    item.image_native


    #for keys, item in recursive_iter(data['items']):
    #    print('keys')
    #    print(keys)
    #    print('item')
    #    print(item)
        #if 'true' == keys[0]['has_image']:
        #    if 'image_native' == keys[0]: 
        #        print(item)
        #print(keys)

    #    item[0].get()
        #print(item['image_native'])
    #response = json.loads(requests.get("https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bpublic_domain%3Atrue%5D,%5Bhas_image%3Atrue%5D&offset=0&rows=10").text)
    #print(response)

    #for item in recursive_iter(response):
    #    print(item)

# Get all wikidata items for SMK Wikidata object Q671384
#wikidata.GetInstitutionWikidataItems('Q671384', 'wikidata_smk.csv')
#TestSMKAPI()
#get_smk_object('KMS1')

def last_flagged(seq):
    # Function that returns true if the list item ius
    seq = iter(seq)
    a = next(seq)
    for b in seq:
        yield a, False
        a = b
    yield a, True        

def generate_smk_filter(smk_filter_list):
    smk_filter=""
    for filter,is_last in last_flagged(smk_filter_list):
        smk_filter=smk_filter+"%5B"+filter[0]+"%3A"+filter[1]+"%5D"
        if not is_last:
            smk_filter=smk_filter+","
    return smk_filter

def get_smk_objects(smk_filter, offset, rows):
#    url='https://api.smk.dk/api/v1/art/search/?keys=*&offset='+str(offset)+'&rows='+str(rows)
    url='https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bpublic_domain%3Atrue%5D,%5Bhas_image%3Atrue%5D&offset='+str(offset)+'&rows='+str(rows)
    #https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bpublic_domain%3Atrue%5D,%5Bhas_image%3Atrue%5D,%5Bcreator_gender%3Akvinde%5D,%5Bcreator_nationality%3Adansk%5D&offset=0&rows=10
    url='https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bpublic_domain%3Atrue%5D,%5Bhas_image%3Atrue%5D,%5Bcreator_gender%3Akvinde%5D,%5Bcreator_nationality%3Adansk&offset='+str(offset)+'&rows='+str(rows)
    url='https://api.smk.dk/api/v1/art/search/?keys=*'
    if smk_filter!='':
        url=url+'&filters='+smk_filter
    url=url+'&offset='+str(offset)+'&rows='+str(rows)
    data=json.loads(requests.get(url).text)
    return(data)