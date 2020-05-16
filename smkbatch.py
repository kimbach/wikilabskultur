# smkbatch
#
# Functions for SMK Batch Upload
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
import commons
import wikidata
import os
import pywikibot
from pywikibot import pagegenerators as pg
import logging
import traceback
import sys
import smkapi

def recursive_iter_1(obj):
    if isinstance(obj, dict):
        for item in obj.values():
            yield from recursive_iter(item)
    elif any(isinstance(obj, t) for t in (list, tuple)):
        for item in obj:
            yield from recursive_iter(item)
    else:
        yield obj

def recursive_iter(obj, keys=()):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from recursive_iter(v, keys + (k,))
    elif any(isinstance(obj, t) for t in (list, tuple)):
        for idx, item in enumerate(obj):
            yield from recursive_iter(item, keys + (idx,))
    else:
        yield keys, obj

def TestSMKAPI():
    #url = [ filename ]
    #keepFilename = False        #set to True to skip double-checking/editing destination filename
    keepFilename = True        #set to True to skip double-checking/editing destination filename
    #verifyDescription = True    #set to False to skip double-checking/editing description => change to bot-mode
    verifyDescription = False    #set to False to skip double-checking/editing description => change to bot-mode
    #targetSite = pywikibot.Site('beta', 'commons')

    #bot = UploadRobot(url, description=description, useFilename=pagetitle, keepFilename=keepFilename, verifyDescription=verifyDescription, targetSite=targetSite)
    #bot.run()

    # Get JSON from the SMK API
    #json_string = json.loads(requests.get("https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bpublic_domain%3Atrue%5D,%5Bhas_image%3Atrue%5D&offset=0&rows=10").text)
    #json_string = json.loads(requests.get("https://api.smk.dk/api/v1/art/search/?keys=*&filters=%5Bobject_number%3AKMS1%5D").text)

    #THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    #my_file = os.path.join(THIS_FOLDER, 'smkitems.json')

    #json_file = open(my_file)
    #json_string = json.load(json_file)

    # Map to obejct model
    #smk_items = smkitem.empty_from_dict(json_string)

    # Add categories
    categories  = """[[Category:Wiki Labs Kultur]]
    [[Category:Paintings in Statens Museum for Kunst]]"""

    # Iterate over Items
    # for item in smk_items.items:
    
    #     # Check for image
    #     if item.has_image: 
    #         filename=item.image_native
    #         path=pathlib.Path(filename)
            
    #         # Generate page title
    #         pagetitle='SMK-' + item.id + '-' + item.object_number + ':' + item.titles[0].title + path.suffix

    #         # Generate description
    #         desc = ''
    #         if item.content_description is not None:
    #             for line in item.content_description:
    #                 desc=desc+line
            
    #         # Generate date
    #         production_date = ''
    #         for date in item.production_date:
    #             production_date = production_date+date.start.strftime("%Y-%m-%d")+' - '+date.end.strftime("%Y-%m-%d")+'\n'  


    #         #complete_artwork_desc_and_upload(filename, pagetitle, desc, production_date, categories)

    #         # Generate artwork template
    #         artwork = commons.ArtworkTemplate(artist = '',
    #             author = '',
    #             title = '',
    #             desc = desc,
    #             depicted_people = '',
    #             date = production_date,
    #             medium = '',
    #             dimensions = '',
    #             institution = '',
    #             department = '',
    #             place_of_discovery = '',
    #             object_history = '', 
    #             exhibition_history = '',
    #             credit_line = '',
    #             inscriptions = '',
    #             notes = '',
    #             accession_number = item.object_number,
    #             place_of_creation = '',
    #             source = '',
    #             permission = '',
    #             other_versions = '',
    #             references = '',
    #             depicted_place = '',
    #             wikidata = '',
    #             categories = categories)

    #             #artwork.GenerateWikiText()

    #         print ('id           =' + item.id)
    #         print ('object_number=' + item.object_number)
    #         print ('image_native =' + item.image_native)
    #         print (artwork.wikitext)

# Get all wikidata items for SMK Wikidata object Q671384
#wikidata.GetInstitutionWikidataItems('Q671384', 'wikidata_smk')
try:
    accession_number:str
    # Set up logging
    commons_error_log = "commons_error.log"
    logging.basicConfig(filename=commons_error_log,level=logging.ERROR,format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    offset=0
    rows=1
    items=0

    output_filename='commons_smk'

    f_csv=open(output_filename+'.csv', 'w+')

    # Print CSV Header
    artwork = commons.ArtworkTemplate()

    while True:
        try:
            accession_number=''
            items=items+1
            smk_objects=smkapi.get_smk_objects(offset, rows)
            print('offset='+str(smk_objects['offset']))
            offset=smk_objects['offset']
            print('rows='+str(smk_objects['rows']))
            rows=smk_objects['rows']
            print('found='+str(smk_objects['found']))
            found=smk_objects['found']
            categories  = """[[Category:SMKOpen Batch Upload]]
            [[Category:Paintings in Statens Museum for Kunst]]"""

            smk_creator=''

            for item in smk_objects['items']:
                if item.get('id'):
                    print(item['id'])
                if item.get('image_native'):
                    print(item['image_native'])
                    image_native=item['image_native']
                if item.get('object_number'):
                    print(item['object_number'])
                    accession_number=item['object_number']
                    smk_object_number=accession_number
                if item.get('public_domain'):
                    print(item['public_domain'])
                if item.get('has_image'):
                    print(item['has_image'])
                if item.get('production'):
                    print(item['production'])
                    smk_creator=str(item['production'][0].get('creator'))
                if item.get('production_date'):
                    print(item['production_date'])
                if item.get('titles'):
                    print(item['titles'])
                if item.get('dimensions'):
                    for dimension in item['dimensions']: 
                        print(dimension['type'])
                        print(dimension['value'])
                        print(dimension['unit'])
                        if 'hojde'==dimension['type']:
                            height=dimension['value']
                        if 'bredde'==dimension['type']:
                            width=dimension['value']
                        if 'mm'==dimension['unit']:
                            unit=dimension['unit']
                    dimensions='{{Size|unit='+str(unit)+'|width='+str(width)+'|height='+str(height)+'}}'

                # Generate artwork template
                desc=''
                production_date=''
                smk_title=''
                smk_period=''
                artwork = commons.ArtworkTemplate(artist = '',
                    author = smk_creator,
                    title = smk_title,
                    desc = desc,
                    depicted_people = '',
                    date = smk_period,
                    medium = '',
                    dimensions = dimensions,
                    institution = '{{Institution:Statens Museum for Kunst, Copenhagen}}',
                    department = '',
                    place_of_discovery = '',
                    object_history = '', 
                    exhibition_history = '',
                    credit_line = '',
                    inscriptions = '',
                    notes = '',
                    accession_number = accession_number,
                    place_of_creation = '',
                    source = 'https://collection.smk.dk/#/en/detail/'+accession_number,
                    permission = '',
                    other_versions = '',
                    references = '',
                    depicted_place = '',
                    wikidata = '',
                    categories = categories)

                #artwork.GenerateWikiText()
                #print(artwork.GenerateCSVLine())

            for keys, item in recursive_iter(smk_objects['items']):
                if 'image_native'==keys[1]:
                    smk_image_native=item
                    print('smk_image_native='+smk_image_native)
                if 'id'==keys[1]:
                    smk_id=item
                    print('smk_id='+smk_id)
                if 'object_number'==keys[1]:
                    smk_object_number=item
                    print('smk_object_number='+smk_object_number)
                if 'public_domain'==keys[1]:
                    smk_public_domain=item
                    print('smk_public_domain='+str(smk_public_domain))
                if 'image_width'==keys[1]:
                    smk_image_width=item
                    print('smk_image_width='+str(smk_image_width))
                if 'image_height'==keys[1]:
                    smk_image_height=item
                    print('smk_image_height='+str(smk_image_height))
                if 'has_image'==keys[1]:
                    smk_has_image=item
                    print('smk_has_image='+str(smk_has_image))
                if 'production'==keys[1]:
                    if 'creator'==keys[3]:
                        # last name, first name
                        creator = item.split(",")
                        smk_creator=creator[1]+' '+creator[0]
                        print('smk_creator='+str(smk_creator))
                if 'production_date'==keys[1]:
                    if 'period'==keys[3]:
                        smk_period=item
                        print('smk_period='+str(smk_period))
                if 'titles'==keys[1]:
                    if 'title'==keys[3]:
                        smk_title=item
                        print('smk_title='+str(smk_title))
                    if 'language'==keys[3]:
                        smk_language=item
                        print('smk_language='+str(smk_language))
                    if 'type'==keys[3]:
                        smk_type=item
                        print('smk_type='+str(smk_type))
                if 'dimensions'==keys[1]:
                    if 'notes'==keys[3]:
                        smk_notes=item
                        print('smk_notes='+str(smk_notes))
                    if 'part'==keys[3]:
                        smk_part=item
                        print('smk_part='+str(smk_part))
                    if 'type'==keys[3]:
                        smk_type=item
                        print('smk_type='+str(smk_type))
                    if 'unit'==keys[3]:
                        smk_unit=item
                        print('smk_unit='+str(smk_unit))

            # Generate artwork template
            desc=''
            production_date=''
            artwork = commons.ArtworkTemplate(artist = '',
                author = smk_creator,
                title = smk_title,
                desc = desc,
                depicted_people = '',
                date = smk_period,
                medium = '',
                dimensions = '',
                institution = '{{Institution:Statens Museum for Kunst, Copenhagen}}',
                department = '',
                place_of_discovery = '',
                object_history = '', 
                exhibition_history = '',
                credit_line = '',
                inscriptions = '',
                notes = '',
                accession_number = str(smk_object_number),
                place_of_creation = '',
                source = 'https://collection.smk.dk/#/en/detail/'+str(smk_object_number),
                permission = '',
                other_versions = '',
                references = '',
                depicted_place = '',
                wikidata = '',
                categories = categories)

                #artwork.GenerateWikiText()

        except Exception as e:
            typeerror=TypeError(e)
            logging.exception(e)
        finally:
            print('items='+str(items))
            offset=offset+1

        if 0==rows:
            break
    
except Exception as e:
    logging.exception(e)
finally:
    print('Export finished')
    print('items='+str(items))
    offset=offset+1


#TestSMKAPI()
#get_smk_object('KMS1')
