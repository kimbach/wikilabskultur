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
    url = 'https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bobject_number%3D'+object_number+'%5D'
    data = json.loads(requests.get('https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bobject_number%3A'+object_number+'%5D').text)
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

def get_smk_objects(offset, rows):
    url='https://api.smk.dk/api/v1/art/search/?keys=*&offset='+str(offset)+'&rows='+str(rows)
#    url='https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bpublic_domain%3Atrue%5D,%5Bhas_image%3Atrue%5D&offset='+str(offset)+'&rows='+str(rows)
    data=json.loads(requests.get(url).text)
    return(data)